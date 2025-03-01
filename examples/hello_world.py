screen_width: int = 800
screen_height: int = 450

InitWindow(screen_width, screen_height, "Dratini App")

SetTargetFPS(60)

while not WindowShouldClose():
    BeginDrawing()
    ClearBackground(BLACK)
    DrawText("Hello, Dratini!", 190, 200, 20, PINK)
    EndDrawing()

CloseWindow()
