before = capture_screen()

click(x, y)

after = capture_screen()

if before != after:
    print("Action successful")