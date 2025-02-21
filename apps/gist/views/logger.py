import random
import string

from django.views import generic
import logging
from django.conf import settings
import os, sys, time
import inspect
from rest_framework.permissions import BasePermission



class LogHelper(generic.DetailView):
    def fail_log(e):
        exec_type, exec_obj, exec_tb = sys.exc_info()
        file_name=inspect.currentframe().f_code.co_filename
        log = "----------- Error: " + str(exec_obj) + ", File: " + file_name + ", Line: " + str(
            exec_tb.tb_lineno) + " ------------"
        print(log)
        logger = logging.getLogger(__name__)
        logger.debug(log)
