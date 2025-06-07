#!/bin/bash
pyinstaller --onefile --windowed --icon=assets/favicon.ico --add-data "assets;assets" --paths=lib main.py

