import time
import evdev
import subprocess
import os
import re
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

base_path = config['base_path']
username = config['user_settings']['username']
display = config['user_settings']['display']

# Define file paths
command_path = os.path.join(base_path, 'command.txt')
gui_script_path = os.path.join(base_path, 'gui.py')
eject_device_script_path = os.path.join(base_path, 'eject_device.py')
gui_pid_path = os.path.join(base_path, 'gui_pid.txt')
security_mode_path = os.path.join(base_path, 'security-mode.txt')


def read_from_command_txt():
	with open(command_path, 'r') as f:
		command = f.read()
		print(command, flush=True)
	# Clear the .txt file
	with open(command_path, 'w') as f:
		pass
	return command

def get_connected_devices():
	devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
	return devices

def get_connected_keyboards():
	devices = get_connected_devices()
	key_devices = [device for device in devices if evdev.ecodes.EV_KEY in device.capabilities()]
	return key_devices

def get_usb_sysfs_path(input_dev_path):
    # Traverse the sysfs filesystem to find the USB sysfs path corresponding to the input device
    input_dev_sysfs_path = os.path.realpath(f"/sys/class/input/{os.path.basename(input_dev_path)}")
    usb_dev_sysfs_path = os.path.dirname(input_dev_sysfs_path)
    return usb_dev_sysfs_path

def block_usb_port(usb_port_id):
	if usb_port_id != int:
		return
	subprocess.run(['sudo', 'sh', '-c', f'echo "{usb_port_id}" > /sys/bus/usb/drivers/usb/unbind'])

def unblock_usb_port(usb_port_id):
	if usb_port_id != int:
		return
	subprocess.run(['sudo', 'sh', '-c', f'echo "{usb_port_id}" > /sys/bus/usb/drivers/usb/bind'])

def run_gui_script(usb_port_id):
	print("show_gui", flush=True)

	if display:
		# In the cmd variable DISPLAY and XDG_RUNTIME_DIR is needed to tell the script what to draw on.
		# TODO extract the Wayland (or X11) display number with function to make it more dynamic. Same with username
		cmd = f"DISPLAY={display} XDG_RUNTIME_DIR=/run/user/$(id -u {username}) sudo -u {username} dbus-run-session -- python3 {gui_script_path} {usb_port_id}"
		try:
			subprocess.run(cmd, shell=True)
		except Exception as e:
			print(f"Failed to display GUI: {e}")
	else:
		print("Could not find display or xauthority")

def run_eject_device_script():
	cmd = f"sudo -u {username} dbus-run-session -- python3 {eject_device_script_path}"
	try:
		subprocess.Popen(cmd, shell=True)
	except Exception as e:
		print(f"Failed to start eject_device.py: {e}", flush=True)

# BASIC MODE
def monitor_keyboards():
	connected_key_devices = get_connected_keyboards()

	while True:
		time.sleep(1)
		new_key_devices = get_connected_keyboards()

		if new_key_devices != connected_key_devices:
			for key_device in new_key_devices:
				if key_device not in connected_key_devices and "Consumer" not in key_device.name and "Control" not in key_device.name:
					usb_path = get_usb_sysfs_path(key_device.path)
					# Extract the USB port ID
					pattern = r'/usb\d/(\d+-\d+)/'
					match = re.search(pattern, usb_path)
					usb_port_id = match.group(1)
					
					try:
						key_device = evdev.InputDevice(key_device.path)
						for key_event in key_device.read_loop():
							if(key_event):
								block_usb_port(usb_port_id)
								run_eject_device_script()
								run_gui_script(usb_port_id)
								command = read_from_command_txt()

								if command == "unlock_usb_port":
									unblock_usb_port(usb_port_id)

								break
					except Exception as e:
						print("Exception occurred:", e)
							
		connected_key_devices = new_key_devices

# ULTRA MODE
def monitor_usb():
	connected_devices = get_connected_devices()

	while True:
		time.sleep(1)
		new_devices = get_connected_devices()
		deviceNotFound = True

		if new_devices != connected_devices:
			print("[USB device activity noticed]")
			for device in new_devices:
				if device not in connected_devices and deviceNotFound:
					deviceNotFound = False
					usb_path = get_usb_sysfs_path(device.path)
					# Extract the USB port ID
					pattern = r'/usb\d/(\d+-\d+)/'
					match = re.search(pattern, usb_path)
					usb_port_id = match.group(1)

					try:
						block_usb_port(usb_port_id)
						run_eject_device_script()
						run_gui_script(usb_port_id)
						command = read_from_command_txt()

						if command == "unlock_usb_port":
							unblock_usb_port(usb_port_id)
					except Exception as e:
						print("Exception occurred:", e)
							
		connected_devices = new_devices

def clear_txts():
    with open(gui_pid_path, 'w') as f:
        pass

def init(security_mode):
	clear_txts()

	if security_mode == "none":
		print("none")
	elif security_mode == "basic":
		monitor_keyboards()
	elif security_mode == "ultra":
		monitor_usb()
	else:
		print("error security-mode.txt")


if __name__ == "__main__":
	security_mode = None
	
	with open(security_mode_path, "r") as file:
		security_mode = file.read().strip()

	init(security_mode)
