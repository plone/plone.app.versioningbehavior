Introduction
============

The ``IVersionable`` behavior is used for enabling the CMFEditions functionality
for dexterity contents. It adds a changeNote-field to the edit- and add-forms and
creates a new version when the content is edited, if enabled for the content type.

It's based on *Products.CMFEditions*. For listing the versions of an object use
CMFEdtions' view ``versions_history_form`` or the history viewlet (see default @@view).


Usage
-----

Just use the behavior ``plone.app.versioningbehavior.behaviors.IVersionable`` in
your dexterity content type.

In your *profiles/default/types/YOURTYPE.xml* add the behavior::

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.versioningbehavior.behaviors.IVersionable" />
     </property>

    </object>


The IVersionable behavior just adds versioning support to your content type,
but it does not enable it.
You have to set the "versioning" option in the Plone types control panel
(/@@types-controlpanel) to either "Manual" or "Automatic" for activating
versioning.


More Information
----------------

For more information about how the versioning works see the documentations of
Products.CMFEdtitions:

 * http://pypi.python.org/pypi/Products.CMFEditions
 * http://plone.org/products/cmfeditions/

