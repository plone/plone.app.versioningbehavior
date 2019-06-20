# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.versioningbehavior.testing import \
    PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

import unittest


class TestSubscribers(unittest.TestCase):

    layer = PLONE_APP_VERSIONINGBEHAVIOR_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        # we need to have the Manager role to be able to add things
        # to the portal root
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal.invokeFactory("Document", "foo", title="Document")
        self.doc = self.portal.foo

    def test_create_initial_version_after_adding(self):
        pr = getToolByName(self.portal, "portal_repository")
        version_data = pr.retrieve(self.doc)
        self.assertEqual(version_data.comment.default, "Initial version")
        self.assertEqual(version_data.version_id, 0)

    def test_create_version_on_save(self):
        self.doc.title = "Edited document"
        notify(ObjectModifiedEvent(self.doc))
        pr = getToolByName(self.portal, "portal_repository")
        version_data = pr.retrieve(self.doc)
        self.assertIsNone(version_data.comment)
        self.assertEqual(version_data.version_id, 1)
