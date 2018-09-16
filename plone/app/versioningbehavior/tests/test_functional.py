# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.versioningbehavior.testing import PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING
from plone.app.versioningbehavior.testing import TEST_CONTENT_TYPE_ID
from plone.testing.z2 import Browser

import transaction
import unittest


class FunctionalTestCase(unittest.TestCase):

    layer = PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()

        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))

        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Member'])
        self.portal.invokeFactory(
            type_name=TEST_CONTENT_TYPE_ID,
            id='obj1',
            title=u'Object 1 Title',
            description=u'Description of obect number 1',
            text=u'Object 1 some footext.',
        )
        self.obj1 = self.portal['obj1']
        transaction.commit()

    def test_content_core_view(self):
        self.browser.open(self.obj1.absolute_url() + '/@@content-core')

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)
        self.assertIn(self.obj1.text, self.browser.contents)

    def test_version_view(self):
        self.browser.open(
            self.obj1.absolute_url() + '/@@version-view?version_id=0')

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)
        self.assertIn(self.obj1.text, self.browser.contents)

    def test_versions_history_form_should_work_with_dexterity_content(self):
        old_text = self.obj1.text
        old_title = self.obj1.title

        new_text = 'Some other text for object 1.'
        new_title = 'My special new title for object 1'

        self.browser.open(self.obj1.absolute_url() + '/edit')
        self.browser.getControl(label='Title').value = new_title
        self.browser.getControl(label='Text').value = new_text
        self.browser.getControl(name='form.buttons.save').click()

        self._assert_versions_history_form(
            0, self.obj1.getId(), old_title, old_text)
        self._assert_versions_history_form(
            1, self.obj1.getId(), new_title, new_text)

    def _assert_versions_history_form(self, version_id, obj_id, title, text):
        self.browser.open(
            '%s/%s/versions_history_form?version_id=%s'
            % (self.portal_url, obj_id, version_id))
        self.assertIn('Working Copy', self.browser.contents)

        if version_id == 0:
            self.assertIn(
                '/%s/versions_history_form?version_id=%s' % (obj_id, version_id),
                self.browser.contents)
        self.assertIn('Working Copy', self.browser.contents)
        self.assertIn('Revert to this revision', self.browser.contents)
        self.assertIn(
            '/%s/@@history?one' % obj_id, self.browser.contents)
        self.assertIn('Preview of Revision %s' % version_id,
                      self.browser.contents)
        self.assertIn('<h1 class="documentFirstHeading">%s</h1>' % str(title),
                      self.browser.contents)
        self.assertIn(str(text), self.browser.contents)
