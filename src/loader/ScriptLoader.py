import os
import hashlib
import imp
import traceback
import sys

from OmniComponent import OmniComponent

__author__ = 'Sefverl'


class ModuleLoader(OmniComponent):
    MODULE_DIR = "../scripts/"

    def __init__(self, core):
        super(ModuleLoader, self).__init__(core)
        self.modules = {}

    def load_modules(self):
        scripts_dirs = []
        modules = []

        for dir in os.listdir(ModuleLoader.MODULE_DIR):
            dir_path = os.path.join(ModuleLoader.MODULE_DIR, dir)
            if (os.path.isdir(dir_path)):
                base_name = dir.split(".")[-1]
                scripts_dirs.append((dir, dir_path))
                modules.append(self.load_module(os.path.join(dir_path, base_name + ".py")))

        return (scripts_dirs, modules)

    # Import and return module from file
    # SRC = http://code.davidjanes.com/blog/2008/11/27/how-to-dynamically-load-python-code/
    def load_module(self, module_path):
        try:
            try:
                module_code_dir = os.path.dirname(module_path)
                module_code_file = os.path.basename(module_path)

                module_file = open(module_path, 'rb')
                md5_hasher = hashlib.md5()
                md5_hasher.update(module_path)
                dir_hash = md5_hasher.digest()
                return imp.load_source(dir_hash, module_path, module_file)
            finally:
                try:
                    module_file.close()
                except:
                    pass
        except ImportError, x:
            traceback.print_exc(file=sys.stderr)
            raise
        except:
            traceback.print_exc(file=sys.stderr)
            raise

    def reload_modules(self):
        pass
