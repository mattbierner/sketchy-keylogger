
def draw_axis(t, screen_width, screen_height, origin=(0, 0)):
    t.up()
    t.setpos(origin[0], origin[1])
    t.down()
    t.setpos(screen_width / 2, origin[1])
    t.setpos(-screen_width / 2, origin[1])
    t.setpos(origin[0], origin[1])
    t.setpos(origin[0], screen_height / 2)
    t.setpos(origin[0], -screen_height / 2)
    t.up()
