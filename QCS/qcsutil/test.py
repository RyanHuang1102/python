#!/usr/bin/python
from qsgwlogger import *

LOG = QSGWLogger()
"""
mesg = LOG.id('123','213',[123,456])
mesg = LOG.id('block','213',[123,456])
mesg = LOG.id('block','CREATE_LUN_SUCCESS',(123,456))
mesg = LOG.id('block','CREATE_LUN_SUCCESS',[123,456])
"""
mesg = LOG.id('block','CREATE_LUN_SUCCESS',[123,456,789,1234])
mesg = LOG.id('block','CREATE_LUN_SUCCESS',['block01','ryanhuang','mylun',10])

#LOG.mesg('gg', '/var/log/iscsi/mesg_qsgwlogger.log', '2200lkfa;sfryanhuang')
LOG.mesg('NORMAL', '/var/log/iscsi/mesg_qsgwlogger.log', '2200lkfa;sfryanhuang')
LOG.mesg('NORMAL', '/var/log/iscsi/mesg1_qsgwlogger.log', '2200lkfa;sfryanhuang123123123')

LOG_tag = QSGWLogger('qsgw_iscsi')

LOG_tag.id('block','CREATE_LUN_SUCCESS',[123,456,789,1234])
LOG_tag.id('block','CREATE_LUN_SUCCESS',[123,456,789,1234456456])
LOG_tag.mesg('NORMAL', '/var/log/iscsi/mesg_qsgwlogger.log', '2200lkfa;sfryanhuang')
LOG_tag.mesg('NORMAL', '/var/log/iscsi/mesg1_qsgwlogger.log', '2200lkfa;sfryanhuang123123123')
