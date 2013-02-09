#coding=utf8
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.TextDiff import TextDiff
from plone.app.testing import (
    IntegrationTesting, FunctionalTesting, PLONE_FIXTURE, PloneSandboxLayer)
from plone.dexterity.fti import DexterityFTI

TEST_CONTENT_TYPE_ID = 'TestContentType'

DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert',)


class PackageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        import plone.app.versioningbehavior
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=plone.app.versioningbehavior)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.versioningbehavior:default')

        types_tool = getToolByName(portal, 'portal_types')

        fti = DexterityFTI(
            TEST_CONTENT_TYPE_ID,
            factory=TEST_CONTENT_TYPE_ID,
            global_allow=True,
            behaviors=(
                'plone.app.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
                'plone.app.dexterity.behaviors.metadata.IRelatedItems',
            ),
            model_source='''
                <model xmlns="http://namespaces.plone.org/supermodel/schema">
                    <schema>
                        <field name="text" type="zope.schema.Text">
                            <title>Text</title>
                            <required>False</required>
                        </field>
                    </schema>
                </model>
                '''
        )
        types_tool._setObject(TEST_CONTENT_TYPE_ID, fti)

        self['test_content_type_fti'] = fti

        diff_tool = getToolByName(portal, 'portal_diff')
        diff_tool.setDiffForPortalType(
            TEST_CONTENT_TYPE_ID, {'text': TextDiff.meta_type})

        portal_repository = getToolByName(portal, 'portal_repository')
        portal_repository.setVersionableContentTypes(
            list(portal_repository.getVersionableContentTypes()) +
            [TEST_CONTENT_TYPE_ID])
        for policy_id in DEFAULT_POLICIES:
            portal_repository.addPolicyForContentType(
                TEST_CONTENT_TYPE_ID, policy_id)

FIXTURE = PackageLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='plone.app.versioningbehavior:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='plone.app.versioningbehavior:Functional')
