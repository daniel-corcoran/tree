import os
def update():
    p = os.popen('echo %s|sudo -S %s' % ('tree2020', 'git pull')).read()
    return p
    # Git pulled, now we want to