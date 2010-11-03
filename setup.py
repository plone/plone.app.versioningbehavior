from setuptools import setup, find_packages
import os

version = open('plone/versioningbehavior/version.txt').read().strip()

setup(name='plone.versioningbehavior',
      version=version,
      description="Provides a behavior for using CMFEditions with dexterity content types",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity behavior versioning CMFEditions',
      author='Jonas Baumann',
      author_email='mailto:dexterity-development@googlegroups.com',
      url='http://plone.org/products/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFEditions',
          'five.grok',
          'plone.dexterity',
          'plone.directives.form',
          'rwproperty',
          'plone.autoform',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
