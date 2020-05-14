import os
def update():
    p = os.system('echo %s|sudo -S %s' % ('UCincy2020!', 'git pull'))
    print("P: " , p)
    # Git pulled, now we want to