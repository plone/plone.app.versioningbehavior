from setuptools import setup, find_packages
import os

version = '1.1'

tests_require = [
    'Products.PloneTestCase',
    'plone.namedfile[blobs]',
    ]

setup(name='plone.app.versioningbehavior',
      version=version,
      description='Provides a behavior for using CMFEditions with ' + \
          'dexterity content types',
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Zope2",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity behavior versioning CMFEditions',
      author='Jonas Baumann, 4teamwork GmbH',
      author_email='mailto:dexterity-development@googlegroups.com',
      url='http://plone.org/products/dexterity',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'plone.app.dexterity[relations]',
        'plone.autoform',
        'plone.dexterity',
        'plone.directives.form',
        'plone.namedfile[blobs]',
        'Products.CMFEditions',
        'rwproperty',
        'setuptools',
        'zope.app.container',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
