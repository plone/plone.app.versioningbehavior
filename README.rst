Introduction
============

The ``IVersionable`` behavior is used for enabling the CMFEditions functionality for dexterity contents.
It adds a changeNote-field to the edit- and add-forms and creates a new version when the content is edited, if enabled for the content type.

It's based on *Products.CMFEditions*.
For listing the versions of an object use CMFEdtions' view ``versions_history_form`` or the history viewlet (see default @@view).


Usage
-----

Just use the behavior ``plone.app.versioningbehavior.behaviors.IVersionable`` in your dexterity content type.

In your *profiles/default/types/YOURTYPE.xml* add the behavior ``plone.versionable``::

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.versioning" />
     </property>

    </object>


The ``IVersionable`` behavior just adds versioning support to your content type,
but it does not enable it.

You have to set the "versioning" option in the Plone types control panel (/@@types-controlpanel) to either "Manual" or "Automatic" for activating versioning.

If you want to automatically enable versioning for your custom content types through generic setup you have to create a file "repositorytool.xml" in your gs profile (e.g. "profiles/default") with the following content::

    <?xml version="1.0"?>
    <repositorytool>
        <policymap>
            <type name="MyType">
                <policy name="at_edit_autoversion"/>
                <policy name="version_on_revert"/>
            </type>
            <type name="AnotherType">
                <policy name="at_edit_autoversion"/>
                <policy name="version_on_revert"/>
            </type>
        </policymap>
    </repositorytool>

See http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-4.0-to-4.1/updating-add-on-products-for-plone-4.1/use-generic-setup-for-defining-versioning-policies for more details.


More Information
----------------

For more information about how the versioning works see the documentation of Products.CMFEditions:

 * http://pypi.python.org/pypi/Products.CMFEditions
 * http://plone.org/products/cmfeditions/

