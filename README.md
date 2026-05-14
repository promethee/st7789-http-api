# ST7789 Raspberry Pi Hat HTTP API

A basic http server to display text on a Raspberry Pi, using the WaveShare ST7789 hat.  
Feel free to use this as a basis to do anything else.

## Install  

- Use the `install.sh` script to install the required dependencies from Waveshare
- edit the `/boot/firmware/config.txt` file and add `gpio=6,19,5,26,13,21,20,16=pu` at the end
- Install the dependencies listed in requirements.txt

## Start  

- Start the server with `python main.py`
or
- Make the `main.py` file executable using `sudo chmod +x main.py` and then start it with `./main.py`

## Start at boot  

Make a crontab entry using `crontab -e` with the following line `@reboot  sleep 60 && cd ~/st7789-http-api/ && python main.py 2>&1`

- It can take some time for the server to start, depending on the hardware you use: A Raspberry Pi Zero can take up to a minute of two

## API Routes

```
/                       default route, return the available routes
/clear                  clear the screen
/flash                  flash the screen 3 times to get user attention
/rotation/[angle]       set the current screen rotation, angle must be 0/90/180/270
/text/[text]            display the provided text on the screen
```
