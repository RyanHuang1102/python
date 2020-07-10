#!/usr/bin/python

import argparse
import os
import sys
import json
import logging
import socket
from logging.handlers import RotatingFileHandler, SysLogHandler

# append import path
sys.path.append('/home/ryanhuang/QCS-task/check_in/qcsutil')
# global variable
qsgwlogger_flag = {'NORMAL':'0x0001','WARNING':'0x0002','CRITICAL':'0x0004'}
qsgwlogger_config = '/etc/config/qsgwlogger.cfg'
facilities = ['kern','user','mail','daemon','auth','syslog','lpr',
        'news','uucp','cron','authpriv','ftp','local0','local1',
        'local2','local3','local4','local5','local6','local7']

class QSGWLogger():
    def __init__(self,tag=None,facility=None):
        self.tag = tag
        self.facility = facility
        if tag is None:
            self.tag = 'qsgwlogger'
        if facility is None:
            self.facility = 'user'

        # add level name to lower-case
        logging.addLevelName(logging.INFO, 'info')
        logging.addLevelName(logging.WARNING, 'warn')
        logging.addLevelName(logging.CRITICAL, 'crit')

        self._auto_prepare_default_config_file()

    def _auto_prepare_default_config_file(self):
        # prepare log config file.
        if not os.path.isdir('/etc/config'):
            os.mkdir('/etc/config')
        if not os.path.isfile(qsgwlogger_config):
            with open(qsgwlogger_config, 'w') as fo:
                data = {'Level':'0x0004','Syslogd':'Disabled'}
                json.dump(data, fo, indent=4)

    def _check_mesg_code_exist(self, service, mesg_code):
        if service == 'file':
            return False
        elif service == 'block':
            from MesgCodeTable.BlockMesgTable import mesg_code_table
            if mesg_code not in mesg_code_table:
                return False
            mesg = mesg_code_table[mesg_code]
            return mesg
        elif service == 'object':
            return False
        else:
            print 'Not Support this service %s'%(service)
            return False

    def _prepare_syslog_handler(self):
        if self.facility not in facilities:
            print 'Not support this facility'
            return 1
        logger = logging.getLogger(self.tag)
        handler = SysLogHandler(address = '/dev/log')
        formatter = self.facility+'.%(levelname)s %(name)s: %(message)s'
        handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(handler)
        return logger, handler

    def _prepare_rotating_handler(self, logfile):
        if self.facility not in facilities:
            print 'Not support this facility'
            return 1
        # prepare log path
        if logfile:
            log_dir = os.path.split(logfile)[0]
            if not os.path.isdir(log_dir): 
                os.makedirs(log_dir)
        logger = logging.getLogger(self.tag)
        handler = RotatingFileHandler(logfile, mode='w', maxBytes=5*1024*1024,
                                     backupCount=3, encoding='utf-8', delay=0)
        formatter = '%(asctime)s '+self.facility+'.%(levelname)s %(name)s: %(message)s'
        handler.setFormatter(logging.Formatter(formatter, "%B %d %H:%M:%S"))
        logger.addHandler(handler)
        return logger, handler

    def _get_config_setting(self):
        with open(qsgwlogger_config, 'r') as fo:
            data = json.load(fo)
        try:
            data['Level']
        except:
            return None
        try:
            data['Syslogd']
        except:
            return None
        return data 

    def _print_mesg(self, logger, flag, level, mesg):
        if flag:
            if level == 'NORMAL':
                logger.setLevel(logging.INFO)
                logger.info(mesg)
            elif level == 'WARNING':
                logger.setLevel(logging.WARNING)
                logger.warning(mesg)
            elif level == 'CRITICAL':
                logger.setLevel(logging.CRITICAL)
                logger.critical(mesg)
        else:
            return 0

    def id(self, service, mesg_code, mesg_code_args):
        # checking all input args
        if type(mesg_code_args) is not list:
            print 'args must be list type'
            return 1
        support_service = ['file','block','object']
        if service not in support_service:
            print 'Only Support {0} {1} {2} service.'.format(*support_service)
            return 1
        mesg = self._check_mesg_code_exist(service, mesg_code)
        if not mesg:
            print 'message code %s not exist.'%(mesg_code)
            return 1
        try:
            mesg_level = mesg['level']
            mesg = mesg['mesg'].format(*mesg_code_args)
        except IndexError:
            print mesg['mesg']
            print mesg_code_args
            print 'Please check input args.'
            return 1
        setting = self._get_config_setting() 
        if setting:
            syslogd_enable = setting['Syslogd']
        else:
            syslogd_enable = 'Disabled'
        # sysloghandler
        if syslogd_enable == 'Enabled':
            #status = os.system('ps aux |grep [s]yslogd >/dev/null 2>&1')
            status = os.system('ps aux |grep [r]syslogd >/dev/null 2>&1')
            if status is not 0:
                os.system('/usr/sbin/rsyslogd')
                #os.system('/sbin/syslogd')
            syslog_logger, syslog_handler = self._prepare_syslog_handler()
            self._print_mesg(syslog_logger, 1, mesg_level, mesg)
            syslog_logger.removeHandler(syslog_handler)
        # rotatinghandler
        id_logfile = '/var/log/qsgw_id/id_message.log'
        rotating_logger, rotating_handler = self._prepare_rotating_handler(id_logfile)
        self._print_mesg(rotating_logger, 1, mesg_level, mesg)
        rotating_logger.removeHandler(rotating_handler)

    def mesg(self, level, mesg_logfile, mesg):
        if level not in qsgwlogger_flag:
            print 'Not Support this level %s'%(level)
            return 1
        setting = self._get_config_setting() 
        if setting:
            flag = int(setting['Level'],16) & int(qsgwlogger_flag[level],16)
            syslogd_enable = setting['Syslogd']
        else:
            flag = 0
            syslogd_enable = 'Disabled'
        # rotatinghandler
        rotating_logger, rotating_handler = self._prepare_rotating_handler(mesg_logfile)
        self._print_mesg(rotating_logger, flag, level, mesg)
        rotating_logger.removeHandler(rotating_handler)

