# -*- coding: utf-8 -*-
from pynetworking import Feature
from pprint import pformat
import re
import json
import socket
try:
    from collections import OrderedDict
except ImportError: #pragma: no cover
    from ordereddict import OrderedDict


class awp_file(Feature):
    """
    File feature implementation for AWP
    """
    def __init__(self, device, **kvargs):
        Feature.__init__(self, device, **kvargs)
        self._file_config={}
        self._file={}
        self._d = device
        self._d.log_debug("loading feature")

    def load_config(self, config):
        self._d.log_info("loading config")
        self._file_config = OrderedDict()

        # 588 -rw- Jun 10 2014 12:38:10  michele.cfg
        ifre = re.compile('\s+(?P<size>\d+)\s+'
                          '(?P<permission>[^\s]+)\s+'
                          '(?P<month>[^\s]+)\s+'
                          '(?P<day>\d+)\s+'
                          '(?P<year>\d+)\s+'
                          '(?P<hhmmss>[^\s]+)\s+'
                          '(?P<file_name>[^\s]+)')
        for line in self._device.cmd("dir").split('\n'):
            m = ifre.match(line)
            self._d.log_info("read {0}".format(line))
            if m:
                self._file_config[m.group('file_name')] = {'size': m.group('size'),
                                                           'permission': m.group('permission'),
                                                           'month': m.group('month'),
                                                           'day': m.group('day'),
                                                           'year': m.group('year'),
                                                           'hhmmss': m.group('hhmmss')
                                                          }
        self._d.log_info(self._file_config)


    def download(self, device_path):
        self._d.log_info("copying {0} from device to host".format(device_path))
        self._update_file()

        # host HTTP server thread

        # device commands
        host_ip_address = socket.gethostbyname(socket.getfqdn())
        device_ip_address = self._d._host
        download_cmd = 'copy ' + device_path + ' http://' + device_ip_address + '/' + device_path
        cmds = {'cmds':[{'cmd': 'enable'    , 'prompt':'\#'},
                        {'cmd': 'conf t'    , 'prompt':'\(config\)\#'},
                        {'cmd': download_cmd, 'prompt':'\(config\)\#'},
                        {'cmd': chr(26)     , 'prompt':'\#'},
                       ]}

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._device.load_system()


    def upload(self, host_path, overwrite=False):
        self._d.log_info("copying {0} from host to device".format(host_path))
        self._update_file()

        add_confirmation = False
        dir_names = host_path.split('/')
        dev_file_name = dir_names[-1]
        if dev_file_name in self._d.file.keys():
            if overwrite == False:
                raise KeyError('file {0} cannot be overwritten'.format(dev_file_name))
            else:
                add_confirmation = True

        # host HTTP server thread

        # device commands
        host_ip_address = socket.gethostbyname(socket.getfqdn())
        device_ip_address = self._d._host
        upload_cmd = 'copy http://' + host_ip_address + host_path + ' ' + dev_file_name
        cmds = {'cmds':[{'cmd': 'enable'  , 'prompt':'\#'},
                        {'cmd': 'conf t'  , 'prompt':'\(config\)\#'},
                        {'cmd': upload_cmd, 'prompt':'\(config\)\#'}
                       ]}

        if add_confirmation == True:
            cmds['cmds'].append({'cmd': 'y', 'prompt':''})
        cmds['cmds'].append({'cmd': chr(26), 'prompt':'\#'})

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._device.load_system()


    def delete(self, file_name):
        self._d.log_info("remove {0}".format(file_name))
        self._update_file()

        delete_cmd = 'delete {0}'.format(file_name)
        cmds = {'cmds':[{'cmd': 'enable'  , 'prompt':'\#'},
                        {'cmd': delete_cmd, 'prompt':''  },
                        {'cmd': 'y'       , 'prompt':'\#'}
                       ]}

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._device.load_system()


    def items(self):
        self._update_file()
        return self._file.items()


    def keys(self):
        self._update_file()
        return self._file.keys()


    def __getitem__(self, filename):
        self._update_file()
        if filename in self._file.keys():
            return self._file[filename]
        raise KeyError('file {0} does not exist'.format(filename))


    def _update_file(self):
        self._d.log_info("_update_file")
        self._file = OrderedDict()

        # 588 -rw- Jun 10 2014 12:38:10  michele.cfg
        ifre = re.compile('\s+(?P<size>\d+)\s+'
                          '(?P<permission>[^\s]+)\s+'
                          '(?P<month>[^\s]+)\s+'
                          '(?P<day>\d+)\s+'
                          '(?P<year>\d+)\s+'
                          '(?P<hhmmss>[^\s]+)\s+'
                          '(?P<file_name>[^\s]+)')
        for line in self._device.cmd("dir").split('\n'):
            m = ifre.match(line)
            self._d.log_info("read {0}".format(line))
            if m:
                key = m.group('file_name')
                self._file[key] = {'size': m.group('size'),
                                   'permission': m.group('permission'),
                                   'month': m.group('month'),
                                   'day': m.group('day'),
                                   'year': m.group('year'),
                                   'hhmmss': m.group('hhmmss')
                                  }
                self._file[key] = dict(self._file[key].items() + self._file_config[key].items())
        self._d.log_debug("File {0}".format(pformat(json.dumps(self._file))))