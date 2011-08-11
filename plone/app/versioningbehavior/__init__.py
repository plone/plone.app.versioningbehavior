import zope.i18nmessageid

MessageFactory = zope.i18nmessageid.MessageFactory("plone.app.versioningbehavior")

from Products.CMFCore.permissions import ManagePortal
from plone.namedfile.interfaces import HAVE_BLOBS

    
def initialize(context):
    """Registers modifiers with zope (on zope startup).
    """
    if HAVE_BLOBS:
        from modifiers import modifiers
    
        for m in modifiers:
            context.registerClass(
                m['wrapper'], m['id'],
                permission = ManagePortal,
                constructors = (m['form'], m['factory']),
                icon = m['icon'],
            )
