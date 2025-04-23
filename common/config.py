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

import configparser

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
            config = configparser.ConfigParser(interpolation=None)
            config.read_file(file)
            self.config = config

    def get_property(self, section, key):
        return self.config.get(section, key).strip('"')

