# CG Cookie Bot - A video downloader for the lessons of the courses
# Copyright (C) 2015 Santiago Sanchez Sobrino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import os
import sys
import errno
import re
import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from subprocess import call


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


class CGCookieBot:
    login_url = "https://cgcookie.com/wp-login.php"
    login_user = "enter here your username"
    login_pass = "enter here your password"

    def run(self, argv):
        if len(argv) < 3:
            self.help(argv)
            return

        if '--url' in argv:
            self.downloadCourse(argv[2])
        elif '--file' in argv:
            with open(argv[2], "r") as ins:
                for url in ins:
                    if url[0] != '#':
                        self.downloadCourse(url)

    def downloadCourse(self, url):
        # Firefox selenium driver
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

        # Log in to the website
        self.driver.get(self.login_url)
        self.driver.find_element_by_id("user_login").send_keys(self.login_user)
        self.driver.find_element_by_id("user_pass").send_keys(self.login_pass)
        self.driver.find_element_by_name("wp-submit").click()

        # Recuperamos videos y titulos de las lecciones del curso especificado

        # 1. Let's go to the course's url
        # 2. Get the course's title to use it as directory name
        # 3. Get the number of lessons for this course (the real ones; avoid quizes)
        self.driver.get(url)
        course_title = self.driver.find_element_by_xpath('//h1[@class="entry-title"]').text.strip()
        lessons = self.driver.find_elements_by_xpath('//ol[@class="course-lessons-list"]/li')
        real_num_lessons = 0
        for l in lessons:
            if 'Quiz' not in l.text.strip():
                real_num_lessons += 1

        print "{}: {} lessons".format(course_title, real_num_lessons)
        print '---'

        mkdir_p(course_title)
        num_lessons = len(lessons)  # The official number of lessons just to get the right indexes
        counter = 1  # What lesson are us?

        # Let's loop over all the lessons
        for i in xrange(num_lessons):
            # Skip quizes
            if 'Quiz' in lessons[i].text.strip():
                continue

            # Get lesson url and open a new tab loading it
            url = lessons[i].find_element_by_tag_name('a').get_attribute('href')
            self.openTab(url)

            # Videos are retrieved through AJAX, so let's wait some seconds to
            # be assure video exists
            time.sleep(2)

            # Build a dictionary to hold the lesson data (name and video url)
            item = {}

            # 1. Get the lesson name
            # 2. Remove non-ascii characters
            # 3. Trim non-alphanumeric characters from the name to add our own index
            item['name'] = self.driver.find_element_by_xpath('//h1[@class="entry-title"]').text.strip()
            item['name'] = item['name'].encode('ascii', 'ignore').decode('ascii')
            item['name'] = re.sub('^[^a-zA-z]*', '', item['name'])
            item['name'] = str(counter) + '. ' + item['name']

            # Check for lesson existence; whether it exists, we skip it
            if glob.glob(os.path.join(course_title, item['name']) + '.*'):
                print "{}. This lesson has been already downloaded; skipping.".format(item['name'])
                self.closeTab()
                counter += 1
                continue

            try:
                # Is the video internal to the site?
                item['link'] = self.driver.find_element_by_xpath('//*[@id="wistia_12_source"]').get_attribute('src')
                item['in_service'] = True
            except:
                # Is the video in a remote provider such as youtube, vimeo, etc?
                try:
                    item['link'] = self.driver.find_element_by_xpath('/html/body/section[2]/div/div/div/article/div[1]/div/iframe').get_attribute('src')
                    item['link'] = item['link'].encode('ascii', 'ignore').decode('ascii')
                except:
                    item['link'] = "E - No se puede obtener la URL del video"
                item['in_service'] = False

            print '{} -> {}'.format(item['name'], item['link'])
            self.downloadVideo(course_title, item)
            print '---'

            counter += 1

            self.closeTab()

        self.driver.close()

    def downloadVideo(self, directory, video):
        # If the video is stored in-site, let's download it using wget (direct link)
        if(video['in_service']):
            call(['wget', '{}'.format(video['link']), '-O', os.path.join(directory, video['name'] + ".mp4")])
        else:
            if(video['link'][0] != 'E'):
                # Else, let's use youtube-dl to download it
                call(['youtube-dl', '-o', os.path.join(directory, video['name'] + ".%(ext)s"), video['link']])

    def openTab(self, url, delay=1):
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 't')
        time.sleep(delay)
        self.driver.get(url)

    def closeTab(self, delay=1):
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'w')
        time.sleep(delay)

    def help(self, argv):
        print "Info:\n    {} <--url course_url> | <--file urls_file>".format(argv[0])

if __name__ == "__main__":
    app = CGCookieBot()
    app.run(sys.argv)
