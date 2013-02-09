import unittest

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from plone.app.versioningbehavior import testing


def test_suite():
    functional = ztc.FunctionalDocFileSuite(
        'tests/doctest_behavior.txt',
        package='plone.app.versioningbehavior',
        test_class=ptc.FunctionalTestCase)
    functional.layer = testing.package_layer
    return unittest.TestSuite([functional])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
