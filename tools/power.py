# Here we make OS calls to power off, or restart, the device.

import os
# FIXME: This is not secure. We don't want users to have sudo access.

def power_off():
    p = os.system('echo %s|sudo -S %s' % ('tree2020', '( sleep 5 ; shutdown ) & '))
    print(p)

def reboot():
    p = os.system('echo %s|sudo -S %s' % ('tree2020', '( sleep 5 ; shutdown ) & '))
    print(p)