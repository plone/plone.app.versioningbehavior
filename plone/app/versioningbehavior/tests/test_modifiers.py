# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.versioningbehavior.modifiers import CloneNamedFileBlobs
from plone.app.versioningbehavior.modifiers import SkipRelations
from plone.app.versioningbehavior.testing import PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING
from plone.app.versioningbehavior.testing import PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.fti import DexterityFTI
from plone.dexterity.schema import portalTypeToSchemaName
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer
from plone.namedfile import field
from plone.namedfile.file import NamedBlobFile
from plone.supermodel import model
from six import StringIO
from z3c.relationfield.relation import RelationValue
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from ZODB.interfaces import IBlob
from zope.component import getUtility
from zope.configuration import xmlconfig
from zope.interface import alsoProvides
from zope.interface import Interface
from zope.intid.interfaces import IIntIds

import transaction
import unittest


class IBlobFile(model.Schema):
    file = field.NamedBlobFile(title=u'File')


alsoProvides(IBlobFile, IFormFieldProvider)


class IRelationsType(Interface):
    single = RelationChoice(title=u'Single',
                            required=False, values=[])
    multiple = RelationList(title=u'Multiple (Relations field)',
                            required=False)


class IRelationsBehavior(model.Schema):
    single = RelationChoice(title=u'Single',
                            required=False, values=[])
    multiple = RelationList(title=u'Multiple (Relations field)',
                            required=False)


alsoProvides(IRelationsBehavior, IFormFieldProvider)


