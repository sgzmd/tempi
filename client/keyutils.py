from importlib import util as iutil
import logging

def GetIftttKeyOrDie():
    spec = iutil.find_spec('iftt_key')
    if spec == None:
        raise Exception("Please create iftt_key.py with KEY=<your IFTTT webhook key>")
    module = iutil.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.KEY

def GetThingspeakKeyOrDie():
    spec = iutil.find_spec('thingspeak_key')
    if spec == None:
        raise Exception("Please create iftt_key.py with KEY=<your IFTTT webhook key>")
    module = iutil.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.KEY

