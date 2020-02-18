#!/usr/bin/python

from lib import *

Config = config("test.cfg")

#Config.Ini_Conf_Set_Field('mylun', 'alias', 'haha')
#ret = Config.Ini_Conf_Get_Field('mylun','dev')
ret = Config.Ini_Conf_Remove_Section('mylun')
ret = Config.Ini_Conf_Remove_Section('Global')
print ret



