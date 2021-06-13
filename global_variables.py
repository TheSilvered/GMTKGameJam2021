gravity = 1.5
current_level = 0

def switch_grav():
    global gravity
    gravity = -gravity

def next_level():
    global current_level
    current_level += 1
