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

IS_WINDOWS = (sys.platform == 'win32' or sys.platform == 'cygwin')

class Provider(object):
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
    }

    def __init__(self, id, title=None, ext='video', format=None, debug=False):
        self.id = id
        self.title = id if title is None else title
        self.format = format
        self.fileext = ext
        self.filename = title
        self.debugging = debug


    def _pre_download(self):
        '''
        Optional callback which occurs before the download takes place.
        '''
        pass
    def _in_download(self, url):
        '''
        Optional callback which occurs after the download url is opened by urllib2.
        '''
        pass
    def _post_download(self, success):
        '''
        Optional callback which occurs after the download has finished.
        '''
        pass
    def get_download_url(self):
        '''
        Required to be overriden by implementing class
        '''
        raise NotImplementedError('Provider did implement "get_download_url()". Cannot download video.')

    def run(self):
        '''
        Download the video.
        '''
        #Callback
        self._pre_download()

        url = None
        out = None
        success = False

        try:
            url = Provider._download(self.get_download_url())

            #Callback
            self._in_download(url)

            filename = self.filename + self.fileext
            #Invalid filename character fix
            if IS_WINDOWS:
                filename = re.sub(ur'[?\[\]\/\\=+<>:;",*]+', '_', filename, re.UNICODE)
            self._debug('Provider', 'run', 'filename', filename)

            out = open(filename, 'wb')
            out.write(url.read())

            success = True
        finally:
            if out is not None:
                out.close()
            if url is not None:
                url.close()

            #Callback
            self._post_download(success)

    def _debug(self, cls, method, *args):
        if self.debugging:
            if len(args) == 2:
                print '%s %s:%s %s = %s' % (datetime.now(), cls, method, args[0], args[1])
            else:
                print '%s %s:%s - %s' % (datetime.now(), cls, method, ' '.join(args))


    @staticmethod
    def _download(url):
        return urllib2.urlopen(urllib2.Request(url, headers=Provider.HEADERS))


from vimeo import Vimeo
from youtube import YouTube