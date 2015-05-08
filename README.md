CG Cookie Bot
============
A simple bot to download all videos for a given course or tutorial from the CG Cookie site, in order to watch them offline. It allows you to enter your user and password in the script itself to enjoy your citizen access.

The script has been successfully tested with the Blender Cookie and Unity Cookie subsites.

Installation
------------
The script depends hardly on Selenium. You can install it using pip:

    $ sudo pip install selenium

It also depends on Firefox to automate the whole process. If you don't use Firefox, you can hack the script in order to use Chrome or any other Selenium supports.

Once installed, you have to edit the script to set your user and password in the lines 26 and 27. If you don't trust me, I encourage you to run a `grep` a to the script and see what happens with your user and password:

    $ grep -Enr 'login_user|login_pass' cgcookiebot.py

Also, in order to download videos others but internals to the site (from youtube or vimeo) you have to install [`youtube-dl`](https://github.com/rg3/youtube-dl/):

    $ sudo pip install youtube_dl

Usage
------------
After installing it, you can launch the script by running the next command:
 
    $ python cgcookiebot.py <--url course_url> | <--file urls_file>
So if you want to download the lessons for one course, you have to run:

    $ python cgcookiebot.py --url https://cgcookie.com/blender/cgc-courses/blender-2-72-overview-new-features/
You can also use the `--file` option to specify a text file with all the courses' urls you want to download, one per line. If one of these lines starts by a `#` character, it will be ignored.

License
------------

> CG Cookie Bot - A video downloader for the lessons of the courses
> Copyright (C) 2015 Santiago Sánchez Sobrino
> 
> This program is free software: you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation, either version 3 of the License, or (at
> your option) any later version.
> 
> This program is distributed in the hope that it will be useful, but
> WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
> General Public License for more details.
> 
> You should have received a copy of the GNU General Public License
> along with this program.  If not, see <http://www.gnu.org/licenses/>.

Full text can be found at the [LICENSE file](https://github.com/SanchezSobrino/CGCookieBot/blob/master/LICENSE).