class TestModifiers(unittest.TestCase):

    layer = PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        # we need to have the Manager role to be able to add things
        # to the portal root
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def testCloneNamedFileBlobsInSchema(self):
        file_fti = DexterityFTI(
            'BlobFile',
            model_source="""
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="file"
                           type="plone.namedfile.field.NamedBlobFile">
                        <title>File</title>
                        <required>True</required>
                    </field>
                </schema>
            </model>
        """)
        self.portal.portal_types._setObject('BlobFile', file_fti)

        file1 = createContentInContainer(self.portal, 'BlobFile')
        file1.file = NamedBlobFile('dummy test data', filename=u'test.txt')
        modifier = CloneNamedFileBlobs('modifier', 'Modifier')
        attrs_dict = modifier.getReferencedAttributes(file1)
        self.assertTrue(
            'plone.dexterity.schema.generated.plone_0_BlobFile.file'
            in attrs_dict)
        blob = list(attrs_dict.values())[0]
        self.assertTrue(IBlob.providedBy(blob))

        file2 = createContentInContainer(self.portal, 'BlobFile')
        file2.file = NamedBlobFile('dummy test data', filename=u'test.txt')
        modifier.reattachReferencedAttributes(file2, attrs_dict)
        self.assertTrue(file2.file._blob is blob)

    def testCloneNamedFileBlobsInBehavior(self):
        configuration = """\
        <configure
             package="plone.behavior"
             xmlns="http://namespaces.zope.org/zope"
             xmlns:plone="http://namespaces.plone.org/plone"
             i18n_domain="plone.behavior.tests">

             <include package="plone.behavior" file="meta.zcml" />

            <plone:behavior
                title="BlobFile behavior"
                description="A behavior"
                provides="plone.app.versioningbehavior.tests.test_modifiers.IBlobFile"
                factory="plone.behavior.AnnotationStorage"
                />
        </configure>
        """
        xmlconfig.xmlconfig(StringIO(configuration))

        file_fti = DexterityFTI(
            'BlobFile',
            behaviors=[IBlobFile.__identifier__])
        self.portal.portal_types._setObject('BlobFile', file_fti)

        file1 = createContentInContainer(self.portal, 'BlobFile')
        IBlobFile(file1).file = NamedBlobFile('dummy test data',
                                              filename=u'test.txt')
        modifier = CloneNamedFileBlobs('modifier', 'Modifier')
        attrs_dict = modifier.getReferencedAttributes(file1)
        self.assertTrue(
            'plone.app.versioningbehavior.tests.test_modifiers.IBlobFile.file'
            in attrs_dict)
        blob = list(attrs_dict.values())[0]
        self.assertTrue(IBlob.providedBy(blob))

        file2 = createContentInContainer(self.portal, 'BlobFile')
        IBlobFile(file2).file = NamedBlobFile('dummy test data',
                                              filename=u'test.txt')
        modifier.reattachReferencedAttributes(file2, attrs_dict)
        self.assertTrue(IBlobFile(file2).file._blob is blob)

    def testCloneNamedFileBlobsOnCloneModifiers(self):
        file_fti = DexterityFTI(
            'BlobFile',
            model_source="""
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="file"
                           type="plone.namedfile.field.NamedBlobFile">
                        <title>File</title>
                        <required>True</required>
                    </field>
                </schema>
            </model>
        """)
        self.portal.portal_types._setObject('BlobFile', file_fti)

        file1 = createContentInContainer(self.portal, 'BlobFile')
        file1.file = NamedBlobFile('dummy test data', filename=u'test.txt')
        modifier = CloneNamedFileBlobs('modifier', 'Modifier')
        on_clone_modifiers = modifier.getOnCloneModifiers(file1)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(file1.file._blob))
        self.assertTrue(pers_load(file1.file._blob) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

    def testCloneNamedFileBlobsWithNoFile(self):
        file_fti = DexterityFTI(
            'BlobFile',
            model_source="""
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="file"
                           type="plone.namedfile.field.NamedBlobFile">
                        <title>File</title>
                        <required>True</required>
                    </field>
                </schema>
            </model>
        """)
        self.portal.portal_types._setObject('BlobFile', file_fti)
        file1 = createContentInContainer(self.portal, 'BlobFile')
        modifier = CloneNamedFileBlobs('modifier', 'Modifier')
        attrs_dict = modifier.getReferencedAttributes(file1)
        self.assertTrue(attrs_dict == {})
        on_clone_modifiers = modifier.getOnCloneModifiers(file1)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(None) is None)
        self.assertTrue(pers_load(None) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

        # Previous version without file but working copy has a file.
        self.portal.portal_repository.save(file1)
        file1.file = NamedBlobFile('dummy test data', filename=u'test.txt')
        attrs_dict = modifier.getReferencedAttributes(file1)
        self.assertTrue(
            'plone.dexterity.schema.generated.plone_0_BlobFile.file'
            in attrs_dict)
        blob = list(attrs_dict.values())[0]
        self.assertTrue(IBlob.providedBy(blob))
        on_clone_modifiers = modifier.getOnCloneModifiers(file1)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(file1.file._blob))
        self.assertTrue(pers_load(file1.file._blob) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

    def testRelations(self):
        rel_fti = DexterityFTI(
            'RelationsType',
            schema=IRelationsType.__identifier__
        )
        self.portal.portal_types._setObject('RelationsType', rel_fti)

        intids = getUtility(IIntIds)

        source = createContentInContainer(self.portal, 'RelationsType')
        target = createContentInContainer(self.portal, 'RelationsType')

        # Test modifier when no relations are set
        modifier = SkipRelations('modifier', 'Modifier')
        on_clone_modifiers = modifier.getOnCloneModifiers(source)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(None) is None)
        self.assertTrue(pers_id(None) is None)
        self.assertTrue(pers_load(None) is None)
        self.assertTrue(pers_load(None) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

        repo_clone = createContent('RelationsType')
        modifier.afterRetrieveModifier(source, repo_clone)
        self.assertTrue(repo_clone.single is source.single)
        self.assertTrue(repo_clone.multiple is source.multiple)

        # Add some relations
        source.single = RelationValue(intids.getId(target))
        source.multiple = [RelationValue(intids.getId(target))]

        # Update relations
        from zope.lifecycleevent import ObjectModifiedEvent
        from zope.event import notify
        notify(ObjectModifiedEvent(source))

        modifier = SkipRelations('modifier', 'Modifier')
        on_clone_modifiers = modifier.getOnCloneModifiers(source)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(source.single))
        self.assertTrue(pers_id(source.multiple))
        self.assertTrue(pers_load(source.single) is None)
        self.assertTrue(pers_load(source.multiple) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

        repo_clone = createContent('RelationsType')
        modifier.afterRetrieveModifier(source, repo_clone)
        self.assertTrue(repo_clone.single is source.single)
        self.assertTrue(repo_clone.multiple is source.multiple)

    def register_RelationsType(self):
        xmlconfig.xmlconfig(StringIO(
            '''
            <configure
                 package="plone.behavior"
                 xmlns="http://namespaces.zope.org/zope"
                 xmlns:plone="http://namespaces.plone.org/plone"
                 i18n_domain="plone.behavior.tests">

                 <include package="plone.behavior" file="meta.zcml" />

                <plone:behavior
                    title="Relations behavior"
                    description="A behavior"
                    provides="plone.app.versioningbehavior.tests.test_modifiers.IRelationsBehavior"
                    />
            </configure>
            '''
        ))
        rel_fti = DexterityFTI(
            'RelationsType',
            behaviors=[IRelationsBehavior.__identifier__]
        )
        self.portal.portal_types._setObject('RelationsType', rel_fti)

    def testRelationsInBehaviors(self):
        self.register_RelationsType()
        intids = getUtility(IIntIds)

        source = createContentInContainer(self.portal, 'RelationsType')
        target = createContentInContainer(self.portal, 'RelationsType')

        # Test modifier when no relations are set
        modifier = SkipRelations('modifier', 'Modifier')
        on_clone_modifiers = modifier.getOnCloneModifiers(source)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(None) is None)
        self.assertTrue(pers_id(None) is None)
        self.assertTrue(pers_load(None) is None)
        self.assertTrue(pers_load(None) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

        repo_clone = createContent('RelationsType')
        modifier.afterRetrieveModifier(source, repo_clone)
        self.assertTrue(repo_clone.single is None)
        self.assertTrue(repo_clone.multiple is None)

        # Add some relations
        IRelationsBehavior(source).single = RelationValue(
            intids.getId(target)
        )
        IRelationsBehavior(source).multiple = [
            RelationValue(intids.getId(target))
        ]

        # Update relations
        from zope.lifecycleevent import ObjectModifiedEvent
        from zope.event import notify
        notify(ObjectModifiedEvent(source))

        modifier = SkipRelations('modifier', 'Modifier')
        on_clone_modifiers = modifier.getOnCloneModifiers(source)
        pers_id, pers_load, empty1, empty2 = on_clone_modifiers
        self.assertTrue(pers_id(IRelationsBehavior(source).single))
        self.assertTrue(pers_id(IRelationsBehavior(source).multiple))
        self.assertTrue(pers_load(IRelationsBehavior(source).single) is None)
        self.assertTrue(pers_load(IRelationsBehavior(source).multiple) is None)
        self.assertTrue(empty1 == [])
        self.assertTrue(empty2 == [])

        repo_clone = createContent('RelationsType')
        modifier.afterRetrieveModifier(source, repo_clone)
        self.assertTrue(IRelationsBehavior(repo_clone).single
                        is IRelationsBehavior(source).single)
        self.assertTrue(IRelationsBehavior(repo_clone).multiple
                        is IRelationsBehavior(source).multiple)

    def testRelationsInBehaviorsForMigratedDXObjects(self):
        ''' Do not break in the case of
        dexterity objects with relations migrated from something else
        (e.g. Archetypes)
        '''
        self.register_RelationsType()
        source = createContentInContainer(self.portal, 'RelationsType')

        # Test modifier when no relations are set
        class Dummy(object):
            pass

        repo_clone = Dummy()

        modifier = SkipRelations('modifier', 'Modifier')
        modifier.afterRetrieveModifier(source, repo_clone)

        self.assertFalse(hasattr(repo_clone, 'single'))
        self.assertFalse(hasattr(repo_clone, 'multiple'))


class TestModifiersFunctional(unittest.TestCase):

    layer = PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        # we need to have the Manager role to be able to add things
        # to the portal root
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def testCloneNamedFileBlobsInUpdatedSchema(self):
        file_fti = DexterityFTI(
            'BlobFile',
            model_source="""
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="file"
                           type="plone.namedfile.field.NamedBlobFile">
                        <title>File</title>
                        <required>True</required>
                    </field>
                </schema>
            </model>
        """)
        self.portal.portal_types._setObject('BlobFile', file_fti)

        # Sets _p_mtime on FTI used in schema suffix in p.dexterity >= 2.10.0
        transaction.commit()

        file1 = createContentInContainer(self.portal, 'BlobFile')
        file1.file = NamedBlobFile('dummy test data', filename=u'test.txt')
        modifier = CloneNamedFileBlobs('modifier', 'Modifier')
        attrs_dict = modifier.getReferencedAttributes(file1)
        schema_name = portalTypeToSchemaName(
            'BlobFile',
            suffix=repr(self.portal.portal_types.BlobFile._p_mtime)
        )
        attr = "plone.dexterity.schema.generated." + schema_name + ".file"
        self.assertTrue(attr in attrs_dict)
        blob = list(attrs_dict.values())[0]
        self.assertTrue(IBlob.providedBy(blob))

        # Update _p_mtime on FTI
        self.portal.portal_types.BlobFile._p_changed = True
        transaction.commit()

        # Test that modifier can attach after schema suffix has changed
        modifier.reattachReferencedAttributes(file1, attrs_dict)
