# Here we make OS calls to power off, or restart, the device.
import os
import sys
import psutil
import logging
from tools.buzzer import disable_buzzer
import os
# FIXME: This is not secure. We don't want users to have sudo access.

def power_off():
    p = os.system('echo %s|sudo -S %s' % ('mendel', 'sleep 5 && shutdown now & '))
    print(p)

def reboot():
    disable_buzzer()
    p = os.system('echo %s|sudo -S %s' % ('mendel', ' sleep 5 && reboot & '))
    print(p)



def restart_client():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)