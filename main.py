import sys
from config import CONFIG
from graphics.pygame_ui import launch_menu
from core.simulation_loop import run_simulation

def main():
    # Launch menu and get user config
    user_config = launch_menu(CONFIG)
    if user_config is None:
        print("Exited from menu.")
        sys.exit(0)
    # Start simulation
    run_simulation(user_config)

if __name__ == "__main__":
    main()
