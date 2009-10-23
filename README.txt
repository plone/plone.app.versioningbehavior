Introduction
============

The ``IVersionable`` behavior is used for enabling the CMFEditions functionality
for dexterit contents. It adds a changeNote-field to the edit- and add-forms and
creates a new version when the content is edited.

It's based on *Products.CMFEditions*. For listing the versions of a object use
CMFEdtions' view ``versions_history_form``.

Usage
-----

Just use the behavior ``plone.behaviors.versioning.behaviors.IVersionable`` in
your dexterity content type.

In your *profiles/default/types/YOURTYPE.xml* add the behaviour as following::

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     
     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.behaviors.versioning.behaviors.IVersionable" />
     </property>

    </object>


The IVersionable behavior just enables versioning support for your content type,
but it does not activate it.
You have to set the "versioning" option in the Plone types control panel
(/@@types-controlpanel) to either "Manual" or "Automatic" for activating
versioning.

