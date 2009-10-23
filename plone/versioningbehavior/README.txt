
Some Tests
----------

Just use the behavior ``plone.versioningbehavior.behaviors.IVersionable`` in
your dexterity content type::

    >>> from plone.dexterity.fti import DexterityFTI
    >>> fti = DexterityFTI('TestingType')
    >>> fti.behaviors = (
    ...         'plone.versioningbehavior.behaviors.IVersionable',
    ... )
    >>> self.portal.portal_types._setObject('TestingType', fti)
    'TestingType'
    >>> schema = fti.lookupSchema()


We have to setup versioning for this content type by visiting the plone
configuration panel for content types (/@@types-controlpanel) and enable
automatic versioning for our content type.
For this test we set this configuration manually::

    >>> from Products.CMFEditions import CopyModifyMergeRepositoryTool
    >>> pr = self.portal.portal_repository
    >>> pr._versionable_content_types.append('TestingType')
    >>> pr._version_policy_mapping['TestingType'] = [
    ...     'version_on_revert',
    ...     'at_edit_autoversion',
    ... ]


Create a new Browser and connect it::

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False
    >>> self.app.acl_users.userFolderAddUser('root', 'secret', ['Manager'], [])
    >>> browser.addHeader('Authorization', 'Basic root:secret')


Now we should be able to create a new TestingType-object::

    >>> browser.open('http://nohost/plone/folder_factories')
    >>> 'TestingType' in browser.contents
    True
    >>> browser.getControl("TestingType").click()
    >>> browser.getControl("Add").click()
    >>> browser.url
    'http://nohost/plone/++add++TestingType'
    >>> browser.getControl(name='form.widgets.title').value = 'Blubb'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.url
    'http://nohost/plone/testingtype/view'


We should be able to access the object, it should provide the marker
interface ``plone.versioningbehavior.behaviors.IVersioningSupport``::

    >>> obj = self.portal.get('testingtype')
    >>> from plone.versioningbehavior.behaviors import IVersioningSupport
    >>> IVersioningSupport.providedBy(obj)
    True


After creating the object we wan't to create a new version by simply editing it::

    >>> browser.open('http://nohost/plone/testingtype/edit')
    >>> browser.getControl(name='form.widgets.title').value = 'Blubb2'
    >>> field = browser.getControl(name='form.widgets.IVersionable.changeNote')
    >>> field.value = 'just a test'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.url
    'http://nohost/plone/testingtype'


Now we should have at least one version::

    >>> obj = self.portal.get('testingtype')
    >>> pa = self.portal.portal_archivist
    >>> history = pa.getHistoryMetadata(obj)
    >>> history.getLength(countPurged=False) > 0
    True


And we should be able to list the versions::

    >>> browser.open('http://nohost/plone/testingtype/versions_history_form')
    >>> 'just a test' in browser.contents
    True


A freshly created object should have a initial version::

    >>> browser.open('http://nohost/plone/++add++TestingType')
    >>> browser.getControl(name='form.widgets.title').value = 'Init test'
    >>> browser.getControl(name='form.widgets.IVersionable.changeNote') \
    ...     .value = 'initial change note'
    >>> browser.getControl(name='form.buttons.save').click()
    >>> browser.url
    'http://nohost/plone/testingtype-1/view'

Now we should have one - and only one - version::

    >>> obj = self.portal.get('testingtype-1')
    >>> pa = self.portal.portal_archivist
    >>> history = pa.getHistoryMetadata(obj)
    >>> history.getLength(countPurged=False)
    1

And we should see our comment on the versions listing later...
### browser.open('http://nohost/plone/testingtype-1/versions_history_form')
### 'initial change note' in browser.contents
True


