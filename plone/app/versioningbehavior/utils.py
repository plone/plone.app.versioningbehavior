# -*- coding: utf-8 -*-
from zope.annotation.interfaces import IAnnotations
from zope.publisher.interfaces.browser import IBrowserRequest


def get_change_note(request, default=None):
    """Returns the changeNote submitted with this request. The changeNote
    is read from the form-field (see behaviors.IVersionable)
    """

    _marker = object()

    value = _marker
    if IBrowserRequest.providedBy(request):
        annotations = IAnnotations(request)
        value = annotations.get(
            'plone.app.versioningbehavior-changeNote', _marker)

    if not value or value == _marker:
        return default

    return value
