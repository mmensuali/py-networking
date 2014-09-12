import pytest
from pynetworking import Device, DeviceException
from time import sleep
from paramiko.rsakey import RSAKey
from mock import MagicMock
from mock import patch
import yaml
import zmq


def setup_dut(dut):
    dut.reset()
    dut.add_cmd({'cmd':'show version',        'state':-1, 'action': 'PRINT','args':["""
AlliedWare Plus (TM) 5.4.2 09/25/13 12:57:26

Build name : x600-5.4.2-3.14.rel
Build date : Wed Sep 25 12:57:26 NZST 2013
Build type : RELEASE
    """]})


# def test_vlan_for_mock_classes(dut, log_level):
#     output_sr = ["""
# !
# interface port1.0.1-1.0.50
# switchport
# switchport mode access
# !
# vlan database
# vlan 7 name admin state enable
# vlan 8-100 mtu 1200
# vlan 6,7 mtu 1000
# !
# end
#     """]
#     output_sv = ["""
# VLAN ID  Name            Type    State   Member ports
#                                          (u)-Untagged, (t)-Tagged
# ======= ================ ======= ======= ====================================
# 1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
#                                          port1.0.4(u) port1.0.5(u) port1.0.6(u)
#                                          port1.0.7(u) port1.0.8(u) port1.0.9(u)
#                                          port1.0.10(u) port1.0.11(u)
#                                          port1.0.12(t) port1.0.13(u)
#                                          port1.0.14(u) port1.0.15(u)
#                                          port1.0.16(u) port1.0.17(u)
#                                          port1.0.18(u) port1.0.19(u)
#                                          port1.0.20(t) port1.0.21(u)
#                                          port1.0.22(u) port1.0.23(u)
#                                          port1.0.24(u) port1.0.25(u)
#                                          port1.0.26(u) port1.0.27(u)
#                                          port1.0.28(u) port1.0.29(u)
#                                          port1.0.31(u)
#                                          port1.0.32(u) port1.0.33(u)
#                                          port1.0.34(u) port1.0.35(u)
#                                          port1.0.36(u) port1.0.37(u)
#                                          port1.0.38(u) port1.0.39(u)
#                                          port1.0.40(u) port1.0.41(u)
#                                          port1.0.44(u) port1.0.45(u)
#                                          port1.0.46(u) port1.0.47(u)
#                                          port1.0.48(u) port1.0.49(u)
#                                          port1.0.50(u)
# 7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
#     """]
#
#     setup_dut(dut)
#
#     dut.add_cmd({'cmd': 'show running-config', 'state':0, 'action': 'PRINT','args':output_sr})
#     dut.add_cmd({'cmd': 'show vlan all'      , 'state':0, 'action': 'PRINT','args':output_sv})
#
#     d=MagicMock()
#     d.open()
#     d.close()
#
#
# def test_vlan_for_mock_methods(dut, log_level):
#     output_sr = ["""
# !
# interface port1.0.1-1.0.50
# switchport
# switchport mode access
# !
# vlan database
# vlan 7 name admin state enable
# vlan 8-100 mtu 1200
# vlan 6,7 mtu 1000
# !
# end
#     """]
#     output_sv = ["""
# VLAN ID  Name            Type    State   Member ports
#                                          (u)-Untagged, (t)-Tagged
# ======= ================ ======= ======= ====================================
# 1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
#                                          port1.0.4(u) port1.0.5(u) port1.0.6(u)
#                                          port1.0.7(u) port1.0.8(u) port1.0.9(u)
#                                          port1.0.10(u) port1.0.11(u)
#                                          port1.0.12(t) port1.0.13(u)
#                                          port1.0.14(u) port1.0.15(u)
#                                          port1.0.16(u) port1.0.17(u)
#                                          port1.0.18(u) port1.0.19(u)
#                                          port1.0.20(t) port1.0.21(u)
#                                          port1.0.22(u) port1.0.23(u)
#                                          port1.0.24(u) port1.0.25(u)
#                                          port1.0.26(u) port1.0.27(u)
#                                          port1.0.28(u) port1.0.29(u)
#                                          port1.0.31(u)
#                                          port1.0.32(u) port1.0.33(u)
#                                          port1.0.34(u) port1.0.35(u)
#                                          port1.0.36(u) port1.0.37(u)
#                                          port1.0.38(u) port1.0.39(u)
#                                          port1.0.40(u) port1.0.41(u)
#                                          port1.0.44(u) port1.0.45(u)
#                                          port1.0.46(u) port1.0.47(u)
#                                          port1.0.48(u) port1.0.49(u)
#                                          port1.0.50(u)
# 7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
#     """]
#
#     setup_dut(dut)
#
#     dut.add_cmd({'cmd': 'show running-config', 'state':0, 'action': 'PRINT','args':output_sr})
#     dut.add_cmd({'cmd': 'show vlan all'      , 'state':0, 'action': 'PRINT','args':output_sv})
#
#     d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
#     d.open = MagicMock()
#     d.close = MagicMock()
#     d.open()
#     d.close()
#
#
# def test_log(dut, log_level):
#     output_sr = ["""
# !
# interface port1.0.1-1.0.50
# switchport
# switchport mode access
# !
# vlan database
# vlan 7 name admin state enable
# vlan 8-100 mtu 1200
# vlan 6,7 mtu 1000
# !
# end
#     """]
#     output_sv = ["""
# VLAN ID  Name            Type    State   Member ports
#                                          (u)-Untagged, (t)-Tagged
# ======= ================ ======= ======= ====================================
# 1       default          STATIC  ACTIVE  port1.0.1(u) port1.0.2(u) port1.0.3(u)
#                                          port1.0.4(u) port1.0.5(u) port1.0.6(u)
#                                          port1.0.7(u) port1.0.8(u) port1.0.9(u)
#                                          port1.0.10(u) port1.0.11(u)
#                                          port1.0.12(t) port1.0.13(u)
#                                          port1.0.14(u) port1.0.15(u)
#                                          port1.0.16(u) port1.0.17(u)
#                                          port1.0.18(u) port1.0.19(u)
#                                          port1.0.20(t) port1.0.21(u)
#                                          port1.0.22(u) port1.0.23(u)
#                                          port1.0.24(u) port1.0.25(u)
#                                          port1.0.26(u) port1.0.27(u)
#                                          port1.0.28(u) port1.0.29(u)
#                                          port1.0.31(u)
#                                          port1.0.32(u) port1.0.33(u)
#                                          port1.0.34(u) port1.0.35(u)
#                                          port1.0.36(u) port1.0.37(u)
#                                          port1.0.38(u) port1.0.39(u)
#                                          port1.0.40(u) port1.0.41(u)
#                                          port1.0.44(u) port1.0.45(u)
#                                          port1.0.46(u) port1.0.47(u)
#                                          port1.0.48(u) port1.0.49(u)
#                                          port1.0.50(u)
# 7       VLAN0007         STATIC  ACTIVE  port1.0.28(t) port1.0.29(u)
#     """]
#
#     setup_dut(dut)
#
#     dut.add_cmd({'cmd': 'show running-config', 'state':0, 'action': 'PRINT','args':output_sr})
#     dut.add_cmd({'cmd': 'show vlan all'      , 'state':0, 'action': 'PRINT','args':output_sv})
#
#     # THE SW HERE BELOW WOULD GIVE AN ERROR IF INVOKED
#     # d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
#     # d.log_level(33)
#     # d.open()
#     # d.close()
#
#     # THE SW HERE BELOW DO NOT GIVE ANY ERROR IF INVOKED BECAUSE OF THE MOCK
#     Device.log_level = MagicMock()
#     d=Device(host=dut.host,port=dut.port,protocol=dut.protocol, log_level=log_level)
#     d.log_level(33)
#     d.log_level.assert_called_once_with(33)
#     d.open()
#     d.close()
#
#
# def test_ping_failure_1(dut, log_level):
#     setup_dut(dut)
#
#     # Mock a failed ping as the device was unexisting on EVERY instance of the Device class
#     ping_mck = MagicMock()
#     ping_mck.return_value = False
#     Device.ping = ping_mck
#
#     d=Device(host=dut.host,port=dut.port,protocol=dut.protocol,log_level=log_level)
#     d.open()
#     assert d.ping() == False
#     d.ping.assert_called_once()
#     d.close()
#
#
# def test_ping_failure_2(dut, log_level):
#     setup_dut(dut)
#
#     # Mock a failed ping as the device was unexisting on a particular instance of the Device class
#     ping_mck = MagicMock()
#     ping_mck.return_value = False
#
#     d=Device(host=dut.host,port=dut.port,protocol=dut.protocol,log_level=log_level)
#     d.ping = ping_mck
#     d.open()
#     assert d.ping() == False
#     d.ping.assert_called_once()
#     d.close()
#
#
def test_load_system(dut, log_level):
    setup_dut(dut)

    with patch('yaml.load') as MockClass:
        models = {'features': None, 'system': None}
        yaml_mck = MagicMock()
        yaml_mck.return_value = models
        yaml.load = yaml_mck

        d=Device(host=dut.host,port=dut.port,protocol=dut.protocol,log_level=log_level)
        with pytest.raises(ImportError) as excinfo:
            d.open()
        assert str(excinfo.value) == 'No module named None'


