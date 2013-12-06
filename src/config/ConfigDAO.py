__author__ = 'Sefverl'

import os
import cPickle as pickle


class ConfigDAO(object):
    def __init__(self, default_directory=None):
        self.directory = default_directory

    def store_config(self, key, doc):
        key = key.lower()

        filename = os.path.join(self.directory if self.directory else os.path.curdir, key + ".conf")
        fd = open(filename, 'w')
        pickle.dump(doc, fd)

    def list_configs(self):
        directory = self.directory if self.directory else os.path.curdir

        absolute_path = os.path.join(os.path.abspath(directory), "config")
        dir_listing = os.listdir(absolute_path)

        json_configs = {}

        for listing in dir_listing:
            split_filename = listing.split('.')
            key = split_filename[-2]
            ext = split_filename[-1]

            if ext == 'conf':
                filename = os.path.join(absolute_path, listing)
                if os.path.isfile(filename):
                    json_configs[key] = filename

        return json_configs

    def load_config(self, key):
        key = key.lower()

        config_dir = self.list_configs()

        if key in config_dir:
            fd = open(config_dir[key], 'r')
            doc = pickle.load(fd)
            return doc

        return {}
