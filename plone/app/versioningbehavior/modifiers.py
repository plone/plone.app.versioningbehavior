# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from Acquisition import aq_base
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata, resolveDottedName
from plone.namedfile.interfaces import INamedBlobFileField
from plone.namedfile.interfaces import INamedBlobImageField
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.interfaces.IArchivist import ArchivistRetrieveError
from Products.CMFEditions.interfaces.IModifier import IAttributeModifier
from Products.CMFEditions.interfaces.IModifier import ICloneModifier
from Products.CMFEditions.interfaces.IModifier import ISaveRetrieveModifier
from Products.CMFEditions.Modifiers import ConditionalTalesModifier
from Products.CMFEditions.utilities import dereference
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from z3c.relationfield.interfaces import IRelationChoice, IRelationList
from ZODB.blob import Blob
from zope.interface import implementer
from zope.schema import getFields


import os
import six

# XXX needs to become some kind of util lookup...
BEHAVIOR_LOOKUP = {
    'plone.app.contenttypes.behaviors.leadimage.ILeadImage':
        'plone.app.contenttypes.behaviors.leadimage.ILeadImageBehavior'

}


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


def fetch_blob_from_history(obj, field_name, version_id=None):
    # For some reason, the blob cannot be retrieved from the actual
    # object any more. A common reason can be that the behavior that provides
    # the field was renamed.
    # In this case, take the appropriate version from the history storage and
    # try to retrieve the blob directly.
    archivist_tool = getToolByName(obj, 'portal_archivist')
    item, history_id = dereference(obj, zodb_hook=archivist_tool)
    storage = getToolByName(obj, 'portal_historiesstorage')
    version_data = storage.retrieve(history_id, version_id)
    # We know that the blob will be stored under a key that starts with our
    # class name, and that ends with the field name.
    # Now look up the (XXX utility) mapping of changed behavior names.
    # If the interface name of the key is found in the mapping, meaning we
    # know that it was an interface that has now been renamed,
    # return the blob stored under that key.
    for key in version_data.referenced_data.keys():
        if not key.startswith('CloneNamedFileBlobs'):
            continue
        name = key.split('/')[-1]
        iface_name, f_name = name.rsplit('.', 1)
        if f_name == field_name and iface_name in BEHAVIOR_LOOKUP:
            blob = version_data.referenced_data[key]
            if blob:
                return blob


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

                    if not field_value._blob:
                        # Get the current version, don't pass version_id
                        actual_field_blob = fetch_blob_from_history(obj, name)
                    else:
                        actual_field_blob = field_value._blob

                    # The blob is simply not there. We can't do anything more.
                    if not actual_field_blob:
                        continue

                    blob_file = actual_field_blob.open()
                    save_new = True
                    dotted_name = '.'.join([schemata.__identifier__, name])

                    if prior_rev is not None:
                        prior_obj = prior_rev.object
                        prior_blob = field.get(field.interface(prior_obj))
                        if prior_blob is not None:

                            if not prior_blob._blob:
                                # Get the appropriate older version
                                actual_prior_blob = fetch_blob_from_history(
                                    obj, name, prior_rev.version_id)
                            else:
                                actual_prior_blob = prior_blob._blob

                            # The blob is simply not there. Continue...
                            if not actual_prior_blob:
                                continue

                            prior_file = actual_prior_blob.open()

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
            iface_name, f_name = name.rsplit('.', 1)
            # Look up if the interface might have changed
            # XXX make this a utility lookup...
            if iface_name in BEHAVIOR_LOOKUP:
                iface_name = BEHAVIOR_LOOKUP[iface_name]
            iface = resolveDottedName(iface_name)
            field = iface.get(f_name)
            if field is not None:  # Field may have been removed from schema
                adapted_field = field.get(iface(obj))
                if adapted_field:
                    adapted_field._blob = blob

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
