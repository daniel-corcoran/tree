# Switch the current running application
def switch(target):
    with open("database/default_app", 'w') as f:
        if '.x' == target[-2:]:
            print("got here")
            target = target[:-2]
        f.write(target)