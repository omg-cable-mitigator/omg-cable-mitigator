<div align="center">
<h1>omg-cable-mitigator</h1>
  
<b>DVGC25 - Bachelor Thesis</b>

![omg-logo-notext-200x200](https://github.com/vvijk/omg-cable-mitigator/assets/91020676/fc1adb23-d59d-48d1-9985-0894a9d55137)
  
</div>

## Installation for Linux

* Step 1: Clone the repository
```bash
  git clone https://github.com/vvijk/omg-cable-mitigator.git 
```
* Step 2: Create service file for background running
```bash
sudo touch /etc/systemd/system/testing.service && sudo bash -c 'cat << EOF > /etc/systemd/system/testing.service
[Unit]
Description=OMG Cable Mitigator

[Service]
Type=simple
ExecStart=/usr/bin/python3 path/to/the/program/omg-cable-mitigator/main.py

[Install]
WantedBy=multi-user.target
EOF'
```

* Step 3: Start the service file for background running
```bash
sudo /path/to/the/program/reset.sh
```

## Authors

- [@vvijk](https://www.github.com/vvijk)
- [@azullstrom](https://github.com/azullstrom)

