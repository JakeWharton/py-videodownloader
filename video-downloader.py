#!/usr/bin/env python

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

from optparse import OptionParser, OptionGroup
import providers
import sys

def main():
    DEFAULT_DEBUG = False

    version =  'video-downloader-1.1.0pre - by Jake Wharton <jakewharton@gmail.com>'
    parser = OptionParser(usage="Usage: %prog -p PROVIDER [-f FMT] [-o DIR] videoID [... videoID]", version=version)

    provider_list = ', '.join(["'%s'" % provider for provider in providers.__all__])
    parser.add_option('-f', '--format', dest='fmt', help='Format of video to download. Run with no video IDs for a provider specific list.')
    parser.add_option('-d', '--directory', dest='dir', help='Other directory to place downloaded files.')
    parser.add_option('-p', '--provider', dest='provider', help='Online provider from where to download the video. (Available: %s)'%provider_list)
    parser.add_option('--debug', dest='is_debug', action='store_true', default=DEFAULT_DEBUG, help='Enable debugging output.')

    options, videos = parser.parse_args()

    print version
    print

    #TODO: Load provider
    try:
        provider = getattr(providers, options.provider)
    except Exception:
        print 'ERROR: Could not load provider "%s".' % options.provider
        sys.exit(1)

    if len(videos) == 0:
        print '%-10s %-40s' % ('Format', 'Description')
        print '-'*10, '-'*40
        for format in provider.FORMATS.iteritems():
            print '%-10s %-40s' % format
    else:
        if options.fmt is None:
            options.fmt = provider.DEFAULT

        for video in videos:
            v = provider(video, format=options.fmt, debug=options.is_debug)
            print 'Downloading %s ("%s")...' % (video, v.get_title())
            v.run()

        print
        print 'Done.'

if __name__ == '__main__':
    main()