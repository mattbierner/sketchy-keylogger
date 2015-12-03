
def draw_axis(t, screen_width, screen_height):
    t.up()
    t.home()
    t.down()
    t.setpos(screen_width / 2, 0)
    t.setpos(-screen_width / 2, 0)
    t.setpos(0, 0)
    t.setpos(0, screen_height / 2)
    t.setpos(0, -screen_height / 2)
    t.up()
