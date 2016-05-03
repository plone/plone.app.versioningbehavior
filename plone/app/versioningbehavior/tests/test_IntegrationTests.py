# -*- coding: utf-8 -*-
from ..testing import VERSIONING_INTEGRATION_TESTING
from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.tests import test_IntegrationTests
from unittest import makeSuite
from unittest import TestSuite


class TestDexterityIntegration(test_IntegrationTests.TestIntegration):
    """This tests is the same tests as in CMFEditions, but it's run for
    dexterity Document and dexterity Folder.
    """

    layer = VERSIONING_INTEGRATION_TESTING

    def afterSetUp(self):
        # get some tools
        types_tool = getToolByName(self.portal, 'portal_types')
        repo_tool = getToolByName(self.portal, 'portal_repository')
        acl_users = getToolByName(self.portal, 'acl_users')

        # we need to have the Manager role to be able to add things
        # to the portal root
        self.setRoles(['Manager', ])

        # add an additional user
        acl_users.userFolderAddUser('reviewer', 'reviewer',
                                    ['Manager'], '')

        # now create some dexterity FTIs...
        # ... a document
        document_fti = DexterityFTI(
            'Document',
            factory='Document',
            global_allow=True,
            behaviors=(
                'plone.app.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
            ),
            model_source="""
            <model xmlns="http://namespaces.plone.org/supermodel/schema">
                <schema>
                    <field name="text" type="zope.schema.Text">
                        <title>Text</title>
                        <required>False</required>
                    </field>
                </schema>
            </model>
        """)
        if 'Document' in types_tool.objectIds():
            types_tool._delObject('Document')
        types_tool._setObject('Document', document_fti)

        # ... and a folder
        folder_fti = DexterityFTI(
            'Folder',
            factory='Folder',
            klass='plone.dexterity.content.Container',
            global_allow=True,
            allowed_content_types=('Document',),
            behaviors=(
                'plone.app.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
            ))
        if 'Folder' in types_tool.objectIds():
            types_tool._delObject('Folder')
        types_tool._setObject('Folder', folder_fti)

        # lets disable versioning while creating, otherwise we'd have to
        # change all tests because we'd have an initial versions and the
        # archetypes tests wouldnt have one after just calling
        # invokeFactory - that's the difference between archetypes and
        # zope events..

        vtypes = repo_tool.getVersionableContentTypes()
        vtypes.remove('Document')
        repo_tool.setVersionableContentTypes(vtypes)

        # now add a document
        self.portal.invokeFactory('Document', 'doc')

        # and add a folder with two documents in it
        self.portal.invokeFactory('Folder', 'fol')
        self.portal.fol.invokeFactory('Document', 'doc1')
        self.portal.fol.invokeFactory('Document', 'doc2')

        # re-enable versioning
        vtypes.append('Dpcument')
        repo_tool.setVersionableContentTypes(vtypes)

        # We have a test that fails without workflow.
        wf_tool = getToolByName(self.portal, 'portal_workflow')
        wf_tool.setChainForPortalTypes(('Document',), ('simple_publication_workflow',))

    def test13_revertUpdatesCatalog(self):
        # This test in CMFEditions uses doc.edit, but we have no archetypes
        # objects so doc.edit is portal.edit (acquisition), which is wrong...
        pass


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestDexterityIntegration))
    return suite