if __name__ == '__main__':

    def build_parser():
        # handle argparse
        parser = argparse.ArgumentParser(
            prog='qsgwlogger.py',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=
            '''
            example:\n
            qsgwlogger.py ID -s block -m CREATE_LUN_SUCCESS -a block01 ryanhuang mylun 10 [-t qsgw_iscsi] [-f user]
            qsgwlogger.py Mesg -l NORMAL -p /var/log/iscsi.log -m mesg [-t qsgw_iscsi] [-f user]
            '''
        )
        # create subparsers
        subparsers = parser.add_subparsers(help='sub-command help')
        # create the parser for the "ID" command
        parser_id = subparsers.add_parser('ID', help='ID command help')
        parser_id.add_argument(
                '-s', '--service', type=str, 
                help='choose service',
                choices=['file', 'block', 'object'],
                required=True)
        parser_id.add_argument(
                '-m', '--mesg_code', type=str,
                help='covert mesg_code to sting',
                required=True)
        parser_id.add_argument('-a', '--args', 
                metavar='params', help='input params', 
                nargs='+', required=True)
        parser_id.add_argument(
                '-t', '--tag', type=str, 
                metavar='tag name',
                help='syslog tag name, default is qsgwlogger')
        parser_id.add_argument(
                '-f', type=str, 
                help='syslog facility, default is user',
                choices=facilities)

        # create the parser for the "Mesg" command
        parser_mesg = subparsers.add_parser('Mesg', help='Mesg command help')
        parser_mesg.add_argument(
                '-l', '--level', type=str,
                help='level', choices=['NORMAL','WARNING','CRITICAL'],
                required=True)
        parser_mesg.add_argument(
                '-p', '--path', type=str,
                metavar='log path', help='log path',
                required=True)
        parser_mesg.add_argument(
                '-m', '--mesg',type=str,
                metavar='message', help='input mesg',
                required=True)
        parser_mesg.add_argument(
                '-t', '--tag', type=str, 
                metavar='tag name',
                help='syslog tag name, default is qsgwlogger')
        parser_mesg.add_argument(
                '-f', type=str, 
                help='syslog facility, default is user',
                choices=facilities)
        return parser

    parser = build_parser()
    # parse some argument lists
    args = parser.parse_args()
    tag = args.tag
    facility = args.f
    qsgwlogger = QSGWLogger(tag,facility)
    try:
        service = args.service
        mesg_code = args.mesg_code
        mesg_code_args = args.args
        qsgwlogger.id(service, mesg_code, mesg_code_args)
    except:
        level = args.level
        path = args.path
        mesg = args.mesg
        qsgwlogger.mesg(level, path, mesg)
