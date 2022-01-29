#!/bin/bash
cd /restartHeater
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git pull 
/usr/bin/env python3 /restartHeater/restartHeater.py