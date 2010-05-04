__license__ = '''
Copyright 2010 Jake Wharton

py-video-downloader is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

py-video-downloader is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with py-video-downloader.  If not, see
<http://www.gnu.org/licenses/>.
'''

from videodownloader.providers import Provider
import re

class Vimeo(Provider):
    DEFAULT = ['hd', 'sd']
    FORMATS = {
        'sd': '640x360 H.264/AAC Stereo MP4',
        'hd': '1280x720 H.264/AAC Stereo MP4',
    }

    def __init__(self, id, **kwargs):
        super(Vimeo, self).__init__(id, **kwargs)

        self.format = kwargs.pop('format', None)
        self.extension = 'mp4' #Set via download_callback but needs a default
        self._html = None
        self._formats = None


    @property
    def html(self):
        if self._html is None:
            self._html = super(Vimeo, Vimeo)._download(self._get_data_url()).read()
        return self._html

    @property
    def formats(self):
        if self._formats is None:
            self._formats = set(['sd'])
            match = re.search(r'<isHD>(0|1)<\/isHD>', self.html)
            if match and match.group(1) == '1':
                self._formats.add('hd')
        return self._formats


    def get_title(self):
        match = re.search(r'<caption>(.+)<\/caption>', self.html)
        if match:
            title = match.group(1).decode('utf-8')
        else:
            title = super(Vimeo, self).get_title()
        self._debug('Vimeo', 'get_title', 'title', title)
        return title

    def get_filename(self):
        filename = "%s.%s" % (self.get_title(), self.extension)
        self._debug('Vimeo', 'get_filename', 'filename', filename)
        return filename

    def get_download_url(self):
        url = 'http://vimeo.com/moogaloop/play/clip:%s/%s/%s/' % (self.id, self._get_signature(), self._get_signature_expiration())
        if self.format is None:
            self.format = self._get_best_format()
        if self.format != 'sd':
            url += '?q=%s' % self.format
        self._debug('Vimeo', 'get_download_url', 'url', url)
        return url

    def download_callback(self, url):
        self.extension = re.search(r'(mp4|flv)', url.geturl()).group(1)
        self._debug('Vimeo', 'download_callback', 'extension', self.extension)


    def _get_best_format(self):
        for format in Vimeo.DEFAULT:
            if format in self.formats:
                self._debug('Vimeo', '_get_best_format', 'format', format)
                return format
        raise ValueError("Could not determine the best available format. Vimeo has likely changed its page layout. Please contact the author of this script.")

    def _get_data_url(self):
        url = 'http://vimeo.com/moogaloop/load/clip:%s' % self.id
        self._debug('Vimeo', 'get_data_url', 'url', url)
        return url

    def _get_signature(self):
        match = re.search(r'<request_signature>(.+)<\/request_signature>', self.html)
        value = match.group(1) if match else None
        self._debug('Vimeo', '_get_signature', 'signature', value)
        return value

    def _get_signature_expiration(self):
        match = re.search(r'<request_signature_expires>(.+)<\/request_signature_expires>', self.html)
        value = match.group(1) if match else None
        self._debug('Vimeo', '_get_signature_expiration', 'expiration', value)
        return value
