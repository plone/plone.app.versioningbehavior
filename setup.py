from pathlib import Path
from setuptools import find_packages
from setuptools import setup


version = "2.0.4"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

tests_require = [
    "plone.app.contenttypes[test]",
    "plone.app.robotframework",
    "plone.app.testing",
    "plone.protect",
    "plone.testing",
    "Products.CMFDiffTool",
    "Products.CMFEditions [test]",
    "zope.intid",
]

setup(
    name="plone.app.versioningbehavior",
    version=version,
    description=(
        "Provides a behavior for using CMFEditions with dexterity content types"
    ),
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone dexterity behavior versioning CMFEditions",
    author="Jonas Baumann, 4teamwork GmbH",
    author_email="mailto:dexterity-development@googlegroups.com",
    url="http://plone.org/products/dexterity",
    license="GPL version 2",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "plone.app.dexterity[relations]",
        "plone.autoform",
        "plone.base",
        "plone.behavior>=1.1",
        "plone.dexterity",
        "plone.namedfile",
        "plone.rfc822",
        "plone.supermodel",
        "Products.CMFEditions>2.2.9",
        "Products.GenericSetup",
        "setuptools",
        "z3c.form",
        "z3c.relationfield",
        "Zope",
    ],
    extras_require=dict(tests=tests_require),
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
