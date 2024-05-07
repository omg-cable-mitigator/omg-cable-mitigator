<div align="center">
<h1>omg-cable-mitigator</h1>
  
<b>DVGC25 - Bachelor Thesis</b>

![omg-logo-notext-200x200](https://github.com/omg-cable-mitigator/omg-cable-mitigator/blob/main/src/icons/omg-logo-notext-200x200.png)
  
</div>

## Installation for Linux

* Step 1: Clone the repository
```bash
  git clone https://github.com/omg-cable-mitigator/omg-cable-mitigator.git
```
* Step 2: Update the ```base_path``` inside the ```config.example.json``` file with you specific path and rename it to ```config.json```
* Step 3: Update the path to read the config file inside ```main.py```, ```gui.py``` and ```eject_device.py```
  
* Step 4: Copy and paste below text into the terminal to create service file for background running. *Rememeber to change* ExecStart-path!!
```bash
sudo touch /lib/systemd/system/omg-cable-mitigator.service && sudo bash -c 'cat << EOF > /lib/systemd/system/omg-cable-mitigator.service
[Unit]
Description=OMG Cable Mitigator

[Service]
Type=simple
ExecStart=/usr/bin/python3 path/to/the/program/omg-cable-mitigator/src/main.py

[Install]
WantedBy=multi-user.target
EOF'
```

* Step 5: Start the service file for background running
```bash
sudo bash /path/to/the/program/reset.sh
```

## Authors

- [@vvijk](https://www.github.com/vvijk)
- [@azullstrom](https://github.com/azullstrom)

