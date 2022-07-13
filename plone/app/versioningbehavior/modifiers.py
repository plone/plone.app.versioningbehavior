# -*- coding: utf-8 -*-
from AccessControl.class_init import InitializeClass
from Acquisition import aq_base
from plone.behavior.registration import BehaviorRegistrationNotFound
from plone.behavior.registration import lookup_behavior_registration
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.schema import SCHEMA_CACHE
from plone.dexterity.schema import schemaNameToPortalType
from plone.dexterity.utils import iterSchemata
from plone.dexterity.utils import resolveDottedName
from plone.namedfile.interfaces import INamedBlobFileField
from plone.namedfile.interfaces import INamedBlobImageField
from Products.CMFEditions.interfaces.IModifier import IAttributeModifier
from Products.CMFEditions.interfaces.IModifier import ICloneModifier
from Products.CMFEditions.interfaces.IModifier import ISaveRetrieveModifier
from Products.CMFEditions.Modifiers import ConditionalTalesModifier
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from z3c.relationfield.interfaces import IRelationChoice, IRelationList
from zope.interface import implementer
from zope.schema import getFields


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
    """Modifier to store an un-cloned reference to blobs.

    Without this, the Blob instance is cloned
    without also copying its connected file.

    (The name of the class is misleading; it remains for backwards
    compatibility with persistent objects but it's left over from
    a time when the implementation cloned the Blob. Now the whole
    point of this modifier is to avoid cloning the Blob,
    because it's unnecessary and slow.)
    """

    def __init__(self, id_, title):
        self.id = str(id_)
        self.title = str(title)

    def getReferencedAttributes(self, obj):
        file_data = {}
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
                    dotted_name = '.'.join([schemata.__identifier__, name])
                    file_data[dotted_name] = field_value._blob
        return file_data

    def reattachReferencedAttributes(self, obj, attrs_dict):
        obj = aq_base(obj)
        for name, blob in attrs_dict.items():
            iface_name, f_name = name.rsplit('.', 1)
            generated_prefix = 'plone.dexterity.schema.generated.'
            # In case the field is provided via a behavior:
            # Look up the behavior via dotted name.
            # If the behavior's dotted name was changed, we might still have
            # the old name in our attrs_dict.
            # Use the fallback of plone.behavior, provided via the field
            # former_dotted_names, so that the correct behavior can still
            # be found.
            try:
                behavior = lookup_behavior_registration(iface_name)
                iface = behavior.interface
            except BehaviorRegistrationNotFound:
                # Not a behavior - fetch the interface directly
                if iface_name.startswith(generated_prefix):
                    portal_type = schemaNameToPortalType(iface_name)
                    iface = SCHEMA_CACHE.get(portal_type)
                else:
                    iface = resolveDottedName(iface_name)
            field = iface.get(f_name)
            if field is not None:  # Field may have been removed from schema
                adapted_field = field.get(iface(obj))
                if adapted_field:
                    adapted_field._blob = blob

    def getOnCloneModifiers(self, obj):
        """Removes references to blobs in the cloned object.
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
