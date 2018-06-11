# -*- coding: utf-8 -*-
"""Tests for the `browser` module."""
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_ROLES
from plone.app.versioningbehavior import browser
from plone.app.versioningbehavior.testing import PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING
from plone.app.versioningbehavior.testing import TEST_CONTENT_TYPE_ID
from plone.namedfile import NamedBlobFile
from zope.component import getMultiAdapter

import re
import unittest


class BaseViewTestCase(unittest.TestCase):

    layer = PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, TEST_USER_ROLES + ['Manager'])
        self.portal.invokeFactory(
            type_name=TEST_CONTENT_TYPE_ID,
            id='obj1',
            title=u'Object 1 Title',
            description=u'Description of obect number 1',
            text=u'Object 1 some footext.',
            file=NamedBlobFile(filename=u'object_1_file.txt', data='Object 1 Data'),
        )
        self.obj1 = self.portal['obj1']

    def _render_view(self, view, url=None, params=None):
        if url:
            self.request.set('ACTUAL_URL', url)
            self.request.set('URL', url)

        self.request.form.clear()
        self.request.form.update(params or {})
        return view()


class VersionViewTestCase(BaseViewTestCase):
    """Tests for the `VersionView` view."""

    def test_version_view_is_registered(self):
        obj = self.obj1
        view = getMultiAdapter((obj, self.request), name='version-view')
        self.assertIsInstance(view, browser.VersionView)

    def test_convert_download_links(self):
        """Tests for the `_get_download_version_link` method."""
        obj = self.obj1
        view = browser.VersionView(obj, self.request)
        href_template = u'<a href="{}" />'

        def _assert(old_path, version, field=None, filename=None):
            old_url = obj.absolute_url() + old_path
            old = href_template.format(old_url)
            new = view._convert_download_links(old, version)
            correct_url = view._get_download_version_link(
                version_id=version,
                field_id=field,
                filename=filename,
            )
            correct = href_template.format(correct_url)
            self.assertEqual(new, correct)

        _assert(
            '/@@download/my_field/my_file.txt',
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/versions_history_form/++widget++form.widgets.my_interface.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/versions_history_form/++widget++form.widgets.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/++widget++form.widgets.my_interface.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/++widget++form.widgets.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/my-view/++widget++form.widgets.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            (
                '/@@my-view/++widget++form.widgets.my_field'
                '/@@download/my_file.txt'
            ),
            version='my_version',
            field='my_field',
            filename='my_file.txt',
        )

        _assert(
            '/@@images/abde-01fa.png',
            version='my_version',
        )

    def test_get_download_version_link(self):
        """Tests for the `_get_download_version_link` method."""
        obj = self.obj1
        view = browser.VersionView(obj, self.request)

        def _assert(version, correct_path, field=None, filename=None):
            actual = view._get_download_version_link(
                version_id=version,
                field_id=field,
                filename=filename,
            )
            correct_url = obj.absolute_url() + '/' + correct_path
            self.assertEqual(actual, correct_url)

        _assert(
            version='my_version',
            field='my_field',
            filename='my_file.txt',
            correct_path=(
                '@@download-version?'
                'version_id=my_version&field_id=my_field&filename=my_file.txt'
            ),
        )
        _assert(
            version='my_version',
            filename='my_file.txt',
            correct_path='@@download-version?version_id=my_version&filename=my_file.txt',
        )
        _assert(
            version='my_version',
            field='my_field',
            correct_path='@@download-version?version_id=my_version&field_id=my_field',
        )
        _assert(
            version='my_version',
            correct_path='@@download-version?version_id=my_version',
        )

    def test_call(self):
        """Tests for the `__call__` method."""
        obj = self.obj1
        view = browser.VersionView(obj, self.request)

        html = self._render_view(view=obj, url=obj.absolute_url())
        download_url_pattern = re.compile(
            obj.absolute_url() +
            r'(/[@A-Za-z0-9-_]+)?/' +  # View name can be present or not.
            r'\+\+widget\+\+form\.widgets\.file/@@download/' +
            obj.file.filename
        )
        self.assertTrue(download_url_pattern.search(html))

        html = self._render_view(view=view, url=obj.absolute_url(), params={'version_id': '0'})
        download_url = '{}/@@download-version?version_id=0&field_id=file&filename={}'.format(
            obj.absolute_url(),
            obj.file.filename,
        )
        self.assertTrue(download_url in html)


class DownloadViewTestCase(BaseViewTestCase):
    """Tests for the `VersionView` view."""

    def test_should_download_file_correctly(self):
        obj = self.obj1
        view = browser.DownloadVersion(obj, self.request)

        # We're not passing the field name, the view has to find out which is the primary field.
        data = self._render_view(
            view,
            url=obj.absolute_url(),
            params={'version_id': '0', 'do_not_stream': '1'})
        self.assertTrue(data)
        self.assertEqual(obj.file.data, data)

        # Now we pass field name and filename.
        data = self._render_view(
            view,
            url=obj.absolute_url(),
            params={
                'version_id': '0',
                'do_not_stream': '1',
                'field': 'file',
                'filename': 'some_file_name.bin',
            }
        )
        self.assertTrue(data)
        self.assertEqual(obj.file.data, data)
        self.assertTrue(
            'some_file_name.bin' in self.request.response.headers['content-disposition']
        )
