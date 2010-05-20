py-videodownloader
===================
Python module and script for downloading video source files from the major
online streaming sites (YouTube, Vimeo, etc.)


Usage
=====
Videos from various providers can be specified using the following command line
format:

    Usage: videodownloader.py -p PROVIDER [-f FMT] [-d DIR] videoID [... videoID]

    Options:
      -h, --help            show this help message and exit
      -e EXT, --ext=EXT     Manually override video extension.
      -f FORMAT, --format=FORMAT
                            Format of video to download. Run with no video IDs for
                            a provider specific list.
      -t TITLE, --title=TITLE
                            Manually override video title.
      -p PROVIDER, --provider=PROVIDER
                            Online provider from where to download the video.
                            (Available: 'Vimeo', 'YouTube')
      --debug               Enable debugging output.


Example
-------
The following two commands will download a 720p video from Vimeo and a 1080p
one from YouTube.

    $ videodownloader.py -p Vimeo -f hd 5720832
    $ videodownloader.py -p YouTube -f 37 tgbNymZ7vqY

To see a list of the formats supported by a provider run the command without
any video IDs.

    $ videodownloader.py -p YouTube
    videodownloader-2.0.0 - by Jake Wharton <jakewharton@gmail.com>

    Format     Description
    ---------- ----------------------------------------
    13         176x144 3GP/AMR Mono 3GP
    17         176x144 3GP/AAC Mono 3GP
    22         1280x720 H.264/AAC Stereo MP4
    18         480x360/480x270 H.264/AAC Stereo MP4
    37         1920x1080 H.264/AAC Stereo MP4
    35         640x480/640x360 H.264/AAC Stereo FLV
    34         320x240 H.264/AAC Stereo FLV
    5          320x240 H.263/MP3 Mono FLV
    6          320x240 H.263/MP3 Mono FLV

Omitting a format will automatically download the best format available for
that video from the provider.


Developed By
============
* Jake Wharton - <jakewharton@gmail.com>

Git repository located at
[http://github.com/JakeWharton/py-videodownloader](http://github.com/JakeWharton/py-videodownloader)


Thanks
======
*   __chexov__

    For `py-youtube-downloader`, the inspiration and basis for this module and
    script. Check it out at
    [http://github.com/chexov/py-youtube-downloader](http://github.com/chexov/py-youtube-downloader).

*   __Arlo Faria__

    Improvement of the token, resolution, and title parsing for YouTube videos.


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
