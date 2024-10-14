# Copyright 2024 Magicum Sidus
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse

from bladoxy.utils.app_actions.init import initialize
from bladoxy.utils.app_actions.cleanup import finalize
from bladoxy.utils.app_actions.run_app import run
from bladoxy.utils.app_actions.stop_app import stop
from bladoxy.utils.app_actions.update_node import update_node
from bladoxy.utils.app_actions.update_profile import update_profile



def main():
    # parser = argparse.ArgumentParser(description="Bladoxy is a linux network assistant.")
    parser = argparse.ArgumentParser(
        description="Bladoxy is a Linux network assistant.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # parser.add_argument("action", help="Select the action you want to perform.",
    #                     choices=["init", "cleanup", "run", "stop", "uptProf","uptNode"])

    parser.add_argument(
        "action", 
        help=(
            "Select the action you want to perform:\n"
            "  init    : Initialize the system.\n"
            "  cleanup : Finalize and clean up resources.\n"
            "  run     : Start the main operations.\n"
            "  stop    : Stop any running processes.\n"
            "  uptProf : Update user profile.\n"
            "  uptNode : Update node configuration."
        ),
        choices=["init", "cleanup", "run", "stop", "uptProf", "uptNode"]
    )
    
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