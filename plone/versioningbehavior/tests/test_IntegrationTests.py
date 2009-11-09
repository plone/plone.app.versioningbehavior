
from Products.CMFEditions.tests import test_IntegrationTests

from Products.PloneTestCase import PloneTestCase
PloneTestCase.setupPloneSite()

from plone.dexterity.fti import DexterityFTI

class TestDexterityIntegration(test_IntegrationTests.TestIntegration):

    def afterSetUp(self):
        # we need to have the Manager role to be able to add things
        # to the portal root
        self.setRoles(['Manager',])

        # add an additional user
        self.portal.acl_users.userFolderAddUser('reviewer', 'reviewer',
                                                ['Manager'], '')

        # now create some dexterity FTIs...
        # ... a document
        document_fti = DexterityFTI('TestingDocument',
                                    factory='TestingDocument')
        document_fti.behaviors = (
                'plone.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
        )
        document_fti.model_source = '''
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="text" type="zope.schema.Text">
                        <title>Text</title>
                        <required>False</required>
                    </field>
                </schema>
            </model>
        '''
        self.portal.portal_types._setObject('TestingDocument', document_fti)
        # ... and a folder
        folder_fti = DexterityFTI('TestingFolder',
                                  factory='TestingFolder')
        folder_fti.behaviors = (
                'plone.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
        )
        self.portal.portal_types._setObject('TestingFolder', folder_fti)

        # now add a document
        self.portal.invokeFactory('TestingDocument', 'doc')

        # and add a folder with two documents in it
        self.portal.invokeFactory('TestingFolder', 'fol')
        self.portal.fol.invokeFactory('TestingDocument', 'doc1')
        self.portal.fol.invokeFactory('TestingDocument', 'doc2')

    def test11_versionAFolderishObjectThatTreatsChildrensAsInsideRefs(self):
        # XXX disabled
        pass

    def test13_revertUpdatesCatalog(self):
        # XXX disabled
        # This test in CMFEditions uses doc.edit, but we have no archetypes
        # objects so doc.edit is portal.edit (acquisition), which is wrong...
        pass

    def test15_retrieveInsideRefsFolderWithAddedOrDeletedObjects(self):
        # XXX disabled
        pass

    def test16_revertInsideRefsUpdatesCatalog(self):
        # XXX disabled
        pass

    def test17_moveInsideRefThenRevertChangesUid(self):
        # XXX disabled
        pass

    def test21_DontLeaveDanglingCatalogEntriesWhenInvokingFactory(self):
        # XXX disabled
        pass




from unittest import TestSuite, makeSuite
def test_suite():
    from Products.PloneTestCase import PloneTestCase
    from Testing.ZopeTestCase import FunctionalDocFileSuite as FileSuite

    suite = TestSuite()
    suite.addTest(makeSuite(TestDexterityIntegration))
    return suite
