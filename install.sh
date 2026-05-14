#!/bin/sh
cd ~/
sudo apt-get install p7zip-full -y
wget https://files.waveshare.com/upload/b/bd/1.3inch_LCD_HAT_code.7z
7z x 1.3inch_LCD_HAT_code.7z -r -o./1.3inch_LCD_HAT_code
sudo chmod 777 -R 1.3inch_LCD_HAT_code
cp ~/1.3inch_LCD_HAT_code/1.3inch_LCD_HAT_code/python/ST7789.py ~/st7789-http-api
cp ~/1.3inch_LCD_HAT_code/1.3inch_LCD_HAT_code/python/config.py ~/st7789-http-api
cp ~/1.3inch_LCD_HAT_code/1.3inch_LCD_HAT_code/python/pic.jpg ~/st7789-http-api
