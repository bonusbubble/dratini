def draw_window(screen_width: int, screen_height: int):
    clear_background(BLACK)
    draw_text("Hello, Dratini!", screen_width / 2, screen_height / 2, 20, PINK)


_screen_width: auto = 640
_screen_height: auto = 480
_screen_title: auto = "Dratini App"

init_window(_screen_width, _screen_height, _screen_title)

set_target_fps(60)

while not window_should_close():
    begin_drawing()
    draw_window(_screen_width, _screen_height)
    end_drawing()

close_window()
