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
sys.path.insert(0, os.path.abspath(__file__))

from unittest import defaultTestLoader, TestSuite, TextTestRunner, TestCase
from videodownloader.providers import Vimeo, YouTube


class VimeoTests(TestCase):
    video = Vimeo('5720832')

    def test_best_format(self):
        self.assertEqual(VimeoTests.video._get_best_format(), 'hd')

    def test_comments(self):
        self.assertNotEqual(VimeoTests.video.comments, -1)

    def test_duration(self):
        self.assertNotEqual(VimeoTests.video.duration, -1)
        self.assertEqual(VimeoTests.video.duration, 299)

    def test_formats(self):
        self.assertEqual(VimeoTests.video.formats, set(['sd', 'hd']))

    def test_height(self):
        self.assertNotEqual(VimeoTests.video.height, -1)
        self.assertEqual(VimeoTests.video.height, 720)

    def test_likes(self):
        self.assertNotEqual(VimeoTests.video.likes, -1)

    def test_plays(self):
        self.assertNotEqual(VimeoTests.video.plays, -1)

    def test_request_expiration(self):
        self.assertNotEqual(VimeoTests.video.request_expiration, None)

    def test_request_signature(self):
        self.assertNotEqual(VimeoTests.video.request_signature, None)

    def test_thumbnail(self):
        self.assertNotEqual(VimeoTests.video.thumbnail, None)
        self.assertEqual(VimeoTests.video.thumbnail, 'http://b.vimeocdn.com/ts/209/280/20928062_640.jpg')

    def test_title(self):
        self.assertEqual(VimeoTests.video.title, 'Brand New - Jesus (Daisy sessions)')

    def test_uploader(self):
        self.assertNotEqual(VimeoTests.video.uploader, None)
        self.assertEqual(VimeoTests.video.uploader, 'Wiseguy Pictures')

    def test_width(self):
        self.assertNotEqual(VimeoTests.video.width, -1)
        self.assertEqual(VimeoTests.video.width, 1280)


class YouTubeTests(TestCase):
    video = YouTube('tgbNymZ7vqY')

    def test_author(self):
        self.assertNotEqual(YouTubeTests.video.author, None)
        self.assertEqual(YouTubeTests.video.author, 'MuppetsStudio')

    def test_best_format(self):
        self.assertEqual(YouTubeTests.video._get_best_format(), '37')

    def test_duration(self):
        self.assertNotEqual(YouTubeTests.video.duration, -1)
        self.assertEqual(YouTubeTests.video.duration, 287)

    def test_formats(self):
        self.assertEqual(YouTubeTests.video.formats, set(['5', '37', '35', '22', '34']))

    def test_keywords(self):
        self.assertNotEqual(YouTubeTests.video.keywords, set([]))
        self.assertEqual(YouTubeTests.video.keywords, set(['Swedish', 'Zealand', 'Honeydew', 'Gonzo', 'Chef', 'Singing', 'Statler', 'Scooter', 'Teeth', 'Pepe', 'Frog', 'virmup', 'Brian', 'Camilla', 'Animal', 'Dr.', 'New', 'John', 'Bunny', 'virmupHD', 'Bobo', 'Eagle', 'Rock', 'Mahna', 'Electric', 'May', 'Rowlf', 'Minella', 'Bear', 'Monsters', 'Freddie', 'Opera', 'Floyd', 'Studio', 'Music', 'Lew', 'Strangepork', 'Beauregard', 'Queen', 'Beaker', 'King', 'Muppets', 'Mercury', 'Julius', 'Turkey', 'Chickens', 'Waldorf', 'Penguins', 'Zoot', 'Piggy', 'Harry', 'Newsman', 'Janice', 'Snowths', 'Bunsen', 'Deacon', 'Crazy', 'Taylor', 'Johnny', 'Sam', 'Show', 'Roger', 'Rhapsody', 'Musical', 'Sal', 'Roll', 'Prawn', 'Fozzie', 'Mayhem', 'Bohemian', 'Kermit', 'Fiama', 'Muppet', 'Miss']))

    def test_rating(self):
        self.assertNotEqual(YouTubeTests.video.rating, -1.0)

    def test_thumbnail(self):
        self.assertNotEqual(YouTubeTests.video.thumbnail, None)
        self.assertEqual(YouTubeTests.video.thumbnail, 'http://i1.ytimg.com/vi/tgbNymZ7vqY/default.jpg')

    def test_title(self):
        self.assertEqual(YouTubeTests.video.title, 'The Muppets: Bohemian Rhapsody [Original Version]')

    def test_token(self):
        self.assertNotEqual(YouTubeTests.video.token, None)



def run(verbosity=2):
    suite = [
        defaultTestLoader.loadTestsFromTestCase(VimeoTests),
        defaultTestLoader.loadTestsFromTestCase(YouTubeTests),
    ]
    return TextTestRunner(verbosity=verbosity).run(TestSuite(suite))

if __name__ == '__main__':
    run()
