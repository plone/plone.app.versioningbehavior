# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.dexterity.fti import DexterityFTI
from plone.protect import auto as protect_auto
from plone.testing import z2
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.TextDiff import TextDiff

import plone.app.versioningbehavior


TEST_CONTENT_TYPE_ID = 'TestContentType'
DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert',)


class PloneAppVersioningbehaviorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=plone.app.versioningbehavior)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.versioningbehavior:default')
        self.registerVersionedDocumentFTI(portal)

    def registerVersionedDocumentFTI(self, portal):
        types_tool = getToolByName(portal, 'portal_types')
        fti = DexterityFTI(
            TEST_CONTENT_TYPE_ID,
            global_allow=True,
            behaviors=(
                'plone.app.versioningbehavior.behaviors.IVersionable',
                'plone.app.dexterity.behaviors.metadata.IBasic',
            ),
            model_source="""
                <model xmlns="http://namespaces.plone.org/supermodel/schema"
                       xmlns:marshal="http://namespaces.plone.org/supermodel/marshal">
                    <schema>
                        <field name="text" type="zope.schema.Text">
                            <title>Text</title>
                            <required>False</required>
                        </field>
                        <field name="file" type="plone.namedfile.field.NamedBlobFile"
                            marshal:primary="true">
                          <title>File</title>
                          <required>False</required>
                        </field>
                    </schema>
                </model>
                """)
        types_tool._setObject(TEST_CONTENT_TYPE_ID, fti)

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

    def testSetUp(self):
        self.CSRF_DISABLED_ORIGINAL = protect_auto.CSRF_DISABLED
        protect_auto.CSRF_DISABLED = True

    def testTearDown(self):
        protect_auto.CSRF_DISABLED = self.CSRF_DISABLED_ORIGINAL

PLONE_APP_VERSIONINGBEHAVIOR_FIXTURE = PloneAppVersioningbehaviorLayer()


PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONE_APP_VERSIONINGBEHAVIOR_FIXTURE,),
    name='PloneAppVersioningbehaviorLayer:IntegrationTesting',
)


PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PLONE_APP_VERSIONINGBEHAVIOR_FIXTURE,),
    name='PloneAppVersioningbehaviorLayer:FunctionalTesting',
)


PLONE_APP_VERSIONINGBEHAVIOR_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PLONE_APP_VERSIONINGBEHAVIOR_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='PloneAppVersioningbehaviorLayer:AcceptanceTesting',
)
