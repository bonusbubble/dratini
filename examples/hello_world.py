screen_width: auto = 640
screen_height: auto = 480
screen_title: auto = "Dratini App"

init_window(screen_width, screen_height, "Dratini App")

set_target_fps(60)

while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    draw_text("Hello, Dratini!", screen_width / 2, screen_height / 2, 20, PINK)
    end_drawing()

close_window()
