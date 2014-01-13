import inspect
from Logger_Experimental import Logger
from OmniCollect_Server_Experimental import OmniCollectServer
from OmniCore import OmniCore
from SubscriberRequest import SubscriberRequest
from loader.ScriptLoader import ModuleLoader

__author__ = 'Sefverl'

import sys


def main(argv):
    logger = Logger("logfile_temp_data.txt")

    requestForm = SubscriberRequest(logger)
    requestForm.addRequest("TEMPERATURE", "test")

    core = OmniCore()
    core.getEventManager().subscribe(logger.__callback__, requestForm)

    mod_loader = ModuleLoader(core)
    (module_file_names, modules) = mod_loader.load_modules()

    kwargs = {"core": core, 'filename': "logger.log"}

    # http://stackoverflow.com/questions/1796180/python-get-list-of-all-classes-within-current-module
    logger_module = modules[0]
    logger_class = inspect.getmembers(logger_module)

    for name, obj in logger_class:
        if inspect.isclass(obj):
            print(obj)
            print(name)

    logger_instance = modules[0].init_instance(**kwargs)
    #class_name,class_object = logger_class[0]
    #class_instance_logger = class_object(class_object,core,"Logger.class")
    #instance_logger = class_instance_logger.class_object(core,"Logger.class")
    print(logger_instance.__about__())
    print("Current # of subscribers (before Events): ", len(core.getEventManager().subscribers))
    print("State of EventManager (before Events): ", core.getEventManager().__dict__)
    server = OmniCollectServer(core, ("", 9999))

    server.listening_socket.serve_forever()


if __name__ == '__main__':
    main(sys.argv[1:])