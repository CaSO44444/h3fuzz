# -*-coding:utf-8 -*-
import os
import sys
import threading
from lib import *

DEBUG = False

def programModeMatch(args):
    """
    Determine the program running mode
    """
    global DEBUG
    params = {'url': [], 'mode': 'spider', 'isBatch': False, 'proxy': ''}
    # Whether to enable the debug mode
    if args:
        pass
    # Determine whether to batch detect target objects
    if isTextFileValid(args['target']):
        params['isBatch'] = False
        params['url'].extend(getTextFileValid(args['target'].strip().lower()))
    elif isUrlValid(args['target']):
        params['url'].append(args['target'].strip().lower())
    # Determine the program running mode, spider/fuzz/nofuzz/api/noapi
    if args['mode'] is None:
        return params



    length_of_args = len(args)
    if length_of_args > 1:
        # Determine whether to batch detect target objects
        if isTextFileValid(args[1]):
            isBatch = True
        elif isUrlValid(args[1]):
            isBatch = False
        else:
            return
        # Determine the program running mode, spider/fuzz/nofuzz/api/noapi
        if length_of_args > 4 or length_of_args < 2:
            return
        elif length_of_args == 2:
            return isBatch, 'spider'
        elif length_of_args == 3:
            if args[2].lower() == 'fuzz':
                return isBatch, 'fuzz'
            elif args[2].lower() == 'api':
                return isBatch, 'api'
            return
        elif length_of_args == 4:
            if args[2].lower() == 'fuzz' and args[3].lower() == 'noapi':
                return isBatch, 'fuzz', 'noapi'
            return
        elif length_of_args == 4:
            if args[2].lower() == 'api' and args[3].lower() == 'nofuzz':
                return isBatch, 'api', 'nofuzz'
            return
    return


def run():
    pass


def main(args):
    """
    API extraction main function
    """
    if 'debug' in args:
        run()
    else:
        try:
            run()
        except KeyboardInterrupt:
            pass
        except ValueError as e:
            print(e)
        finally:
            if threading.active_count() > 1:
                os._exit(getattr(os, "_exitcode", 0))
            else:
                sys.exit(getattr(os, "_exitcode", 0))
