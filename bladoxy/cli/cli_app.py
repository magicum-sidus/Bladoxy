import argparse

from bladoxy.utils.app_actions.init import initialize
from bladoxy.utils.app_actions.cleanup import finalize
from bladoxy.utils.app_actions.run_app import run
from bladoxy.utils.app_actions.stop_app import stop
from bladoxy.utils.app_actions.update_node import update_node
from bladoxy.utils.app_actions.update_profile import update_profile



def main():
    parser = argparse.ArgumentParser(description="Bladoxy is a linux network assistant.")
    parser.add_argument("action", help="Select the action you want to perform.",
                        choices=["init", "cleanup", "run", "stop", "uptProf","uptNode"])
    
    args = parser.parse_args()

    action_map = {
        "init": initialize,
        "cleanup": finalize,
        "run": run,
        "stop": stop,
        "uptProf": update_profile,
        "uptNode": update_node
    }

    action_function = action_map.get(args.action)
    if action_function:
        action_function()

if __name__ == "__main__":
    main()