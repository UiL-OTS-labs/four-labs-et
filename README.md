# Multi-lab baby eyetracking experiment

# Requirements
You are expected to be able to run a few commands from the command line. You
have a working version of python2/3 on your path or know how to run the
python interpreter another way.

# Install experiment

install source tree:

- git clone https://github.com/UiL-OTS-labs/four-labs-et.git

Change to the cloned directory

- cd four-labs-et

Create virtual python environment (use --site-packages in order to obtain pylink
from the system environment)

virtualenv venv2 --site-packages

Activate the environment. Prior to the the next command your terminal prompt
looks roughly like:
"`duijn119@im-lab-009-02:~/zep/daan-van-renswoude/four-labs-et$`"
and after:
"`(venv2) duijn119@im-lab-009-02:~/zep/daan-van-renswoude/four-labs-et$`"
notice the prepending of "(venv3)"

- source venv2/bin/activate

Install the required packages:
First upgrade pip (from the venv)

- pip install --upgrade pip

install packages

- pip install numpy pillow pygame python-pygaze