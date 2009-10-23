
from Acquisition import aq_base
from five import grok
from zope.app.container.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr

from Products.CMFEditions.interfaces.IModifier import FileTooLargeToVersionError
from Products.CMFEditions.interfaces.IArchivist import ArchivistUnregisteredError

from plone.versioningbehavior import MessageFactory as _
from plone.versioningbehavior.behaviors import IVersioningSupport
from plone.versioningbehavior.utils import get_change_note

@grok.subscribe(IVersioningSupport, IObjectModifiedEvent)
def create_version_on_save(context, event):
    """ event handler for creating a new version of the object after
    modifying.
    """
    # according to Products.CMFEditions' update_version_on_edit script
    changeNote = get_change_note(context.REQUEST, None)
    pr = getToolByName(context, 'portal_repository')
    putils = getToolByName(context, 'plone_utils')
    isVersionable = pr.isVersionable(context)

    changed = False
    if not base_hasattr(context, 'version_id'):
        changed = True
    else:
        changed = not pr.isUpToDate(context, context.version_id)

    if isVersionable and ((changed and \
                           pr.supportsPolicy(context, 'at_edit_autoversion')) or \
                          changeNote):
        pr.save(obj=context, comment=changeNote)
    return


@grok.subscribe(IVersioningSupport, IObjectAddedEvent)
def create_initial_version_after_adding(context, event):
    if context.portal_factory.isTemporary(context):
        # don't do anything if we're in the factory
        return
    pr = context.portal_repository
    isVersionable = pr.isVersionable(context)
    comment_field_name = 'form.widgets.IVersionable.changeNote'

    default_changeNote = _(u'initial_version_changeNote', default=u'Initial version')
    changeNote = get_change_note(context.REQUEST, default_changeNote)

    changed = False
    if not base_hasattr(context, 'version_id'):
        changed = True
    else:
        try:
            changed = not pr.isUpToDate(context, context.version_id)
        except ArchivistUnregisteredError:
            # XXX: The object is not actually registered, but a version is
            # set, perhaps it was imported, or versioning info was
            # inappropriately destroyed
            changed = True
    if not changed:
        return
    if pr.supportsPolicy(context, 'at_edit_autoversion') and isVersionable:
        try:
            context.portal_repository.save(obj=context, comment=changeNote)
        except FileTooLargeToVersionError:
            pass # the on edit save will emit a warning
    return