def test_load_features(dut, log_level):
    setup_dut(dut)

    with patch('yaml.load') as MockClass:
        yaml_mck = MagicMock()
        yaml_mck.return_value = None
        yaml.load = yaml_mck

        d=Device(host=dut.host, port=dut.port, protocol=dut.protocol, log_level=log_level)

        models = {'system': 'awp_system', 'features': {'dhcp': 'awp_dhcp'}}
        yaml_mck.return_value = models
        with pytest.raises(ImportError) as excinfo:
            d.open()
        assert str(excinfo.value) == 'No module named awp_dhcp'

        models = None
        yaml_mck.return_value = models
        with pytest.raises(AttributeError) as excinfo:
            d.open()
        assert str(excinfo.value) == '\'Device\' object has no attribute \'system\''

        models = {'features': None}
        yaml_mck.return_value = models
        with pytest.raises(AttributeError) as excinfo:
            d.open()
        assert str(excinfo.value) == '\'Device\' object has no attribute \'system\''


def test_timeout(dut, log_level):
    setup_dut(dut)

    with patch('zmq.Poller.poll') as MockClass:
        # Timeout mocked returning an empty string, as the device had not answered
        poll_mck = MagicMock()
        poll_mck.return_value = ''
        zmq.Poller.poll = poll_mck

        d=Device(host=dut.host,port=dut.port,protocol=dut.protocol,log_level=log_level)
        with pytest.raises(DeviceException) as excinfo:
            d.open()
        assert str(excinfo.value).startswith("proxy exited with error")


def test_last(dut, log_level):
    setup_dut(dut)
    d=Device(host=dut.host,port=dut.port,protocol=dut.protocol,log_level=log_level)
    d.open()
    d.close()
