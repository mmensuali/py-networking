import re


def core_ats(dev):
    dev.log_info("core_ats")
    ret = {}

    out = dev.cmd({'cmds': [{'cmd': 'show version', 'prompt': '\#'}]})

    dev.log_debug("show version\n{0}".format(out))

    #
    #        Unit             SW version         Boot version         HW version
    # ------------------- ------------------- ------------------- -------------------
    #         1               3.0.0.44            1.0.1.07            00.01.00

    m = re.search("Unit\s+SW\sversion\s+Boot\sversion\s+HW\sversion\s*\n[^\n]+\n\s+(?P<unit>\d)\s+(?P<version>[\d\.]+)"
                  "\s+(?P<boot_version>[\d\.]+)\s+(?P<hardware_rev>[\d\.]+)", out)

    if m:
        ret['os'] = 'ats'
        ret['version'] = m.group('version')
        ret['boot version'] = m.group('boot_version')
        ret['hardware_rev'] = m.group('hardware_rev')
    else:
        return ret

    ret['boot config'] = 'startup-config'
    dev.sw_version = ret['version']
    dev.boot_version = ret['boot version']

    out = dev.cmd({'cmds': [{'cmd': 'show system', 'prompt': '\#'}]})
    dev.log_debug("show system\n{0}".format(out))

    #
    # Unit        Type
    # ---- -------------------
    #  1     AT-8000S/24
    #
    #
    # Unit     Up time
    # ---- ---------------
    #  1     00,04:56:34
    #
    # Unit Number:   1
    # Serial number:

    m = re.search("\nUnit\s+Type\s*\n[^\n]+\n\s+\d\s+(?P<model>[^\s]+)\s*\n", out)
    if m:
        ret['model'] = m.group('model')
        dev.model = ret['model']
    else:
        ret['model'] = 'not found'
        dev.log_warn("cannot capture model")

    m = re.search("\nUnit\s+Up\s+time\s*\n[^\n]+\n\s+\d\s+(?P<time>[^\s]+)\s*\n", out)
    if m:
        days = m.group('time').split(',')[0]
        int_d = int(days)
        hours = m.group('time').split(',')[1]
        ret['sysuptime'] = '{0} days {1}'.format(int_d, hours)
    else:
        ret['sysuptime'] = 'not found'

    m = re.search("\nUnit\s+Number:\s+(?P<unit_number>[^\s]+)\s*\n", out)
    if m:
        ret['unit_number'] = m.group('unit_number')
    else:
        ret['unit_number'] = 'not found'
        dev.log_warn("cannot capture unit number")

    m = re.search("\nSerial\s+number:\s+(?P<serial_number>[^\s]*)\s*\n", out)
    if m:
        ret['serial_number'] = m.group('serial_number')
    else:
        ret['serial_number'] = 'not found'
        dev.log_warn("cannot capture serial number")

    out = dev.cmd({'cmds': [{'cmd': 'show system unit 1', 'prompt': '\#'}]})
    dev.log_debug("show system\n{0}".format(out))

    # System Description:                       ATI AT-8000S
    # System Up Time (days,hour:min:sec):       00,00:02:34
    # System Contact:
    # System Name:                              nac_dev
    # System Location:
    # System MAC Address:                       00:15:77:30:36:00
    # System Object ID:                         1.3.6.1.4.1.207.1.4.126
    # Serial number:
    # Type:                                     AT-8000S/24
    #

    m = re.search("\nSystem\s+Contact:\s+(?P<sys_contact>[^\s]*)\s*\n", out)
    if m:
        ret['system contact'] = m.group('sys_contact')
    else:
        ret['system contact'] = 'not found'
    m = re.search("\nSystem\s+Name:\s+(?P<sys_name>[^\s]*)\s*\n", out)
    if m:
        ret['system name'] = m.group('sys_name')
    else:
        ret['system name'] = 'not found'
    m = re.search("\nSystem\s+Location:\s+(?P<sys_loc>[^\s]*)\s*\n", out)
    if m:
        ret['system location'] = m.group('sys_loc')
    else:
        ret['system location'] = 'not found'


    return ret
