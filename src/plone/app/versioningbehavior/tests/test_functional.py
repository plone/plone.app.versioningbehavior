from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.app.versioningbehavior.testing import (
    PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING,
)
from plone.app.versioningbehavior.testing import TEST_CONTENT_TYPE_ID
from plone.testing.zope import Browser

import transaction
import unittest


class FunctionalTestCase(unittest.TestCase):
    layer = PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()

        self.browser = Browser(self.layer["app"])
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization", f"Basic {TEST_USER_NAME}:{TEST_USER_PASSWORD}"
        )

        setRoles(self.portal, TEST_USER_ID, ["Manager", "Member"])
        self.portal.invokeFactory(
            type_name=TEST_CONTENT_TYPE_ID,
            id="obj1",
            title="Object 1 Title",
            description="Description of object number 1",
            text="Object 1 some footext.",
        )
        self.obj1 = self.portal["obj1"]
        transaction.commit()

    def test_content_core_view(self):
        self.browser.open(self.obj1.absolute_url() + "/@@content-core")

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)
        self.assertIn(self.obj1.text, self.browser.contents)

    def test_version_view(self):
        self.browser.open(self.obj1.absolute_url() + "/@@version-view?version_id=0")

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)
        self.assertIn(self.obj1.text, self.browser.contents)

    def test_edit_creates_a_new_version(self):
        # The Classic-UI-only "versions_history_form" rendering is tested
        # in plone.app.layout instead: here we only verify, via the
        # versioning API, that editing created a new version.
        old_text = self.obj1.text

        new_text = "Some other text for object 1."
        new_title = "My special new title for object 1"

        self.browser.open(self.obj1.absolute_url() + "/edit")
        self.browser.getControl(label="Title").value = new_title
        self.browser.getControl(label="Text").value = new_text
        self.browser.getControl(name="form.buttons.save").click()

        portal_archivist = self.portal.portal_archivist
        history = portal_archivist.getHistoryMetadata(self.obj1)
        self.assertEqual(history.getLength(countPurged=False), 2)

        portal_repository = self.portal.portal_repository
        first_version = portal_repository.retrieve(self.obj1, 0).object
        self.assertEqual(first_version.text, old_text)

        second_version = portal_repository.retrieve(self.obj1, 1).object
        self.assertEqual(second_version.text, new_text)
