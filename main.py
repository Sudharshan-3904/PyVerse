import sys
from config import CONFIG
from graphics.pygame_ui import launch_menu

def main():
    # Launch menu and run simulation
    launch_menu(CONFIG)

if __name__ == "__main__":
    main()
