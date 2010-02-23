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

from providers import Provider
import re

class YouTube(Provider):
  FORMAT = {
    '5' : '320x240 H.263/MP3 Mono FLV',
    '6' : '320x240 H.263/MP3 Mono FLV',
    '13': '176x144 3GP/AMR Mono 3GP',
    '17': '176x144 3GP/AAC Mono 3GP',
    '18': '480x360/480x270 H.264/AAC Stereo MP4',
    '22': '1280x720 H.264/AAC Stereo MP4',
    '34': '320x240 H.264/AAC Stereo FLV',
    '35': '640x480/640x360 H.264/AAC Stereo FLV',
    '37': '1920x1080 H.264/AAC Stereo MP4',
  }

  def __init__(self, id, **kwargs):
    Provider.__init__(self, id, **kwargs)

    self.format = kwargs.pop('format', 35)
    self.debug('YouTube', '__init__', 'format', self.format)


  def get_title(self):
    match = re.search(r'<title>\s*YouTube\s*-\s*(.+)</title>', self.html, re.DOTALL)
    if match:
      title = match.group(1).decode('utf-8').strip()
    else:
      title = Provider.get_title(self)

    self.debug('YouTube', 'get_title', 'title', title)
    return title

  def get_filename(self):
    filename = '%s.mp4' % self.get_title()
    self.debug('YouTube', 'get_filename', 'filename', filename)
    return filename

  def get_data_url(self):
    url = 'http://www.youtube.com/watch?v=%s' % self.id
    self.debug('YouTube', 'get_data_url', 'url', url)
    return url

  def get_download_url(self):
    if str(self.format) not in YouTube.FORMAT.keys():
      raise ValueError('Format code "%s" not found in format list.' % self.format)
    url = 'http://www.youtube.com/get_video.php?video_id=%s&fmt=%s&t=%s' % (self.id, self.format, self._get_token())
    self.debug('YouTube', 'get_download_url', 'url', url)
    return url


  def _get_token(self):
    '''
    Magic method witch extract session token from HTML. Session token needed for video download URL
    '''
    match = re.search(r', "t": "([^&"]+)"', self.html)
    token = match.group(1) if match else None
    self.debug('YouTube', '_get_token', 'token', token)
    return token