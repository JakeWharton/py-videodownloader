__license__ = '''
Copyright 2010 Jake Wharton

rcdict is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

rcdict is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General
Public License along with rcdict.  If not, see
<http://www.gnu.org/licenses/>.
'''

from providers import Provider
import re

class Vimeo(Provider):
  def __init__(self, id, **kwargs):
    Provider.__init__(self, id, **kwargs)

    self.format = kwargs.pop('format', 'hd')
    self.debug('Vimeo', '__init__', 'format', self.format)


  def get_title(self):
    match = re.search(r'<caption>(.+)<\/caption>', self.html)
    if match:
      title = match.group(1).decode('utf-8')
    else:
      title = Provider.get_title(self)
    self.debug('Vimeo', 'get_title', 'title', title)
    return title

  def get_filename(self):
    filename = "%s.%s" % (self.get_title(), self.extension)
    self.debug('Vimeo', 'get_filename', 'filename', filename)
    return filename

  def download_callback(self, url):
    self.extension = re.search(r'(mp4|flv)', url.geturl()).group(1)
    self.debug('Vimeo', 'download_callback', 'extension', self.extension)

  def get_data_url(self):
    url = 'http://vimeo.com/moogaloop/load/clip:%s' % self.id
    self.debug('Vimeo', 'get_data_url', 'url', url)
    return url

  def get_download_url(self):
    url = 'http://vimeo.com/moogaloop/play/clip:%s/%s/%s/?q=%s' % (self.id, self._get_signature(), self._get_signature_expiration(), self.format)
    self.debug('Vimeo', 'get_download_url', 'url', url)
    return url


  def _get_signature(self):
    match = re.search(r'<request_signature>(.+)<\/request_signature>', self.html)
    value = match.group(1) if match else None
    self.debug('Vimeo', '_get_signature', 'signature', value)
    return value

  def _get_signature_expiration(self):
    match = re.search (r'<request_signature_expires>(.+)<\/request_signature_expires>', self.html)
    value = match.group(1) if match else None
    self.debug('Vimeo', '_get_signature_expiration', 'expiration', value)
    return value