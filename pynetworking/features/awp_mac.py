# -*- coding: utf-8 -*-
from pynetworking import Feature
from pprint import pformat
import re
import json
try:
    from collections import OrderedDict
except ImportError: #pragma: no cover
    from ordereddict import OrderedDict


class awp_mac(Feature):
    """
    mac feature implementation for AWP
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
            re.match("[0-9a-f]{12}", mac.lower())):
            mac = mac.replace('-', '')
            mac = mac.replace(':', '')
            mac = mac.replace('.', '')
            mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
        else:
            raise KeyError('MAC address {0} is not valid'.format(mac))

        if mac in self._d.mac.keys():
            raise KeyError('MAC address {0} is already existing'.format(mac))

        fwd = 'forward'
        if (fwd == False):
           fwd = 'discard'
        set_cmd = 'mac address-table static {0} {1} interface {2} vlan {3}'.format(mac, fwd, interface, vlan)
        cmds = {'cmds': [{'cmd': 'enable', 'prompt': '\#'},
                         {'cmd': 'conf t', 'prompt': '\(config\)\#'},
                         {'cmd': set_cmd , 'prompt': '\(config\)\#'},
                         {'cmd': chr(26) , 'prompt': '\#'}
                        ]}
        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._update_mac()


    def update(self, mac, interface, forward=True, vlan=1):
        self._d.log_info("update MAC address {0} entry".format(mac))
        self._update_mac()

        if (re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) or
            re.match("[0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4}", mac.lower())  or
            re.match("[0-9a-f]{12}", mac.lower())):
            mac = mac.replace('-', '')
            mac = mac.replace(':', '')
            mac = mac.replace('.', '')
            mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
        else:
            raise KeyError('MAC address {0} is not valid'.format(mac))

        if mac not in self._d.mac.keys():
            raise KeyError('MAC address {0} is not existing'.format(mac))

        fwd = 'forward'
        if (fwd == False):
           fwd = 'discard'
        set_cmd = 'mac address-table static {0} {1} interface {2} vlan {3}'.format(mac, fwd, interface, vlan)
        cmds = {'cmds': [{'cmd': 'enable', 'prompt': '\#'},
                         {'cmd': 'conf t', 'prompt': '\(config\)\#'},
                         {'cmd': set_cmd , 'prompt': '\(config\)\#'},
                         {'cmd': chr(26) , 'prompt': '\#'}
                        ]}
        self._device.cmd(cmds, cache=False, flush_cache=True)
        self._update_mac()


    def delete(self, mac=''):
        self._update_mac()

        if (mac == ''):
            self._d.log_info("remove all the entries")
            del_cmd = 'clear mac address-table'
        else:
            self._d.log_info("remove {0}".format(mac))
            if (re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()) or
                re.match("[0-9a-f]{4}([.])[0-9a-f]{4}([.])[0-9a-f]{4}", mac.lower())  or
                re.match("[0-9a-f]{12}", mac.lower())):
                mac = mac.replace('-', '')
                mac = mac.replace(':', '')
                mac = mac.replace('.', '')
                mac = mac[0:4] + '.' + mac[4:8] + '.' + mac[8:12]
            else:
                raise KeyError('MAC address {0} is not valid'.format(mac))
            if mac not in self._d.mac.keys():
                raise KeyError('mac {0} is not existing'.format(mac))
            if self._d.mac[mac].type == 'dynamic':
                raise KeyError('cannot remove a dynamic entry')

            fwd = 'forward'
            if self._d.mac[mac]['forward'] == False:
                fwd = 'discard'
            interface = self._d.mac[mac]['interface']
            vlan = self._d.mac[mac]['vlan']
            del_cmd = 'no mac address-table static {0} {1} interface {2} vlan {3}'.format(mac, fwd, interface, vlan)

        cmds = {'cmds':[{'cmd': 'enable', 'prompt':'\#'},
                        {'cmd': 'conf t', 'prompt':'\(config\)\#'},
                        {'cmd': del_cmd , 'prompt':'\(config\)\#'},
                        {'cmd': chr(26) , 'prompt':'\#'}
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

        # 1    port1.0.1    0000.cd1d.7eb0   forward   dynamic

        ifre = re.compile('\s+(?P<vlan>\d+)\s+'
                          '(?P<interface>[^\s]+)\s+'
                          '(?P<mac>[^\s]+)\s+'
                          '(?P<action>[^\s]+)\s+'
                          '(?P<type>[^\s]+)')
        for line in self._device.cmd("show mac address-table").split('\n'):
            self._d.log_debug("line is {0}".format(line))
            m = ifre.match(line)
            if m:
                key = m.group('mac')
                self._mac[key] = {'vlan': m.group('vlan'),
                                  'interface': m.group('interface'),
                                  'action': m.group('action'),
                                  'type': m.group('type')
                                 }
        self._d.log_debug("mac {0}".format(pformat(json.dumps(self._mac))))