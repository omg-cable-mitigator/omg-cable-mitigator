import tkinter as tk
import sys
import os
import time
import json

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Construct file paths using os.path.join
base_path = config['base_path']
log_path = os.path.join(base_path, config['log_paths']['gui_log'])
eject_log_path = os.path.join(base_path, config['log_paths']['eject_log'])
gui_pid_path = os.path.join(base_path, config['file_paths']['gui_pid'])
command_txt_path = os.path.join(base_path, config['file_paths']['command_txt'])
pin_txt_path = os.path.join(base_path, config['file_paths']['pin_txt'])
security_mode_path = os.path.join(base_path, config['file_paths']['security_mode_txt'])
default_icon = os.path.join(base_path, config['icon_paths']['default_icon'])
default_icon_green = os.path.join(base_path, config['icon_paths']['default_icon_green'])
options_icon = os.path.join(base_path, config['icon_paths']['options_icon'])
finger_icons = [os.path.join(base_path, fname) for fname in config['icon_paths']['finger_icons']]

animation_active = False
current_image_index = 0
current_image_count = 0
finger_delay = 400
btn_style = {"bg": "#9d887b", "fg": "black", "activebackground": "#972b2b", "highlightthickness": 0, "borderwidth": 5, "padx": 15, "pady": 5}
btn_style_success = {"bg": "#9d887b", "fg": "black", "activebackground": "green", "highlightthickness": 0, "borderwidth": 5, "padx": 15, "pady": 5}
textbox_style = {"bg": "#9d887b", "fg": "black", "insertbackground": "white", "insertwidth": 2, "selectbackground": "#32cd52", "highlightthickness": 0, "borderwidth": 5, "padx": 15, "pady": 5}

def save_pid_to_txt():
    with open(gui_pid_path, 'a') as f:
        f.write(str(os.getpid()))

def write_to_command_txt(root, command):
    with open(command_txt_path, 'a') as f:
        f.write(command)

def restore_default_image(root, label):
    image = tk.PhotoImage(file=default_icon)
    label.config(image=image)
    label.image = image
    root.update()

def switch_finger_image(root, label, images):
    global current_image_index, current_image_count, animation_active
    current_image_index = (current_image_index + 1) % len(images)
    image = images[current_image_index]
    label.config(image=image)
    label.image = image
    root.update()
    if current_image_count < 4:
        current_image_count += 1
        root.after(finger_delay, lambda: switch_finger_image(root, label, images))
    else:
        animation_active = False
        current_image_count = 0
        current_image_index = 0
        root.after(finger_delay, lambda: restore_default_image(root, label))

def authenticate(root, label, pin_textbox, unblock_btn, button_frame_top):
    global animation_active
    with open(pin_txt_path, 'r') as f:
        actual_pin = f.read().strip()
    pin = pin_textbox.get("1.0", tk.END).strip()
    if pin == actual_pin:
        write_to_command_txt(root, "unlock_usb_port")
        image = tk.PhotoImage(file=default_icon_green)
        label.config(image=image, background="black")
        label.image = image
        unblock_btn.config(**btn_style_success)
        button_frame_top.config(bg="#15ef27")
        root.update()
        time.sleep(1)
        root.destroy()
    else:
        if not animation_active:
            animation_active = True
            images = [tk.PhotoImage(file=fpath) for fpath in finger_icons]
            root.after(finger_delay, lambda: switch_finger_image(root, label, images))

def on_button_click(number, textbox):
	textbox.config(state="normal")
	count = len(textbox.get("1.0", tk.END))
	if count <= 4:
		textbox.insert(tk.END, str(number))
	textbox.config(state="disabled")

def on_remove_number(textbox):
	textbox.config(state="normal")
	current_content = textbox.get("1.0", tk.END)
	new_content = current_content[:-2]
	textbox.delete("1.0", tk.END)
	textbox.insert(tk.END, new_content)
	textbox.config(state="disabled")

def show_options_menu(main_frame, options_menu_frame):
	main_frame.pack_forget()
	options_menu_frame.pack()

def show_main_menu(options_menu_frame, main_frame):
	options_menu_frame.pack_forget()
	main_frame.pack()

