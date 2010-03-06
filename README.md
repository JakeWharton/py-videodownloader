py-video-downloader
===================
Python module and script for downloading video source files from the major
streaming sites (YouTube, Vimeo, etc.)

Usage
=====
Videos from Vimeo or YouTube can be downloaded by specifying them as
command-line arguments.

    Usage: video-downloader.py [options]

    Options:
      --version        show program's version number and exit
      -h, --help       show this help message and exit

      Video Provider Switches:
        -V VIMEO_ID    Download video from YouTube.
        -Y YOUTUBE_ID  Download video from Vimeo.

      Display Options:
        --debug        Turn on debugging output on.

Example
-------
The following will download one video from Vimeo and two from YouTube:

    ./video-downloader.py -V 5720832 -Y tgbNymZ7vqY -Y tgbNymZ7vqY


Developed By
============
* Jake Wharton - <jakewharton@gmail.com>

Git repository located at
[http://github.com/JakeWharton/py-video-downloader](http://github.com/JakeWharton/py-video-downloader)

Thanks
======
*   __chexov__

    For `py-youtube-downloader`, the inspiration and basis for this module and script. Check it out at [http://github.com/chexov/py-youtube-downloader](http://github.com/chexov/py-youtube-downloader).

License
=======
    Copyright 2010 Jake Wharton

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
