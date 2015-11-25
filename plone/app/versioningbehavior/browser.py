# -*- coding: utf-8 -*-
from plone.namedfile.utils import set_headers, stream_data
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.publisher.interfaces import NotFound

import re


class VersionView(object):

    download_url_patterns = (
        re.compile(r'/@@download/(?P<field_id>.*?)/(?P<filename>.*?)"'),

        # Behavior name before field name, like "LeadImage.image"
        re.compile(
            r'/versions_history_form/'
            r'\+\+widget\+\+form\.widgets\.\S+\.(?P<field_id>.*?)'
            r'/@@download/(?P<filename>.*?)"'
        ),

        re.compile(
            r'/versions_history_form/'
            r'\+\+widget\+\+form\.widgets\.(?P<field_id>.*?)'
            r'/@@download/(?P<filename>.*?)"'
        ),
    )

    version_of_namedfile_template = (
        r'/@@download-version?'
        r'field_id=\g<field_id>&filename=\g<filename>&version_id={version_id}"'
    )

    def __call__(self):
        version_id = self.request.version_id
        content_core_view = getMultiAdapter((self.context, self.request), name='content-core')
        html = content_core_view()
        transformed_html = html

        for pattern in self.download_url_patterns:
            repl = self.version_of_namedfile_template.format(version_id=version_id)
            transformed_html = pattern.sub(repl, transformed_html)

        return transformed_html


class DownloadVersion(object):

    def __call__(self):
        version_id = self.request.version_id
        field_id = self.request.field_id
        filename = self.request.filename
        repository = getToolByName(self.context, 'portal_repository')
        old_obj = repository.retrieve(self.context, version_id).object

        # Will only work if the file is stored as an attribute with the same
        # name of the field.
        file_ = getattr(old_obj, field_id, None)

        if file_ is None:
            raise NotFound(self, filename, self.request)

        set_headers(file_, self.request.response, filename=filename)

        return stream_data(file_)
