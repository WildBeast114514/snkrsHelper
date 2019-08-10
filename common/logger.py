#!/usr/bin/python3
# coding:utf-8


import os
import inspect
import logging
import logging.handlers

class Logger():
    logger = None

    @staticmethod
    def Init(logfile = '', level = logging.INFO, name = 'logger', logtostdout = False):
        # 避免重复Init
        if Logger.logger != None:
            return 

        Logger.logger = logging.getLogger(name)
        Logger.logger.setLevel(level = level)
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(thread)d|%(message)s')
        if logfile == '':
            logfile = './'+name+'.log'

        if not Logger.logger.handlers:
            handler = None
            if logtostdout:
                handler = logging.StreamHandler()
            else:
                handler = logging.handlers.TimedRotatingFileHandler(
                                logfile, when="D", interval=7, backupCount=7, encoding="utf8")
                handler.suffix = "%Y%m%d.log"
            handler.setLevel(level)
            handler.setFormatter(formatter)
            Logger.logger.addHandler(handler)


def LOG_DEBUG(message):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    Logger.logger.debug("%s|%s:%i| %s" % (
        caller.function, 
        os.path.basename(caller.filename), 
        caller.lineno,
        message 
    ))

def LOG_INFO(message):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    Logger.logger.info("%s|%s:%i| %s" % (
        caller.function, 
        os.path.basename(caller.filename), 
        caller.lineno,
        message 
    ))

def LOG_WARN(message):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    Logger.logger.warn("%s|%s:%i| %s" % (
        caller.function, 
        os.path.basename(caller.filename), 
        caller.lineno,
        message  
    ))

def LOG_ERROR(message):
    caller = inspect.getframeinfo(inspect.stack()[1][0])
    Logger.logger.error("%s|%s:%i| %s" % (
        caller.function, 
        os.path.basename(caller.filename), 
        caller.lineno,
        message 
    ))

# Main functions
if __name__ == "__main__":
    Logger.Init(logtostdout=True, level = logging.DEBUG)
    #Logger.Init()
    LOG_DEBUG("logger")
    LOG_INFO("logger")
