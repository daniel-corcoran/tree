import os
def update():
    p = os.system('echo %s|sudo -S %s' % ('tree2020', 'git pull'))
    print(p)
    # Git pulled, now we want to