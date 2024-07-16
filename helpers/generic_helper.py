# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random
import configparser
import os
import time
import subprocess
import logging


# Singleton config class

class Config:
    __instance = None

    @staticmethod
    def get_instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Config.__instance = self
            self.config = {}
            self.read_config()

    def read_config(self):
        with open("config.ini", mode='r') as file:
            config = configparser.ConfigParser()
            config.read_file(file)
            self.config = config

    def get_property(self, section, key):
        return self.config.get(section, key).strip('"')

# Helper functions

def gemini_response_to_template_html(response):
    # Sometimes gemini produces empty paragraphs as well as markdown in html outputs
    response = response.replace('<p></p>', '') 
    response = response.replace('```html', '')
    response = response.replace('```', '')
    response = response.replace('\"', '"')
    
    return """
        <div class="msg">""" + response + """</div>
    """

def get_random_color():
    return '#{:06x}'.format(random.randint(0, 256**3-1))

def get_audio_stream(request): 
    if 'audio' in request.files:
        audio_file = request.files['audio']
        
        base_filename = 'recording-'+str(random.randrange(0, 10000))+'-'+str(time.time())
        
        webm_filename = os.path.join('uploads', base_filename+'.webm')  
        mp3_filename = os.path.join('uploads', base_filename+'.mp3')  

        audio_file.save(webm_filename)

        # Convert webm to mp3
        subprocess.run([
            'ffmpeg',
            '-i', webm_filename,  # Input webm file
            '-vn',  # Disable video stream
            '-ar', '44100',  # Audio sampling rate (44.1 kHz)
            '-ac', '2',  # Number of audio channels (2 for stereo)
            '-b:a', '192k',  # Audio bitrate (192 kbps)
            mp3_filename  # Output mp3 file
        ])

        os.remove(webm_filename)  # Remove the temporary webm file
        logging.info('Audio saved successfully!')

        with open(mp3_filename, mode='rb') as file: # b is important -> binary
            data = file.read()
        file.close()

        os.remove(mp3_filename)  # Remove the temporary mp3 file
        return data
    else:
        logging.info('No audio input was provided. Fallback to text.')
        return None
