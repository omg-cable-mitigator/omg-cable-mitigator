import pyudev
import os
import signal
import time
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Construct file paths using os.path.join
base_path = config['base_path']
eject_log_path = os.path.join(base_path, config['eject_log_path'])
gui_pid_path = os.path.join(base_path, config['gui_pid_path'])



def get_gui_pid():
    pid = None
    with open(gui_pid_path, 'r') as f:
        pid = f.read()
    # Clear the .txt file
    with open(gui_pid_path, 'w') as f:
        pass

    return pid

if __name__ == "__main__":
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    # Log
    eject_log_file = open(eject_log_path, "a")
    print("eject_device init", file=eject_log_file, flush=True)

    try:
        for action, device in monitor:
            if action == 'remove':
                pid = get_gui_pid()
                print("GUI detached with process-id:", pid, file=eject_log_file, flush=True)
                # Attempt to gracefully terminate the process
                try:
                    os.kill(int(pid), signal.SIGTERM)
                except ProcessLookupError:
                    # Process already terminated
                    pass
                break
                break
    except Exception as e:
        print("Exception: ", e , file=eject_log_file, flush=True)
        