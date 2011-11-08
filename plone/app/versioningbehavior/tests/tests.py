import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import plone.app.dexterity
import plone.app.versioningbehavior
import Products.CMFEditions


@onsetup
def setup_product():
    zcml.load_config('meta.zcml', plone.app.dexterity)
    zcml.load_config('configure.zcml', plone.app.dexterity)
    zcml.load_config('configure.zcml', plone.app.versioningbehavior)
    zcml.load_config('configure.zcml', Products.CMFEditions)

setup_product()
ptc.setupPloneSite(extension_profiles=['plone.app.dexterity:default',
                                       'Products.CMFEditions:CMFEditions'])

doc_tests = (
)

functional_tests = (
    'doctest_behavior.txt',
)


def test_suite():
    return unittest.TestSuite(
        [ztc.FunctionalDocFileSuite(
            'tests/%s' % f, package='plone.app.versioningbehavior',
            test_class=ptc.FunctionalTestCase)
            for f in functional_tests] +
        [ztc.ZopeDocFileSuite(
            'tests/%s' % f, package='plone.app.versioningbehavior',
            test_class=ptc.FunctionalTestCase)
            for f in doc_tests],
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
