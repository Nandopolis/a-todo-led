# a-todo-led
websocket server and serial client for a-todo-led game

## installation
(additional dependencies)
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
(environment)
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt

## running
PYTHONPATH=$PWD twistd -n ws -p {serial_port}
