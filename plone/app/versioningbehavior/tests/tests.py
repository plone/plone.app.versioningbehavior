# -*- coding: utf-8 -*-
from plone.app.versioningbehavior.testing import PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite('doctest_behavior.txt'),
            layer=PLONE_APP_VERSIONINGBEHAVIOR_FUNCTIONAL_TESTING,
        ),
    ])
    return suite
