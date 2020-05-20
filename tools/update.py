import os
def update():
    p = os.popen('echo %s|sudo -S %s' % ('mendel', 'git pull')).read()
    return p
    # Git pulled, now we want to