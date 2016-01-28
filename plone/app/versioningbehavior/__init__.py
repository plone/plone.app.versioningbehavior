# -*- coding: utf-8 -*-
from plone.namedfile.interfaces import HAVE_BLOBS
from Products.CMFCore.permissions import ManagePortal

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('plone')


def initialize(context):
    """Registers modifiers with zope (on zope startup).
    """
    if HAVE_BLOBS:
        from modifiers import modifiers

        for m in modifiers:
            context.registerClass(
                m['wrapper'], m['id'],
                permission=ManagePortal,
                constructors=(m['form'], m['factory']),
                icon=m['icon'],
            )
