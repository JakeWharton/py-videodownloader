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
from providers import YouTube, Vimeo

if __name__ == '__main__':
  DEFAULT_VIMEO = []
  DEFAULT_YOUTUBE = []

  DEFAULT_DEBUG = False

  version =  '''
  video-downloader-1.0.0 - by Jake Wharton <jakewharton@gmail.com>
  '''
  parser = OptionParser(usage="Usage: %prog [options] file1 [... fileN]", version=version)

  group = OptionGroup(parser, 'Video Provider Switches')
  group.add_option('-V', dest='vimeo_id', action='append', default=DEFAULT_VIMEO, help='Download video from YouTube.')
  group.add_option('-Y', dest='youtube_id', action='append', default=DEFAULT_YOUTUBE, help='Download video from Vimeo.')
  parser.add_option_group(group)

  group = OptionGroup(parser, "Display Options")
  group.add_option('--debug', dest='is_debug', action='store_true', default=DEFAULT_DEBUG, help='Turn on debugging output on.')
  parser.add_option_group(group)

  options, args = parser.parse_args()

  if len(args) > 0:
    raise ValueError('All video IDs must be specified with a provider switch.')
  if len(options.vimeo_id) == 0 and len(options.youtube_id) == 0:
    raise ValueError('You must specify at least one video to download.')

  for video in options.vimeo_id:
    v = Vimeo(video, debug=options.is_debug)
    print 'Downloading %s ("%s")...' % (video, v.get_title())
    v.run()
  for video in options.youtube_id:
    v = YouTube(video, debug=options.is_debug)
    print 'Downloading %s ("%s")...' % (video, v.get_title())
    v.run()

  print
  print 'Done.'