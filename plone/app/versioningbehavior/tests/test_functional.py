#coding=utf8
from plone.app.versioningbehavior import testing
from plone.app.versioningbehavior.testing import (
    TEST_CONTENT_TYPE_ID)
from mechanize import LinkNotFoundError
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase


class FunctionalTestCase(PloneTestCase.FunctionalTestCase):

    layer = testing.package_layer

    def afterSetUp(self):
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser()
        self.browser.handleErrors = False
        self.setRoles(['Manager', 'Member'], PloneTestCase.default_user)
        self.portal.invokeFactory(
            type_name=TEST_CONTENT_TYPE_ID,
            id='obj1',
            title=u'Object 1 Title',
            description=u'Description of obect number 1',
            text=u'Object 1 some footext.',
        )
        self.obj1 = self.portal['obj1']
        self.test_content_type_fti = self.layer.test_content_type_fti

    def _dump_to_file(self):
        f = open('/tmp/a.html', 'w')
        f.write(self.browser.contents)
        f.close()

    def _login_browser(self, userid, password):
        self.browser.open(self.portal_url + '/login_form')
        self.browser.getControl(name='__ac_name').value = userid
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()

    def assertLinkNotExists(self, *args, **kwargs):
        self.assertRaises(
            LinkNotFoundError, self.browser.getLink, *args, **kwargs)

    def assertControlNotExists(self, *args, **kwargs):
        self.assertRaises(
            LookupError, self.browser.getControl, *args, **kwargs)

    def test_content_core_view(self):
        self._login_browser(
            PloneTestCase.default_user, PloneTestCase.default_password)

        self.browser.open(self.obj1.absolute_url() + '/@@content-core')

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)
        self.assertIn(self.obj1.text, self.browser.contents)

    def test_version_view(self):
        self._login_browser(
            PloneTestCase.default_user, PloneTestCase.default_password)

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

        self._login_browser(
            PloneTestCase.default_user, PloneTestCase.default_password)
        self.browser.open(self.obj1.absolute_url() + '/edit')
        self.browser.getControl(label='Title').value = new_title
        self.browser.getControl(label='Text').value = new_text
        self.browser.getControl(name='form.buttons.save').click()

        self._assert_versions_history_form(
            0, self.obj1.getId(), old_title, old_text)
        self._assert_versions_history_form(
            1, self.obj1.getId(), new_title, new_text)

    def test_versions_history_form_should_work_with_archetypes_content(self):
        old_text = self.obj1.text
        old_title = self.obj1.title

        new_text = 'Some other text for page 1.'
        new_title = 'My special new title for page 1'

        self.portal.invokeFactory(
            type_name='Document',
            id='page1',
            title=old_title,
            text=old_text,
        )
        page = self.portal['page1']

        self._login_browser(
            PloneTestCase.default_user, PloneTestCase.default_password)

        self.browser.open(page.absolute_url() + '/edit')
        self.browser.getControl(label='Title').value = new_title
        self.browser.getControl(label='Body Text').value = new_text
        self.browser.getControl(name='form.button.save').click()

        self._assert_versions_history_form(
            0, page.getId(), old_title, old_text)
        self._assert_versions_history_form(
            1, page.getId(), new_title, new_text)

    def _assert_versions_history_form(self, version_id, obj_id, title, text):
        self.browser.open(
            '%s/%s/versions_history_form?version_id=%s'
            % (self.portal_url, obj_id, version_id))
        self.assertIn('Working Copy', self.browser.contents)
        self.assertIn(
            '/%s/versions_history_form?version_id=%s' % (obj_id, version_id),
            self.browser.contents)
        self.assertIn('Working Copy', self.browser.contents)
        self.assertIn('Revert to this revision', self.browser.contents)
        self.assertIn(
            '/%s/version_diff?version_id1' % obj_id, self.browser.contents)
        self.assertIn('Preview of Revision %s' % version_id,
                      self.browser.contents)
        self.assertIn('<h1 class="documentFirstHeading">%s</h1>' % str(title),
                      self.browser.contents)
        self.assertIn(str(text), self.browser.contents)
