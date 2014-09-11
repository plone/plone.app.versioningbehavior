# -*- coding: utf-8 -*-
from plone.app.versioningbehavior.testing import VERSIONING_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite('doctest_behavior.txt'),
            layer=VERSIONING_FUNCTIONAL_TESTING,
        ),
    ])
    return suite
