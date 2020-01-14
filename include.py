from ctypes import *
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse

from qcslib.qcs_utils import *
from qcslib.qcs_rest_api import *
from error import *

import os
import sys
import threading

"""
    Parameters
"""
class LUN_PARM(Structure):
    _fields_ = [("lun_idx", c_int),
                ("lun_name", c_char_p)]

class TRGT_PARM(Structure):
    _fields_ = [("trgt_idx", c_int),
                ("trgt_name", c_char_p)]

class TRGTG_PARM(Structure):
    _fields_ = [("trgtG_idx", c_int),
                ("trgtG_name", c_char_p)]

class INIT_PARM(Structure):
    _fields_ = [("init_idx", c_int),
                ("init_name", c_char_p)]
"""
    Stdout Grabber
"""
class Grabbing_Output():

    def __init__(self):
        self.fileno = sys.stdout.fileno()
        self.stdout_save = os.dup(self.fileno)
        self.pipe = os.pipe() #get r,w pipe
        os.dup2(self.pipe[1], self.fileno)
        os.close(self.pipe[1])
        self.Theard = threading.Thread(target = self.drain_pipe)
        self.Theard.start()

    def drain_pipe(self):
        self.captured = ''
        while True:
            data = os.read(self.pipe[0], 2048)
            if not data:
                break
            self.captured += data

    def stop(self):
        os.close(self.fileno)
        self.Theard.join()
        os.close(self.pipe[0])
        os.dup2(self.stdout_save, self.fileno)
        os.close(self.stdout_save)
        return self.captured
        