def create_main_menu():
	root = tk.Tk()    
	root.configure(bg="black")
	root.title("O.MG Cable Mitigator")

	window_width = 500
	window_height = 550
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	x = (screen_width // 2) - (window_width // 2)
	y = (screen_height // 2) - (window_height // 2)

	root.geometry(f"{window_width}x{window_height}+{x}+{y}")

	# Frames declaration
	main_frame = tk.Frame(root) 
	options_menu_frame = tk.Frame(root)

	# OPTIONS MENU (hidden on start) #

	options_menu_frame.configure(bg="black")

	radio_button_frame = tk.Frame(options_menu_frame, bg="#972b2b")  
	radio_button_frame.pack(padx=10, pady=10)

	var = tk.StringVar()

	with open(security_mode_path, "r") as file:
		var.set(file.read().strip())

	radio_button1 = tk.Radiobutton(radio_button_frame, text="No Security", variable=var, value="none", **btn_style)
	radio_button1.pack(side=tk.LEFT, padx=5, pady=5)

	radio_button2 = tk.Radiobutton(radio_button_frame, text="Basic Security", variable=var, value="basic", **btn_style)
	radio_button2.pack(side=tk.LEFT, padx=5, pady=5)

	radio_button3 = tk.Radiobutton(radio_button_frame, text="Ultra Security", variable=var, value="ultra", **btn_style)
	radio_button3.pack(side=tk.LEFT, padx=5, pady=5)

	options_image = tk.PhotoImage(file=options_icon)
	options_label = tk.Label(options_menu_frame, image=options_image, background="black")
	options_label.pack()

	options_button_frame = tk.Frame(options_menu_frame, bg="#972b2b")  
	options_button_frame.pack(padx=10, pady=10)

	options_button = tk.Button(options_button_frame, text="Back", command=lambda: show_main_menu(options_menu_frame, main_frame), **btn_style)
	options_button.pack()

	# MAIN MENU #

	main_frame.configure(bg="black")
	main_frame.pack()

	image = tk.PhotoImage(file=default_icon)
	label = tk.Label(main_frame, image=image, background="black")
	label.pack()

	button_frame_top = tk.Frame(main_frame, bg="#972b2b")  
	button_frame_top.pack(padx=10, pady=1)

	pin_textbox = tk.Text(button_frame_top, height=1, width=10, **textbox_style)
	pin_textbox.pack(pady=5, padx=5)
	pin_textbox.config(state="disabled")

	button_frame1 = tk.Frame(main_frame, bg="black")
	button_frame1.pack(padx=10, pady=(5, 10))
	button_frame2 = tk.Frame(main_frame, bg="black")
	button_frame2.pack(padx=10, pady=(5, 10))
	button_frame3 = tk.Frame(main_frame, bg="black")
	button_frame3.pack(padx=10, pady=(5, 10))
	button_frame4 = tk.Frame(main_frame, bg="black")
	button_frame4.pack(padx=10, pady=(5, 10))

	buttons1 = [("1", 1), ("2", 2), ("3", 3)]
	buttons2 = [("4", 4), ("5", 5), ("6", 6)]
	buttons3 = [("7", 7), ("8", 8), ("9", 9)]
	buttons4 = [("0", 0), ("<-", "remove")]

	for text, number in buttons1:
		button = tk.Button(button_frame1, text=text, command=lambda n=number: on_button_click(n, pin_textbox), **btn_style)
		button.pack(side=tk.LEFT, padx=5)
	for text, number in buttons2:
		button = tk.Button(button_frame2, text=text, command=lambda n=number: on_button_click(n, pin_textbox), **btn_style)
		button.pack(side=tk.LEFT, padx=5)
	for text, number in buttons3:
		button = tk.Button(button_frame3, text=text, command=lambda n=number: on_button_click(n, pin_textbox), **btn_style)
		button.pack(side=tk.LEFT, padx=5)
	for text, number in buttons4:
		if text == "<-":
			button = tk.Button(button_frame4, text=text, command=lambda: on_remove_number(pin_textbox), **btn_style)
		else:
			button = tk.Button(button_frame4, text=text, command=lambda n=number: on_button_click(n, pin_textbox), **btn_style)
		button.pack(side=tk.LEFT, padx=5)

	button_frame_bottom = tk.Frame(main_frame, bg="black")
	button_frame_bottom.pack(padx=10, pady=(0, 5))

	options_button = tk.Button(button_frame_bottom, text="Options", command=lambda: show_options_menu(main_frame, options_menu_frame), **btn_style)
	options_button.pack(side=tk.LEFT, padx=5)
	unblock_btn = tk.Button(button_frame_bottom, text="Authenticate", command=lambda:authenticate(root, label, pin_textbox, unblock_btn, button_frame_top), **btn_style)
	unblock_btn.pack(side=tk.LEFT, padx=5)

	root.mainloop()

if __name__ == "__main__":
	f = open(log_path, "a")
	save_pid_to_txt()

	try:
		usb_port_id = sys.argv[1]
		create_main_menu()
	except IndexError:
		print("No usb_port_id supplied via argv", file=f, flush=True)
	finally:
		f.truncate(0)
		f.close()
        

