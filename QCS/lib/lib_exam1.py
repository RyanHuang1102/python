#!/usr/bin/python

from lib import *

Config = config("test.cfg")

ret = Config.Ini_Conf_Set_Field('mylun', 'alias', 'haha')
ret = Config.Ini_Conf_Remove_Section('mylun')
print ret
ret = Config.Ini_Conf_Get_Field('mylun','dev')
print ret
#ret = Config.Ini_Conf_Remove_Section('Global')



