.. _system-section:

System
******
System class implements device dependent functions and it's used by the Device class to do device specific
operations. This chapter is not intended for the library user but for developer that want to add support for new devices.

Methods
-------

**get_config**
""""""""""""""
**Mandatory**

**Description**: Returns a string representing the full device configuration.

**ping**
""""""""""""""
**Mandatory**

**Description**: Returns True if the device is online.

**save_config**
"""""""""""""""
**Mandatory**

**Description**: Allows to save the running configuration in the flash memory, so to survive in case of reboot.

**shell_init**
""""""""""""""
**Optional**

**Description**: Returns a list of dictionaries representing the commands that need to be executed on the device when a
shell is opened. For example the command output pagination should be disable to avoid that commands that generate long
output stop waiting user input.

**shell_prompt**
""""""""""""""""
**Optional**

**Description**: Returns a regular expression for the default prompt of the device.

**update_firmware(filename, protocol='http', server=None)**
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
**Mandatory**

**Description**: Allows to upgrade the device firmware.
The *filename* is the name of the file and its optional path that contains the device firmware.
The *protocol* is the method used to upload the firmware to the device. Depending on the device capability can be set to http or tftp.
In case of tftp it requires an external server that must be indicated in the *server* parameter.

**Parameters**:

   - *name*: string
       Filename of the device firmware

   - *server*: string
       Server IP address or Hostname
