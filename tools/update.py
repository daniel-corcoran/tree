import os
def update():
    p = os.popen('echo %s|sudo -S %s' % ('UCincy2020!', 'git pull')).read()
    print("P: " , p)
    # Git pulled, now we want to