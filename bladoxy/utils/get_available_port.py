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


import subprocess

from bladoxy.utils.logger import logger

def get_available_port(start_port=1080):
    port = start_port


    while True:
        # Check if the port is in use
        result = subprocess.run(
            ['ss', '-tuln'],
            capture_output=True,
            text=True
        )
        if f":{port} " not in result.stdout:
            logger.info(f"端口 {port} 可用")
            break
        else:
            logger.info(f"端口 {port} 已经被占用")
            port += 1

    return port

if __name__ == "__main__":
    get_available_port()