# COMPSCI 690U Project

## How to install and start:

Assuming that Python 3 and the BLAST CLI are installed, run the following command to create a virtual environment:

    $ python3 -m venv .venv

Activate the virtual environment with this command:

    $ source .venv/bin/activate

Confirm that the virtual environment is running with this command:

    $ which python

Install the packages that are contained in the `requirements.txt` file:

    $ pip install -r requirements.txt

If this doesnt work, install the following packages manually:

    $ pip install datasets
    $ pip install matplotlib

Afterwards, run the following script to start the program:

    $ python main.py