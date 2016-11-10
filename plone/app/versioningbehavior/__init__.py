# -*- coding: utf-8 -*-
from plone.app.versionbehavior.modifiers import modifiers
from Products.CMFCore.permissions import ManagePortal
from zope.i18nmessageid import MessageFactory


_ = MessageFactory('plone')


def initialize(context):
    """Registers modifiers with zope (on zope startup).
    """

    for mod in modifiers:
        context.registerClass(
            mod['wrapper'],
            mod['id'],
            permission=ManagePortal,
            constructors=(mod['form'], mod['factory']),
            icon=mod['icon'],
        )
