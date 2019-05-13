# a-todo-led
websocket server and serial client for a-todo-led game

## installation
### additional dependencies
```bash
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
```
### environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
```
## running
*replace "/dev/ttyUSB0" with the serial port*
```bash
PYTHONPATH=$PWD twistd -n ws -p /dev/ttyUSB0
```
