import os
def update():
    r = os.system('git pull')
    print(r)
    # Git pulled, now we want to