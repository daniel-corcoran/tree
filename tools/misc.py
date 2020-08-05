import os
def default_app():
    with open('database/default_app') as f:
        default_app = f.readline()
    return default_app
def list_apps():
    list_of_apps = os.listdir('programs')
    new_l = []
    for x in list_of_apps:
        if x != "__pycache__" and x != default_app:
            new_l.append(x)
    return new_l