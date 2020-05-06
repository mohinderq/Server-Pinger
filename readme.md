# Requirements

- Python 3+ (I am using 3.7)
- Pip3 (Comes with Python on Windows)

# How to run

1. Git clone this repository.
2. Run `pip3 install -r requirements.txt` 
(this will install all libraries)
3. On line 42 of `main.py` add your API-key
4. On line 43 of `main.py` add your chat ID.
5. Now run the script with your favorite terminal

## Command line arguments

`--interval` (Default 10) Pings all the servers every X seconds

`--timeout` (Default 30) After a change in connection checks again after X seconds

`--ip` The ip addresses to ping (seperated by ,)

## Example usage

`python3 main.py --ip 127.0.0.1,127.0.0.2 --interval 100 --timeout 30`

To exit the script use `CTRL + C`
