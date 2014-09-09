# -*- coding: utf-8 -*-
from pynetworking import Feature
from pprint import pformat
import re
import json
try:
    from collections import OrderedDict
except ImportError: #pragma: no cover
    from ordereddict import OrderedDict


class ats_mac(Feature):
    """
    mac feature implementation for ats
    """
    def __init__(self, device, **kvargs):
        Feature.__init__(self, device, **kvargs)
        self._mac={}
        self._d = device
        self._d.log_debug("loading feature")


    def load_config(self, config):
        self._d.log_info("loading config")


    def create(self, mac, interface, forward=True, vlan=1):
        self._d.log_info("create MAC address {0} entry".format(mac))
        self._update_mac()

        if (re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) or
            re.match("[0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4}", mac.lower())  or
            re.match("[0-9a-f]{12}", x.lower())):
            mac = mac.replace('-', '')
            mac = mac.replace(':', '')
            mac = mac.replace('.', '')
            mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
        else:
            raise KeyError('MAC address {0} is not valid'.format(mac))

        if mac in self._d.mac.keys():
            raise KeyError('MAC address {0} is already existing'.format(mac))

        vlan_cmd = 'interface vlan {0}'.format(vlan)
        set_cmd = 'bridge address {0} ethernet {1} permanent'.format(mac, interface)
        cmds = {'cmds':[{'cmd': 'conf'  , 'prompt':'\(config\)\#'},
                        {'cmd': vlan_cmd, 'prompt':'\(config-if\)\#'},
                        {'cmd': set_cmd , 'prompt':'\(config-if\)\#'},
                        {'cmd': chr(26) , 'prompt':'\#'},
                       ]}
        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._update_mac()


    def update(self, mac, interface, forward=True, vlan=1):
        self._d.log_info("update MAC address {0} entry".format(mac))
        self._update_mac()

        if (re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) or
            re.match("[0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4}", mac.lower())  or
            re.match("[0-9a-f]{12}", x.lower())):
            mac = mac.replace('-', '')
            mac = mac.replace(':', '')
            mac = mac.replace('.', '')
            mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
        else:
            raise KeyError('MAC address {0} is not valid'.format(mac))

        if mac not in self._d.mac.keys():
            raise KeyError('MAC address {0} is not existing'.format(mac))

        vlan_cmd = 'interface vlan {0}'.format(vlan)
        set_cmd = 'bridge address {0} ethernet {1} permanent'.format(mac, interface)
        cmds = {'cmds':[{'cmd': 'conf'  , 'prompt':'\(config\)\#'},
                        {'cmd': vlan_cmd, 'prompt':'\(config-if\)\#'},
                        {'cmd': set_cmd , 'prompt':'\(config-if\)\#'},
                        {'cmd': chr(26) , 'prompt':'\#'},
                       ]}
        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._update_mac()


    def delete(self, mac=''):
        self._update_mac()

        if (mac == ''):
            self._d.log_info("remove all the entries")

            del_cmd = 'clear bridge'
            cmds = {'cmds':[{'cmd': del_cmd , 'prompt':'\#'},
                            {'cmd': chr(26) , 'prompt':'\#'},
                           ]}
        else:
            self._d.log_info("remove {0}".format(mac))

            if mac not in self._d.mac.keys():
                raise KeyError('mac {0} is not existing'.format(mac))
            if self._d.mac[mac].type == 'dynamic':
                raise KeyError('cannot remove a dynamic entry')

            vlan_cmd = 'interface vlan {0}'.format(vlan)
            del_cmd = 'no bridge address {0}'.format(mac)
            cmds = {'cmds':[{'cmd': 'conf'  , 'prompt':'\(config\)\#'},
                            {'cmd': vlan_cmd, 'prompt':'\(config-if\)\#'},
                            {'cmd': del_cmd , 'prompt':'\(config-if\)\#'},
                            {'cmd': chr(26) , 'prompt':'\#'},
                           ]}

        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._update_mac()


    def items(self):
        self._update_mac()
        return self._mac.items()


    def keys(self):
        self._update_mac()
        return self._mac.keys()


    def __getitem__(self, mac):
        self._update_mac()
        if mac not in self._mac.keys():
            raise KeyError('MAC address {0} does not exist'.format(mac))


    def _update_mac(self):
        self._d.log_info("_update_mac")
        self._mac = OrderedDict()

        #   1       00:00:cd:24:04:8b    1/e1   dynamic
        ifre = re.compile('\s+(?P<vlan>\d+)\s+'
                          '(?P<mac>[^\s]+)\s+'
                          '(?P<interface>[^\s]+)\s+'
                          '(?P<type>[^\s]+)')
        for line in self._device.cmd("show bridge address-table").split('\n'):
            m = ifre.match(line)
            if m:
                key = m.group('mac')
                key = key.split(':')[0] + key.split(':')[1] + '.' + key.split(':')[2] + key.split(':')[3] + '.' + key.split(':')[4] + key.split(':')[5]
                self._mac[key] = {'vlan': m.group('vlan'),
                                  'interface': m.group('interface'),
                                  'action': 'forward',
                                  'type': m.group('type')
                                 }
        self._d.log_debug("mac {0}".format(pformat(json.dumps(self._mac))))