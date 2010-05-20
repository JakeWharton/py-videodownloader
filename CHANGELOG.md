Change Log
==========

Version 2.0.0 *(2010-05-19)*
--------------------------------
Rewrite of a significant portion of the codebase to be more modular and easier to extend.

New Features:

 * Supports thumbnail URL retrieval.
 * Improved Vimeo information parsing.
 * All data is stored in instance properties.
 * Provider-specific metadata is now retrieved.
 * Specify custom title and extension for videos.

Bug Fixes:

 * Tests properly reference the library after the folder shuffle.

Version 1.2.4 *(2010-05-07)*
----------------------------
Bug Fixes:

 * Convert all files to Unix-style line endings.

Version 1.2.3 *(2010-05-04)*
----------------------------
New Features:

 * Installable via `easy_install` or `pip`!

Version 1.2.2 *(2010-04-23)*
----------------------------
New Features:

 * New method for parsing token, resolutions, and the title for YouTube videos.

Version 1.2.1 *(2010-04-23)*
----------------------------
Bug Fixes:

 * Add period between file name and extension for a proper full filename.

Version 1.2.0 *(2010-04-21)*
----------------------------
New Features:

 * Ability to determine valid formats for a specific video.
 * Automatic downloading of highest format available if none specified.

Version 1.1.0 *(2010-04-04)*
--------------------------------
New Features:

 * Dynamic loading of providers.
 * Support passing in formats.
 * Unit test for all providers.
 * Alternate destination directory support.

Version 1.0.0 *(2010-03-05)*
----------------------------
Initial release with Vimeo and YouTube support.
