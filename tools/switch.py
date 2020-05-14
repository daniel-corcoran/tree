# Switch the current running application
def switch(target):
    with open("database/default_app", 'w') as f:
        f.write(target)
