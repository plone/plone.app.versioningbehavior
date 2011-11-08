from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.interfaces.IModifier import IConditionalTalesModifier
from plone.app.versioningbehavior.modifiers import modifiers


def install_modifiers(context, logger):
    portal_modifier = getToolByName(context, 'portal_modifier')
    for m in modifiers:
        id_ = m['id']
        if id_ in portal_modifier.objectIds():
            continue
        title = m['title']
        modifier = m['modifier'](id_, title)
        wrapper = m['wrapper'](id_, modifier, title)
        enabled = m['enabled']
        if IConditionalTalesModifier.providedBy(wrapper):
            wrapper.edit(enabled, m['condition'])
        else:
            wrapper.edit(enabled)
        portal_modifier.register(m['id'], wrapper)


def disable_skip_z3c_blobfile(context, logger):
    portal_modifier = getToolByName(context, 'portal_modifier')
    if 'Skip_z3c_blobfile' in portal_modifier.objectIds():
        modifier = portal_modifier.get('Skip_z3c_blobfile')
        modifier.edit(enabled=False)


def import_various(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile(
        'plone.app.versioningbehavior_various.txt') is None:
        return

    logger = context.getLogger('plone.app.versioningbehavior')
    site = context.getSite()
    install_modifiers(site, logger)
    disable_skip_z3c_blobfile(site, logger)
