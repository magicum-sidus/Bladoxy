import argparse

from bladoxy.utils.app_actions.init import initialize
from bladoxy.utils.app_actions.cleanup import finalize
from bladoxy.utils.app_actions.run_app import run
from bladoxy.utils.app_actions.stop_app import stop
from bladoxy.utils.nodes import change_node
from bladoxy.utils.nodes import add_profile



def main():
    parser = argparse.ArgumentParser(description="Bladoxy is a linux network assistant.")
    parser.add_argument("action", help="Select the action you want to perform.",
                        choices=["init", "cleanup", "run", "stop", "addProf","chgNode"])
    
    args = parser.parse_args()

    action_map = {
        "init": initialize,
        "cleanup": finalize,
        "run": run,
        "stop": stop,
        "addProf": add_profile,
        "chgNode": change_node
    }

    action_function = action_map.get(args.action)
    if action_function:
        action_function()

if __name__ == "__main__":
    main()