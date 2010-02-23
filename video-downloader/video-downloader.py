#!/usr/bin/env python

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

from providers import YouTube, Vimeo

print 'video-downloader-1.0.0pre - by Jake Wharton <jakewharton@gmail.com>'
print

if __name__ == '__main__':
  YouTube('tgbNymZ7vqY', debug=True).run()
  Vimeo('5720832', debug=True).run()