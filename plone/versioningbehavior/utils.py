
from zope.annotation.interfaces import IAnnotations

def get_change_note(request, default=None):
    """
    Returns the changeNote submitted with this request. The changeNote
    is read from the form-field (see behaviors.IVersionable)
    """
    annotations = IAnnotations(request)
    _marker = object()
    value = annotations.get('plone.versioningbehavior-changeNote', _marker)
    if not value or value==_marker:
        return default
    return value
