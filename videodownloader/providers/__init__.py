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

from datetime import datetime
import os
import re
import sys
import urllib2

__all__ = ['Vimeo', 'YouTube']

class Provider(object):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
    }

    def __init__(self, id, **kwargs):
        self.debugging = kwargs.pop('debug', False)

        self.id = id
        self._debug('Provider', '__init__', 'id', id)

        self.out_dir = kwargs.pop('dir', None)
        self._debug('Provider', '__init__', 'out_dir', self.out_dir)

        self.out_file = kwargs.pop('out_file', None)
        self._debug('Provider', '__init__', 'out_file', self.out_file)

    ###########################################################################

    #The following two methods MUST be overriden by the implementing class
    def get_download_url(self):
        raise ImportError
    def get_filename(self):
        raise ImportError

    #Optional override which occurs after the download url is opened by urllib2
    def download_callback(self, url):
        pass

    #Recommended to be overriden by implementing class, otherwise just video ID
    def get_title(self):
        title = self.id
        self._debug('Provider', 'get_title', 'title: ' + title)
        return title

    ###########################################################################

    def run(self):
        url = Provider._download(self.get_download_url())
        self.download_callback(url)

        #get_filename() MUST occur after download_callback()
        if self.out_file is None:
            self.out_file = self.get_filename()
        if self.out_dir is not None:
            self.out_file = os.path.join(self.out_dir, self.out_file)
        self.out_file = re.sub(ur'[?\[\]\/\\=+<>:;",*]+', '_', self.out_file, re.UNICODE)
        self._debug('Provider', 'run', 'out_file', self.out_file)

        out = open(self.out_file, 'wb')
        out.write(url.read())
        out.close()
        url.close()

    def _debug(self, cls, method, *args):
        if self.debugging:
            argc = len(args)
            if argc == 2:
                print '%s %s:%s %s = %s' % (datetime.now(), cls, method, args[0], args[1])
            else:
                print '%s %s:%s - %s' % (datetime.now(), cls, method, args[0])

    @staticmethod
    def _download(url):
        return urllib2.urlopen(urllib2.Request(url, headers=Provider.HEADERS))


from vimeo import Vimeo
from youtube import YouTube