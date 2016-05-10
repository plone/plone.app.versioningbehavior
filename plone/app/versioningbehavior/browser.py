# -*- coding: utf-8 -*-
from plone.namedfile.utils import set_headers, stream_data
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.publisher.interfaces import NotFound
import re
from plone.rfc822.interfaces import IPrimaryFieldInfo
from urllib import urlencode


class VersionView(object):
    """Renders the content-core slot of a version of a content item.

    Currently it works by rendering the @@content-core view of the item and then converting the
    links that points to files and images to use the @@download-version view.

    Request parameters:

    version_id -- Version ID.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    _download_url_patterns = (
        # Example: ++widget++form.widgets.my_field/@@download/my_file.txt
        # Example: ++widget++form.widgets.my_interface.my_field/@@download/my_file.txt
        # Example: view-name/++widget++form.widgets.my_field/@@download/my_file.txt
        (
            r'([@a-zA-Z0-9_-]+/)?'
            r'\+\+widget\+\+form\.widgets\.([a-zA-Z0-9_-]+\.)?(?P<field_id>[a-zA-Z0-9_-]+)'
            r'/@@download/(?P<filename>[^"\']+)'
        ),

        # Example: @@download/my_field/my_file.txt
        r'@@download/(?P<field_id>[a-zA-Z0-9_-]+)/(?P<filename>[^"\']+)',

        # Example: @@images/aedf-0123.png
        r'@@images/[0-9a-f\-]+\.[a-z]+',
    )

    def __call__(self):
        version_id = self.request.get('version_id', None)
        if not version_id:
            raise ValueError(u'Missing parameter on the request: version_id')

        content_core_view = getMultiAdapter((self.context, self.request), name='content-core')
        html = content_core_view()
        return self._convert_download_links(html, version_id)

    def _convert_download_links(self, html, version_id):
        transformed_html = html

        def repl(match):
            groups = match.groupdict()
            return self._get_download_version_link(
                version_id=version_id,
                field_id=groups.get('field_id'),
                filename=groups.get('filename'),
            )

        context_url = self.context.absolute_url()
        for pattern in self._download_url_patterns:
            compiled_pattern = re.compile(context_url + '/' + pattern)
            transformed_html = compiled_pattern.sub(repl, transformed_html)

        return transformed_html

    def _get_download_version_link(self, version_id, field_id=None, filename=None):
        parameters = [('version_id', version_id)]

        if field_id:
            parameters.append(('field_id', field_id))

        if filename:
            parameters.append(('filename', filename))

        query_string = urlencode(parameters)
        return '{}/@@download-version?{}'.format(self.context.absolute_url(), query_string)


class DownloadVersion(object):
    """Downloads a file in a field of a content item at an specific version.


    Request parameters:

    version_id -- Version ID.
    field_id -- (optional) ID of the field (eg.: "file" or "image"). If ommited then the
                primary field will be used.
    filename -- (optional) Filename. If ommited then the filename HTTP header won't be set on the
                response, but the download will occur normally.
    do_not_stream -- (optional) Do not stream the file.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        version_id = self.request.get('version_id', None)
        if not version_id:
            raise ValueError(u'Missing parameter on the request: version_id')

        field_id = self.request.get('field_id', IPrimaryFieldInfo(self.context).fieldname)
        filename = self.request.get('filename')
        do_not_stream = self.request.get('do_not_stream')

        repository = getToolByName(self.context, 'portal_repository')
        old_obj = repository.retrieve(self.context, version_id).object

        # Will only work if the file is stored as an attribute with the same
        # name of the field.
        file_ = getattr(old_obj, field_id, None)

        if file_ is None:
            raise NotFound(self, filename, self.request)

        set_headers(file_, self.request.response, filename=filename)

        if do_not_stream:
            return file_.data

        return stream_data(file_)
