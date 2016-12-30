Changelog
=========

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
