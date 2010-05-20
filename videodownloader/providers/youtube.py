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
    FORMAT_PRIORITY = ['37', '22', '35', '18', '34', '5']
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

        #Load video meta information
        url  = 'http://youtube.com/get_video_info?video_id=%s' % self.id
        self._debug('YouTube', '__init__', 'Downloading "%s"...' % url)
        self._html = super(YouTube, YouTube)._download(url).read()

        #Get available formats
        self.formats = set()
        for match in re.finditer(r'itag%3D(\d+)', self._html):
            if match.group(1) not in YouTube.FORMATS.keys():
                print 'WARNING: Unknown format "%s" found.'
            self.formats.add(match.group(1))
        self._debug('YouTube', '__init__', 'formats', ', '.join(self.formats))

        #Get video title if not explicitly set
        if self.title is id:
            match = re.search(r'&title=(.+?)$', self._html, re.DOTALL)
            if match:
                self.title = urllib.unquote_plus(match.group(1))
                self._debug('YouTube', '__init__', 'title', self.title)
        self._debug('YouTube', '__init__', 'title', self.title)

        #Get video filename if not explicity set
        self.filename = self.title if self.filename is None else self.filename
        self._debug('YouTube', '__init__', 'filename', self.filename)

        #Get proper file extension if a valid format was supplied
        if self.format is not None and self.format in YouTube.FORMATS.keys():
            self.fileext = YouTube.FORMATS[self.format][-3:].lower()
            self._debug('YouTube', '__init__', 'fileext', self.fileext)

        #Get magic data needed to download
        match = re.search(r'&token=([-_0-9a-zA-Z]+%3D)', self._html)
        self.token = urllib.unquote(match.group(1)) if match else None
        self._debug('YouTube', '__init__', 'token', self.token)

        #Video thumbnail
        match = re.search(r'&thumbnail_url=(.+?)&', self._html)
        self.thumbnail = urllib.unquote(match.group(1)) if match else None
        self._debug('YouTube', '__init__', 'thumbnail', self.thumbnail)

        #Video duration (seconds)
        try:
            match = re.search(r'&length_seconds=(\d+)&', self._html)
            self.duration = int(match.group(1)) if match else -1
        except ValueError:
            #TODO: warn
            self.duration = -1
        self._debug('YouTube', '__init__', 'duration', self.duration)

        #Other YouTube-specific information
        match = re.search(r'&author=(.+?)&', self._html)
        self.author = match.group(1) if match else None
        self._debug('YouTube', '__init__', 'author', self.author)

        match = re.search(r'keywords=(.+?)&', self._html)
        self.keywords = set(urllib.unquote(match.group(1)).split(',')) if match else set([])
        self._debug('YouTube', '__init__', 'keywords', ','.join(self.keywords))

        try:
            match = re.search(r'&avg_rating=(\d\.\d+)&', self._html)
            self.rating = float(match.group(1)) if match else -1.0
        except ValueError:
            #TODO: warn
            self.rating = -1.0
        self._debug('YouTube', '__init__', 'rating', self.rating)


    def get_download_url(self):
        #Validate format
        if self.format is None:
            self.format = self._get_best_format()
        elif self.format not in self.formats:
            raise ValueError('Invalid format "%s". Valid formats are "%s".' % (self.format, '", "'.join(self.formats)))

        #Check extension
        if self.fileext is None or self.fileext == Provider.DEFAULT_EXT:
            self.fileext = YouTube.FORMATS[self.format][-3:].lower()

        url = 'http://youtube.com/get_video?video_id=%s&fmt=%s&t=%s' % (self.id, self.format, self.token)

        self._debug('YouTube', 'get_download_url', 'url', url)
        return url

    def _get_best_format(self):
        for format in YouTube.FORMAT_PRIORITY:
            if format in self.formats:
                self._debug('YouTube', '_get_best_format', 'format', format)
                return format
        raise ValueError('Could not determine the best available format. YouTube has likely changed its page layout. Please contact the author of this script.')