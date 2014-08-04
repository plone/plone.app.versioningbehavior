#coding=utf8

from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName
from Products.CMFDiffTool.TextDiff import TextDiff
from Products.PloneTestCase.layer import onteardown
from zope.configuration import xmlconfig

# Make it work with plone.protect < 3.0.0 where the `auto` module is not available.
# This is necessary for Plone 4.3.x compatibility.
try:
    from plone.protect import auto as protect_auto
except ImportError:
    class DummyAuto(object):
        CSRF_DISABLED = True
    protect_auto = DummyAuto()


def fix_plonetestcase_mess():
    """Registers a Products.PloneTestCase cleanup.
    It is a nested teardown so that we can meake sure that it is executate
    as last tear down function.
    """
    def reset_zope2():
        """Testing.ZopeTestCase.layer.ZopeLite does not support tearing down.
        This results in a partically teared down Zope2 instance.
        This function resets the Zope2 initialization state so that we can
        initialize another Zope2 instance with p.a.testing.
        """
        import Zope2
        Zope2._began_startup = 0
    onteardown(reset_zope2)()
onteardown(fix_plonetestcase_mess)()


TEST_CONTENT_TYPE_ID = 'TestContentType'
DEFAULT_POLICIES = ('at_edit_autoversion', 'version_on_revert',)


class VersioningLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.versioningbehavior
        xmlconfig.file('configure.zcml', plone.app.versioningbehavior,
                       context=configurationContext)

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
            model_source='''
                <model xmlns="http://namespaces.plone.org/supermodel/schema">
                    <schema>
                        <field name="text" type="zope.schema.Text">
                            <title>Text</title>
                            <required>False</required>
                        </field>
                    </schema>
                </model>
                ''')
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


VERSIONING_FIXTURE = VersioningLayer()
VERSIONING_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VERSIONING_FIXTURE,),
    name="plone.app.versioningbehavior:functional")
