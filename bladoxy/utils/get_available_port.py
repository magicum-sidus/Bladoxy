import subprocess

def get_available_port(start_port=1080):
    port = start_port
    print(f"Initial Shadowsocks port check starts at: {port}")

    while True:
        # Check if the port is in use
        result = subprocess.run(
            ['ss', '-tuln'],
            capture_output=True,
            text=True
        )
        if f":{port} " not in result.stdout:
            print(f"Port {port} is available.")
            break
        else:
            print(f"Port {port} is already in use.")
            port += 1

    # Output the first available port
    print(f"The first available port is {port}.")
    return port

if __name__ == "__main__":
    get_available_port()