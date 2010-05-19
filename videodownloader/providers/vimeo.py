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
from xml.etree import ElementTree
import re

class Vimeo(Provider):
    FORMAT_PRIORITY = ['hd', 'sd']
    FORMATS = {
        'sd': '640x360 H.264/AAC Stereo MP4',
        'hd': '1280x720 H.264/AAC Stereo MP4',
    }

    def __init__(self, id, **kwargs):
        super(Vimeo, self).__init__(id, **kwargs)

        #Load video meta information
        url = 'http://vimeo.com/moogaloop/load/clip:%s' % self.id
        self._debug('Vimeo', '__init__', 'Downloading "%s"...' % url)
        self._xml = ElementTree.fromstring(super(Vimeo, Vimeo)._download(url).read())

        #Get available formats
        self.formats = set(['sd'])
        if self._xml.findtext('video/isHD', '0') == '1':
            self.formats.add('hd')
        self._debug('Vimeo', '__init__', 'formats', ', '.join(self.formats))

        #Get video title if not explicitly set
        if self.title is id:
            self.title = self._xml.findtext('video/caption', self.title)
        self._debug('Vimeo', '__init__', 'title', self.title)

        #Get video filename if not explicity set
        self.filename = self.title if self.filename is None else self.filename
        self._debug('Vimeo', '__init__', 'filename', self.filename)

        #Get magic data needed to download
        self.request_signature  = self._xml.findtext('request_signature', None)
        self._debug('Vimeo', '__init__', 'request_signature', self.request_signature)
        self.request_expiration = self._xml.findtext('request_signature_expires', None)
        self._debug('Vimeo', '__init__', 'request_expiration', self.request_expiration)

        #Video thumbnail
        self.thumbnail = self._xml.findtext('video/thumbnail', None)
        self._debug('Vimeo', '__init__', 'thumbnail', self.thumbnail)

        #Video duration (seconds)
        try:
            self.duration  = int(self._xml.findtext('video/duration', -1))
        except ValueError:
            #TODO: warn
            self.duration = -1
        self._debug('Vimeo', '__init__', 'duration', self.duration)

        #Other Vimeo-specific information:
        self.uploader = self._xml.findtext('video/uploader_display_name', None)
        self._debug('Vimeo', '__init__', 'uploader', self.uploader)

        self.url = self._xml.findtext('video/url_clean', None)
        self._debug('Vimeo', '__init__', 'url', self.url)

        try:
            self.height = int(self._xml.findtext('video/height', -1))
        except ValueError:
            #TODO: warn
            self.height = -1
        self._debug('Vimeo', '__init__', 'height', self.height)

        try:
            self.width  = int(self._xml.findtext('video/width', -1))
        except ValueError:
            #TODO: warn
            self.width = -1
        self._debug('Vimeo', '__init__', 'width', self.width)

        try:
            self.likes = int(self._xml.findtext('video/totalLikes', -1))
        except ValueError:
            #TODO: warn
            self.likes = -1
        self._debug('Vimeo', '__init__', 'likes', self.likes)

        try:
            self.plays = int(self._xml.findtext('video/totalPlays', -1))
        except ValueError:
            #TODO: warn
            self.plays = -1
        self._debug('Vimeo', '__init__', 'plays', self.plays)

        try:
            self.comments = int(self._xml.findtext('video/totalComments', -1))
        except ValueError:
            #TODO: warn
            self.comments = -1
        self._debug('Vimeo', '__init__', 'comments', self.comments)

    def get_download_url(self):
        #Validate format
        if self.format is None:
            self.format = self._get_best_format()
        elif self.format not in self.formats:
            raise ValueError('Invalid format "%s". Valid formats are "%s".' % (self.format, '", "'.join(self.formats)))

        url = 'http://vimeo.com/moogaloop/play/clip:%s/%s/%s/' % (self.id, self.request_signature, self.request_expiration)
        if self.format != 'sd':
            url += '?q=%s' % self.format

        self._debug('Vimeo', 'get_download_url', 'url', url)
        return url

    def _get_best_format(self):
        for format in Vimeo.FORMAT_PRIORITY:
            if format in self.formats:
                self._debug('Vimeo', '_get_best_format', 'format', format)
                return format
        raise ValueError('Could not determine the best available format. Vimeo has likely changed its page layout. Please contact the author of this script.')

    def _in_download(self, url):
        self.fileext = re.search(r'(mp4|flv)', url.geturl()).group(1)
        self._debug('Vimeo', '_in_download', 'fileext', self.fileext)