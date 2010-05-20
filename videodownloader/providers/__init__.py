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
    DEFAULT_EXT = 'video'
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11',
    }

    def __init__(self, id, title=None, ext=DEFAULT_EXT, format=None, debug=False):
        #Save debugging flag immediately
        self.debugging = debug

        self.id = id
        self._debug('Provider', '__init__', 'id', self.id)

        self.title = id if title is None else title
        self._debug('Provider', '__init__', 'title', self.title)

        self.format = format
        if self.format is not None:
            self._debug('Provider', '__init__', 'format', self.format)

        self.fileext = ext
        self._debug('Provider', '__init__', 'fileext', self.fileext)

        self.filename = title
        self._debug('Provider', '__init__', 'filename', self.filename)

        self.full_filename = None


    def _pre_download(self):
        '''
        Optional callback which occurs before the download takes place.
        '''
        self._debug('Provider', '_pre_download', 'No callback supplied.')

    def _in_download(self, url):
        '''
        Optional callback which occurs after the download url is opened by urllib2.
        '''
        self._debug('Provider', '_in_download', 'No callback supplied.')

    def _post_download(self, success):
        '''
        Optional callback which occurs after the download has finished.
        '''
        self._debug('Provider', '_post_download', 'No callback supplied.')

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
        self._debug('Provider', 'run', 'Running pre-download callback.')
        self._pre_download()

        url = None
        out = None
        success = False

        try:
            url = Provider._download(self.get_download_url())

            #Callback
            self._debug('Provider', 'run', 'Running in-download callback.')
            self._in_download(url)

            #Invalid filename character fix
            if IS_WINDOWS:
                filename = re.sub(ur'[?\/\\<>:"*|]+', '_', self.filename, re.UNICODE)
            self.full_filename = '%s.%s' % (filename, self.fileext)
            self._debug('Provider', 'run', 'full_filename', self.full_filename)

            if not os.path.isfile(self.full_filename):
                #Save the stream to the output file
                out = open(self.full_filename, 'wb')
                out.write(url.read())
            else:
                #Skipping
                #TODO: warn
                pass

            #We are done therefore success!
            success = True
        finally:
            if out is not None:
                out.close()
            if url is not None:
                url.close()

            #Callback
            self._debug('Provider', 'run', 'Running post-download callback.')
            self._debug('Provider', 'run', 'success', success)
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