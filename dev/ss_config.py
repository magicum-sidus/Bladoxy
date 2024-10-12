import os
import shutil
import yaml
import json

def main():
    # 1. Prompt the user to input the configuration file path
    config_path = input("Please enter the path to the configuration file: ")

    # 2. Check if the configuration file exists
    if not os.path.isfile(config_path):
        print("Configuration file does not exist.")
        return

    # 3. Check if the configuration file is valid (Clash YAML configuration file)
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)
    except yaml.YAMLError:
        print("Configuration file is not a valid YAML file.")
        return

    # Check if 'proxies' field has nodes and is valid
    proxies = config_data.get('proxies', [])
    if not proxies:
        print("The configuration file does not contain any proxy nodes.")
        return

    valid = True
    for proxy in proxies:
        if proxy.get('type') != 'ss' or not all(k in proxy for k in ['server', 'port', 'cipher', 'password']):
            valid = False
            break

    if not valid:
        print("The configuration file contains invalid SS nodes.")
        return

    # 4. Copy the configuration file to the profiles directory
    profiles_dir = 'profiles'
    os.makedirs(profiles_dir, exist_ok=True)
    shutil.copy(config_path, profiles_dir)
    print(f"Configuration file has been copied to the {profiles_dir} directory.")

    # 5. Read the configuration file
    with open(config_path, 'r', encoding='utf-8') as file:
        config_data = yaml.safe_load(file)

    # 6. Write the configuration file contents to shadowsocks.json
    shadowsocks_config = {
        "servers": [],
        "local_port": 1080  # Default local port, can be adjusted as needed
    }

    for proxy in proxies:
        shadowsocks_config["servers"].append({
            'server': proxy.get('server'),
            'server_port': proxy.get('port'),
            'method': proxy.get('cipher'),
            'password': proxy.get('password'),
            'timeout': 300,  # Default timeout, can be adjusted as needed
        })

    with open('shadowsocks.json', 'w', encoding='utf-8') as json_file:
        json.dump(shadowsocks_config, json_file, ensure_ascii=False, indent=4)
    
    print("Configuration file has been converted and saved as shadowsocks.json.")

if __name__ == "__main__":
    main()