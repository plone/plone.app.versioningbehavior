# -*- coding: utf-8 -*-
from Acquisition import aq_base
from AccessControl.class_init import InitializeClass
from plone.dexterity.utils import iterSchemata, resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedBlobFileField
from plone.namedfile.interfaces import INamedBlobImageField
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.interfaces.IArchivist import ArchivistRetrieveError
from Products.CMFEditions.interfaces.IModifier import IAttributeModifier
from Products.CMFEditions.interfaces.IModifier import ICloneModifier
from Products.CMFEditions.interfaces.IModifier import ISaveRetrieveModifier
from Products.CMFEditions.Modifiers import ConditionalTalesModifier
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZODB.blob import Blob
from zope.interface import implementer
from zope.schema import getFields
from z3c.relationfield.interfaces import IRelationChoice, IRelationList

import os
import six


manage_CloneNamedFileBlobsAddForm =  \
    PageTemplateFile(
        'www/CloneNamedFileBlobs.pt',
        globals(),
        __name__='manage_CloneNamedFileBlobs',
    )


def getCallbacks(values):
    """Return persistent callbacks.

    Register the provided values in a mapping object and return a set
    of persistent callbacks that effectively replace the values with
    ``None``.
    """

    # Important: We must keep a reference to the
    # field value here because it may be a newly
    # created object and we want to ensure that
    # it's not garbage collected and "reused".
    mapping = dict((id(value), value) for value in values)

    def persistent_id(obj):
        return mapping.get(id(obj), None)

    def persistent_load(obj):
        return None

    return persistent_id, persistent_load


def getFieldValues(obj, *ifaces):
    if IDexterityContent.providedBy(obj):
        for schemata in iterSchemata(obj):
            for name, field in getFields(schemata).items():
                for iface in ifaces:
                    if iface.providedBy(field):
                        field_value = field.query(field.interface(obj))
                        if field_value is not None:
                            yield field_value


def manage_addCloneNamedFileBlobs(self, id, title=None, REQUEST=None):
    """Add a clone namedfile blobs modifier.
    """
    modifier = CloneNamedFileBlobs(id, title)
    self._setObject(id, modifier)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')


manage_SkipRelationsAddForm =  \
    PageTemplateFile(
        'www/SkipRelations.pt',
        globals(),
        __name__='manage_SkipRelationsAddForm',
    )


def manage_addSkipRelations(self, id, title=None, REQUEST=None):
    """Add a skip relations modifier.
    """
    modifier = SkipRelations(id, title)
    self._setObject(id, modifier)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')


@implementer(IAttributeModifier, ICloneModifier)
class CloneNamedFileBlobs:
    """Modifier to save an un-cloned reference to the blob to avoid it being
    packed away.
    """

    def __init__(self, id_, title):
        self.id = str(id_)
        self.title = str(title)

    def getReferencedAttributes(self, obj):
        file_data = {}
        # Try to get last revision, only store a new blob if the
        # contents differ from the prior one, otherwise store a
        # reference to the prior one.
        # The implementation is mostly based on CMFEditions's CloneBlobs
        # modifier.
        repo = getToolByName(obj, 'portal_repository')
        try:
            prior_rev = repo.retrieve(obj)
        except ArchivistRetrieveError:
            prior_rev = None

        for schemata in iterSchemata(obj):
            for name, field in getFields(schemata).items():
                if (INamedBlobFileField.providedBy(field) or
                        INamedBlobImageField.providedBy(field)):
                    try:
                        # field.get may raise an AttributeError if the field
                        # is provided by a behavior and hasn't been
                        # initialized yet
                        field_value = field.get(field.interface(obj))
                    except AttributeError:
                        field_value = None
                    if field_value is None:
                        continue
                    blob_file = field_value.open()
                    save_new = True
                    dotted_name = '.'.join([schemata.__identifier__, name])

                    if prior_rev is not None:
                        prior_obj = prior_rev.object
                        prior_blob = field.get(field.interface(prior_obj))
                        if prior_blob is not None:
                            prior_file = prior_blob.open()

                            # Check for file size differences
                            if (os.fstat(prior_file.fileno()).st_size ==
                                    os.fstat(blob_file.fileno()).st_size):
                                # Files are the same size, compare line by line
                                for line, prior_line in six.moves.zip(
                                        blob_file, prior_file):
                                    if line != prior_line:
                                        break
                                else:
                                    # The files are the same, save a reference
                                    # to the prior versions blob on this
                                    # version
                                    file_data[dotted_name] = prior_blob._blob
                                    save_new = False

                    if save_new:
                        new_blob = file_data[dotted_name] = Blob()
                        new_blob_file = new_blob.open('w')
                        try:
                            blob_file.seek(0)
                            new_blob_file.writelines(blob_file)
                        finally:
                            blob_file.close()
                            new_blob_file.close()

        return file_data

    def reattachReferencedAttributes(self, obj, attrs_dict):
        obj = aq_base(obj)
        for name, blob in six.iteritems(attrs_dict):
            iface = resolveDottedName('.'.join(name.split('.')[:-1]))
            fname = name.split('.')[-1]
            field = iface.get(fname)
            if field is not None:  # Field may have been removed from schema
                field.get(iface(obj))._blob = blob

    def getOnCloneModifiers(self, obj):
        """Removes references to blobs.
        """

        persistent_id, persistent_load = getCallbacks(
            aq_base(value._blob) for value
            in getFieldValues(obj, INamedBlobFileField, INamedBlobImageField)
        )

        return persistent_id, persistent_load, [], []


InitializeClass(CloneNamedFileBlobs)


@implementer(ICloneModifier, ISaveRetrieveModifier)
class SkipRelations:
    """Standard modifier to avoid cloning of relations and
    restore them from the working copy.
    """

    def __init__(self, id_, title):
        self.id = str(id_)
        self.title = str(title)

    def getOnCloneModifiers(self, obj):
        """Removes relations.
        """

        persistent_id, persistent_load = getCallbacks(
            aq_base(value) for value
            in getFieldValues(obj, IRelationChoice, IRelationList)
        )

        return persistent_id, persistent_load, [], []

    def beforeSaveModifier(self, obj, clone):
        """Does nothing, the pickler does the work."""
        return {}, [], []

    def afterRetrieveModifier(self, obj, repo_clone, preserve=()):
        """Restore relations from the working copy."""
        if (
            IDexterityContent.providedBy(obj) and
            IDexterityContent.providedBy(repo_clone)
        ):
            for schemata in iterSchemata(obj):
                for name, field in getFields(schemata).items():
                    if (IRelationChoice.providedBy(field) or
                            IRelationList.providedBy(field)):
                        field.set(field.interface(repo_clone),
                                  field.query(field.interface(obj)))
        return [], [], {}


InitializeClass(SkipRelations)


modifiers = (
    {
        'id': 'CloneNamedFileBlobs',
        'title': "Store blobs by reference on content",
        'enabled': True,
        'condition': "python:True",
        'wrapper': ConditionalTalesModifier,
        'modifier': CloneNamedFileBlobs,
        'form': manage_CloneNamedFileBlobsAddForm,
        'factory': manage_addCloneNamedFileBlobs,
        'icon': 'www/modifier.gif',
    },
    {
        'id': 'SkipRelations',
        'title': "Skip saving of relations",
        'enabled': True,
        'condition': "python:True",
        'wrapper': ConditionalTalesModifier,
        'modifier': SkipRelations,
        'form': manage_SkipRelationsAddForm,
        'factory': manage_addSkipRelations,
        'icon': 'www/modifier.gif',
    },
)
