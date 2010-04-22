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

#Ensure we get the repository version and not an installed version
import os
import sys
sys.path.insert(0, os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

from unittest import defaultTestLoader, TestSuite, TextTestRunner, TestCase
from providers import Vimeo, YouTube


class VimeoTests(TestCase):
    def test_default_format(self):
        video = Vimeo('5720832')
        self.assertEqual(video.format, Vimeo.DEFAULT, 'Default value mismatch.')

    def test_SD(self):
        video = Vimeo('5720832', format=None)
        self.assertEqual(video.get_title(), 'Brand New - Jesus (Daisy sessions)', 'Invalid title.')

    def test_HD(self):
        video = Vimeo('5720832', format='hd')
        self.assertEqual(video.get_title(), 'Brand New - Jesus (Daisy sessions)', 'Invalid title.')


class YouTubeTests(TestCase):
    def test_default_format(self):
        video = YouTube('tgbNymZ7vqY')
        self.assertEqual(video.format, YouTube.DEFAULT, 'Default value mismatch.')

    def test_480p(self):
        video = YouTube('tgbNymZ7vqY', format='35')
        self.assertEqual(video.get_title(), 'The Muppets: Bohemian Rhapsody', 'Invalid title.')

    def test_720p(self):
        video = YouTube('tgbNymZ7vqY', format='22')
        self.assertEqual(video.get_title(), 'The Muppets: Bohemian Rhapsody', 'Invalid title.')

    def test_1080p(self):
        video = YouTube('tgbNymZ7vqY', format='37')
        self.assertEqual(video.get_title(), 'The Muppets: Bohemian Rhapsody', 'Invalid title.')



def run(verbosity=2):
    suite = [
        defaultTestLoader.loadTestsFromTestCase(VimeoTests),
        defaultTestLoader.loadTestsFromTestCase(YouTubeTests),
    ]
    return TextTestRunner(verbosity=verbosity).run(TestSuite(suite))

if __name__ == '__main__':
    run()