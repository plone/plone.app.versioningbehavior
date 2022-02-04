Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

1.4.6 (2022-02-04)
------------------

Bug fixes:


- Removed deprecated `plone.namedfile[blobs]` from the test requirements.
  [maurits] (#106)


1.4.5 (2022-01-28)
------------------

Bug fixes:


- Depend on `plone.namedfile` core instead of its empty `[blobs]` extra.
  [maurits] (#106)


1.4.4 (2021-11-26)
------------------

Bug fixes:


- Fix tests on Python 2 with newer plone.dexterity using repr for the schema.
  [wesleybl] (#60)


1.4.3 (2021-05-03)
------------------

Bug fixes:


- Fix issue where versioning dynamic content types with blob fields broke after a schema update due to change in dynamic schema identifiers since plone.dexterity >= 2.10.0
  [datakurre] (#57)


1.4.2 (2021-02-16)
------------------

Bug fixes:


- Do not break if the portal_repository tool cannot be found (#53)


1.4.1 (2020-07-30)
------------------

Bug fixes:


- Avoid traceback when transforming links on content type with no primary field
  [laulaz] (#51)


1.4.0 (2020-04-30)
------------------

New features:


- Change to use Python's built-in `filecmp.cmp(shallow=False)` to compare blobs for differences instead of the old method of comparing them line by line. [datakurre] (#50)


1.3.9 (2020-04-20)
------------------

Bug fixes:


- Update the documentation that was pointing to the obsolete @@types-controlpanel (it is @@content-controlpanel instead) (#33)


1.3.8 (2019-06-27)
------------------

Bug fixes:


- Initial version for versionable objects is properly created [ale-rt] (#47)


1.3.7 (2019-02-13)
------------------

Bug fixes:


- If a behavior that provides a NamedBlobFile was renamed, we can now still
  find the blob file, provided that the old behavior's dotted name was properly
  registered. [pysailor] (#45)


1.3.6 (2018-12-10)
------------------

Bug fixes:

- Move change notes field to be the last field of the form (just above the buttons).
  https://github.com/plone/Products.CMFPlone/issues/2640
  [gforcada]

1.3.5 (2018-11-02)
------------------

Bug fixes:

- Made writing Blob less aggressive.(issue #42)
  [iham]

- Remove (testing) dependency on zope.app.intid.
  [gforcada]

1.3.4 (2018-09-25)
------------------

Bug fixes:

- Migrate tests away from PloneTestCase
  [pbauer]

- Fix imports for py3
  [pbauer]


1.3.3 (2018-04-03)
------------------

New features:

- Add a field for disabling versions per content item
  https://github.com/plone/Products.CMFPlone/issues/2341
  [tomgross]

Bug fixes:

- Remove obsolete grok usage
  [tomgross]


1.3.2 (2018-02-02)
------------------

Bug fixes:

- Imports are Python3 compatible
  [ale-rt, robbuh]


1.3.1 (2017-06-06)
------------------

Bug fixes:

- Added a missing TTW edit form.
  [Rotonen]


1.3 (2016-12-30)
----------------

New features:

- Add shortname ``plone.versioning`` for behavior.
  [jensens]


1.2.10 (2016-09-23)
-------------------

Bug fixes:

- Do not break in the case of dexterity objects with relations
  migrated from something else (usually Archetypes).
  [ale-rt]


1.2.9 (2016-08-18)
------------------

Bug fixes:

- Use zope.interface decorator.
  [gforcada]


1.2.8 (2016-05-15)
------------------

Fixes:

- Fixes #25: URLs like `${absolute_url}/@@images/${uuid}.png` are not converted
  on `@@version-view`. [rafaelbco]


1.2.7 (2016-02-11)
------------------

New:

- Used plone i18n domain and removed locales folder.  [klinger]

Fixes:

- Updated Traditional Chinese translations.  [l34marr]


1.2.6 (2015-11-28)
------------------

Fixes:

- Update Italian translations
  [ale-rt, cekk]

- Fixes #10: Views for Image and File versions don't work.
  [rafaelbco]


1.2.5 (2015-09-20)
------------------

- Update French translations
  [enclope]


1.2.4 (2015-09-11)
------------------

- Updated basque translation
  [erral]


1.2.3 (2015-07-18)
------------------

- Correct functional test, it was not checking correct on version1.
  [bloodbare]


1.2.2 (2015-05-13)
------------------

- Synchronize translations
  [vincentfretin]

- provide better description of how new versions are created when in manual mode
  [vangheem]


1.2.1 (2015-03-13)
------------------

- Ported tests to plone.app.testing.
  Removed PloneTestCase / p.a.testing compatibility hack.
  [jone]

- Remove dependencies on zope.app.container and rwproperty.
  [davisagli]

- Added Italian translations.
  [cekk]


1.2.0 (2014-09-11)
------------------

- Remove customization of versions_history_form since the changes were ported
  to Products.CMFEditions>2.2.9.
  [rafaelbco]


1.1.4 (2014-08-25)
------------------

- Deal with AttributeError when trying to access fields provided by behaviors
  using attribute storage.
  [lgraf]

- Added Traditional Chinese translations.
  [marr]


1.1.3 (2014-02-26)
------------------

- Include ``*.rst`` files in the release. 1.1.2 was a brown bag release.
  [timo]


1.1.2 (2014-02-26)
------------------

- Remove plone.directives.form dependency since this fetches five.grok, which
  is not allowed in Plone core.
  [timo]


1.1.1 (2013-07-19)
------------------

- Merge Rafael Oliveira's (@rafaelbco) versions_history_form fixes
  from collective.cmfeditionsdexteritycompat.
  [rpatterson]

- danish translation added [tmog]

- Fixed an issue where a clone modifier would cause an incorrect
  pickle due to an implementation detail in CPython's memory
  allocation routine (exposed in Python as the object ``id``).
  [malthe]

- Include grok when grok package is installed.
  This makes sure the ZCML for the `grok` directive is loaded.
  [lgraf]

- For dexterity 1.x compatibility grok the package if grok is installed.
  [jone]

- Added Dutch translations.
  [kingel]

- Fix case where versioning of blobs would cause an error if a
  field was removed from a schema between revisions.
  [mikerhodes]


1.1 (2012-02-20)
----------------

- Added French translations.
  [jone]

- Fixed SkipRelations modifier to also work with behaviors which are storing
  relations in attributes.
  [buchi]

- Added Spanish translation.
  [hvelarde]


1.0 (2011-11-17)
----------------

- Added pt_BR translation.
  [rafaelbco, davisagli]

- Added support for versioning items with relations (plone.app.relationfield).
  Relations are skipped on clone and added from the working copy on restore.
  [buchi]


1.0b7 (2011-10-03)
------------------

* Fixed a bug in the CloneNamedFileBlobs modifier causing an AttributeError
  when the previous version doesn't have a blob and the working copy has one.
  [buchi]


1.0b6 (2011-09-25)
------------------

* Add missing dependency declaration on plone.namedfile[blobs].
  [davisagli]


1.0b5 (2011-09-01)
------------------

* Fixed setuphandler to not fail with older versions of Products.CMFEditions
  that do not have a Skip_z3c_blobfile modifier.
  [buchi]

* Fixed CloneNamedFileBlobs modifier to handle fields with value ``None``.
  [buchi]


1.0b4 (2011-08-11)
------------------

* Added generic setup profile which installs and enables the modifier for
  cloning blobs and disables the Skip_z3c_blobfile modifier.
  [buchi]

* Added support for versioning blobs (NamedBlobFile, NamedBlobImage).
  [buchi]

1.0b3 (2011-03-01)
------------------

* Remove grok usage, tidy up and declare zope.app.container dependency.
  [elro]

* Only version the modified object, not its container on modification.
  [elro]

1.0b2 (2011-01-25)
------------------

* Changed the behavior so that the changeNote field is only
  rendered in the Add and Edit forms.
  [deo]

* Made sure to always try to catch the ArchivistUnregisteredError
  exception at create_version_on_save (this mimics the original
  handling from CMFEditions).
  [deo]


1.0b1 (2010-11-04)
------------------

* Renamed package to `plone.app.versioningbehavior`.
  [jbaumann]

* Load Products.CMFEditions before testing.
  [jbaumann]

* Added some more tests.
  [jbaumann]

* Renamed package to plone.versioningbehavior (see dexterity mailing list).
  [jbaumann]

* Re-enabled IObjectAddedEvent-Eventhandler. The pickling error was fixed in
  CMFEdition's trunk.
  [jbaumann]

* Renamed the behavior marker interface IVersionOnSave to IVersioningSupport
  because it depends on the "version" settings in the types control panel if
  a content is automatically versioning on saving or not. The marker interface
  should only indicate if the type could be versioned or not.
  [jbaumann]

* Added locales directory with own domain for local translations.
  [jbaumann]

* Updated README.txt, included doctests in long-description.
  [jbaumann]

* Updated tests: events and version creation are now tested properly.
  [jbaumann]

* Added helper method for getting the changenote from the request annotation.
  [jbaumann]

* Storing changenote in an annotation on the request between the field-adapter
  and the event handler which creates the version. That makes it possible to
  use different form and widget manager prefixes.
  [jbaumann]

* Added localization for the comment field.
  [jbaumann]

* Disabled the Added-Event because it's not working due to a pickling problem.
  [jbaumann]

* Added a form-field changeNote. It's content is used as comment for the
  created version.
  [jbaumann]

* Added a Event-Handler for creating a new version on save.
  [jbaumann]

* Implemented the behavior plone.behaviors.versioning.behaviors.IVersionable.
  [jbaumann]
