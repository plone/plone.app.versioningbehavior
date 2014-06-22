from plone.app.versioningbehavior.testing import VERSIONING_FUNCTIONAL_TESTING
from Products.CMFCore.utils import getToolByName
from unittest2 import TestCase


class InstallTestCase(TestCase):

    layer = VERSIONING_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_skins = getToolByName(self.portal, 'portal_skins')

    def test_should_override_versions_history_form_skin_template(self):
        layer_name = 'plone_app_versioningbehavior'
        self.assertIn(layer_name, self.get_selected_skin_layers())
        layer = self.portal_skins[layer_name]
        self.assertIn('versions_history_form', layer)

    def get_selected_skin_layers(self):
        """
        Return: a sequence of skin layer names corresponding to the default
        skin selection.
        """
        return [l.strip() for l in self.portal_skins.getSkinPath(
                self.portal_skins.getDefaultSkin()).split(',')]
