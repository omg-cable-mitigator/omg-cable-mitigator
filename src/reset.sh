#!/bin/bash

sudo systemctl daemon-reload
sudo systemctl start omg-cable-mitigator.service
sudo systemctl enable omg-cable-mitigator.service
sudo systemctl restart omg-cable-mitigator.service
sudo systemctl status omg-cable-mitigator.service
