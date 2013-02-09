from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
from Products.CMFCore.utils import getToolByName
import re
from zope.component import getMultiAdapter


class VersionView(object):

    def __call__(self):
        version_id = self.request.version_id
        content_core_view = getMultiAdapter((self.context, self.request), name='content-core')
        html = content_core_view()
        return re.sub(
            r'''/@@download/(?P<field_id>.*?)/(?P<filename>.*?)"''',
            r'''/@@download-version?field_id=\g<field_id>&filename=\g<filename>&version_id=''' + version_id + '"',
            html
        )

class DownloadVersion(object):

    def __call__(self):
        version_id = self.request.version_id
        field_id = self.request.field_id
        filename = self.request.filename
        repository = getToolByName(self.context, 'portal_repository')
        old_obj = repository.retrieve(self.context, version_id).object
        file_ = getattr(old_obj, field_id)

        if file_ is None:
            raise NotFound(self, filename, self.request)
        
        set_headers(file_, self.request.response, filename=filename)

        return stream_data(file_)

