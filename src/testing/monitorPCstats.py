import os 
import psutil
import time

def get_system_status():
	cpu_percent = psutil.cpu_percent(interval=1)

	memory = psutil.virtual_memory()
	memory_percent = memory.percent

	disk = psutil.disk_usage('/')
	disk_percent = disk.percent

	network = psutil.net_io_counters()
	sent_bytes = network.bytes_sent
	received_bytes = network.bytes_recv

	os.system('clear' if os.name == 'posix' else 'cls')

	print("CPU Usage: {}".format(cpu_percent))
	print("Memory Usage: {}".format(memory_percent))
	print("Disk Usage: {}".format(disk_percent))
	print("Bytes sent: {}".format(sent_bytes))
	print("Bytes received: {}".format(received_bytes))
	
if __name__ == '__main__':
    print("Ctrl + c to exit..")
    try:
        while True:
            get_system_status()
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
