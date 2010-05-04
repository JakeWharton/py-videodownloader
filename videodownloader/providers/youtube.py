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
import urllib

class YouTube(Provider):
    DEFAULT = ['37', '22', '35', '18', '34', '5']
    FORMATS = {
        '5' : '320x240 H.263/MP3 Mono FLV',
        '13': '176x144 3GP/AMR Mono 3GP',
        '17': '176x144 3GP/AAC Mono 3GP',
        '18': '480x360/480x270 H.264/AAC Stereo MP4',
        '22': '1280x720 H.264/AAC Stereo MP4',
        '34': '320x240 H.264/AAC Stereo FLV',
        '35': '640x480/640x360 H.264/AAC Stereo FLV',
        '37': '1920x1080 H.264/AAC Stereo MP4',
    }

    def __init__(self, id, **kwargs):
        super(YouTube, self).__init__(id, **kwargs)

        self.format = kwargs.pop('format', None)
        self._html = None
        self._formats = None


    @property
    def html(self):
        if self._html is None:
            self._html = super(YouTube, YouTube)._download(self._get_data_url()).read()
        return self._html

    @property
    def formats(self):
        if self._formats is None:
            self._formats = set()
            for match in re.finditer(r'itag%3D(\d+)', self.html):
                if match.group(1) not in YouTube.FORMATS.keys():
                    print 'WARNING: Unknown format "%s" found.'
                self._formats.add(match.group(1))
            self._debug('YouTube', 'formats', 'formats', ', '.join(self._formats))
        return self._formats


    def get_title(self):
        match = re.search(r'&title=(.+)$', self.html, re.DOTALL)
        if match:
            title = urllib.unquote(match.group(1).replace('+', ' '))
        else:
            title = super(YouTube, self).get_title()

        self._debug('YouTube', 'get_title', 'title', title)
        return title

    def get_filename(self):
        if self.format is None:
            self.format = self._get_best_format()

        if self.format not in YouTube.FORMATS.keys():
            filename = self.get_title() + '.video'
        else:
            #Title + dot + last three letters of the format description lowercased
            filename = self.get_title() + '.' + YouTube.FORMATS[self.format][-3:].lower()

        self._debug('YouTube', 'get_filename', 'filename', filename)
        return filename

    def get_download_url(self):
        if self.format is None:
            self.format = self._get_best_format()
        url = 'http://youtube.com/get_video?video_id=%s&fmt=%s&t=%s' % (self.id, self.format, self._get_token())
        self._debug('YouTube', 'get_download_url', 'url', url)
        return url


    def _get_best_format(self):
        for format in YouTube.DEFAULT:
            if format in self.formats:
                self._debug('YouTube', '_get_best_format', 'format', format)
                return format
        raise ValueError("Could not determine the best available format. YouTube has likely changed its page layout. Please contact the author of this script.")

    def _get_data_url(self):
        url = 'http://youtube.com/get_video_info?video_id=%s' % self.id
        self._debug('YouTube', '_get_data_url', 'url', url)
        return url

    def _get_token(self):
        '''
        Magic method which extracts session token from HTML. Session token needed for video download URL
        '''
        match = re.search(r'&token=([-_0-9a-zA-Z]+%3D)', self.html)
        token = urllib.unquote(match.group(1)) if match else None
        self._debug('YouTube', '_get_token', 'token', token)
        return token
