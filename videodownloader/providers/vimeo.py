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
        xml = ElementTree.fromstring(super(Vimeo, Vimeo)._download(url).read())

        #Get available formats
        self.formats = set(['sd'])
        if xml.findtext('video/isHD', '0') == '1':
            self.formats.add('hd')

        #Get video title and filename if not explicitly set
        if self.title is id:
            self.title = xml.findtext('video/caption', self.title)
        self.filename = self.title if self.filename is None else self.filename

        #Get magic data needed to download
        self.request_signature  = xml.findtext('request_signature', None)
        self.request_expiration = xml.findtext('request_signature_expires', None)

        #Other Vimeo-specific information
        self.height = xml.findtext('video/height', None)
        self.width  = xml.findtext('video/width', None)
        self.thumbnail = xml.findtext('video/thumbnail', None)
        self.duration  = xml.findtext('video/duration', None)
        self.likes = xml.findtext('video/totalLikes', None)
        self.plays = xml.findtext('video/totalPlays', None)
        self.comments = xml.findtext('video/totalComments', None)
        self.uploader = xml.findtext('video/uploader_display_name', None)
        self.url = xml.findtext('video/url_clean', None)

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