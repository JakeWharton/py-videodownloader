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
import sys
import os

from videodownloader import providers

def main():
    DEFAULT_DEBUG = False

    print 'videodownloader-2.0.0 - by Jake Wharton <jakewharton@gmail.com>'
    print

    parser = OptionParser(usage="Usage: %prog -p PROVIDER [-f FMT] [-d DIR] videoID [... videoID]")

    provider_list = ', '.join(["'%s'" % provider for provider in providers.__all__])
    parser.add_option('-e', '--ext', dest='ext', default=providers.Provider.DEFAULT_EXT, help='Manually override video extension.')
    parser.add_option('-f', '--format', dest='format', help='Format of video to download. Run with no video IDs for a provider specific list.')
    parser.add_option('-t', '--title', dest='title', help='Manually override video title.')
    parser.add_option('-p', '--provider', dest='provider', help='Online provider from where to download the video. (Available: %s)'%provider_list)
    parser.add_option('--debug', dest='is_debug', action='store_true', default=DEFAULT_DEBUG, help='Enable debugging output.')

    options, videos = parser.parse_args()

    try:
        provider = getattr(providers, options.provider)
    except Exception:
        print 'ERROR: Could not load provider "%s".' % options.provider
        sys.exit(1)

    if len(videos) == 0:
        #Print out a format list for that provider
        print '%-10s %-40s' % ('Format', 'Description')
        print '-'*10, '-'*40
        for format in provider.FORMATS.iteritems():
            print '%-10s %-40s' % format
    else:
        for video in videos:
            v = provider(video, title=options.title, format=options.format, ext=options.ext, debug=options.is_debug)
            print 'Downloading "%s"...' % v.title
            try:
                v.run()
            except KeyboardInterrupt:
                print "WARNING: Aborting download."

                #Try to delete partially completed file
                try:
                    os.remove(v.full_filename)
                except IOError:
                    print 'WARNING: Could not remove partial file.'
            except (urllib2.HTTPError, IOError):
                print "ERROR: Fatal HTTP error."

        print
        print 'Done.'