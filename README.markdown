
# SQUIRL

Student Quest to Unite In Real Life

More documentation is available in 
[this repoisitory's wiki](https://github.com/squirl/squirl/wiki).

## Setting Up (for Developers)

This is a website built in Python, using the Django web framework.
There are a few steps needed to get a brand new machine up and running.

### 1. Install Git and Clone the Source Code

To access the source code for this website, you'll also need to 
[download Git](http://git-scm.com/downloads) and install it. Then, in a command
prompt (either Git Bash on Windows or the standard terminal on OS X / Linux),
run the following commands:

    $ cd <project directory>
    $ git clone git@github.com:squirlapp/squirl.git

This creates a new subdirectory `squirl` below the given directory (`<project
directory>`), containing the current website sources. 

### 2. Install Python

As previously mentioned, this website is written in Python using the Django
framework. To get started developing, you'll need to
[download and install Python 2.7](https://www.python.org/download).

Among other things, this installs a program called '`python`', which is
responsible for running code written in Python, the programming language. Once
you've installed Python, open another terminal, like you did when you cloned
this repository. Then try running

    $ python --version

The output should be something along the lines of '`Python 2.7.8`'. If you get 
an error about not being able to find python, you may need to add python to
your terminal's program search path. If you're developing on Windows, you can 
follow steps 3.3.1 and 3.3.2 on 
[this page](https://docs.python.org/2/using/windows.html#configuring-python).

### 3. Install `pip`

Pip is a package manager responsible for downloading and installing open-source
Python modules that squirl relies on. If you've set up Python on your machine,
installing pip should be relatively straightforward:

* If you're on Windows, run the following in a command prompt:

        $ easy_install pip

* If you're on OS X / Linux, run this command instead:

        $ sudo easy_install pip

If this step completes successfully, you should be able to run the following
in a terminal without errors:

    $ pip --version

### 4. (Optional) Create a Virtual Environment for Developing

In the step after this one, we'll set up the tools needed to run Squirl locally
on your development machine. There are two ways to set up these tools:

* Global: all Python projects on your machine will see the installed modules
* Local: only Squirl will see the installed modules

We recommend the local route, since doing so can prevent headaches involved
when two projects use different, incompatible versions of the same module. To
install dependencies locally, we recommend using 
[virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html).

Installing virtualenv is pretty straightforward using pip. Just run:

    $ pip install virtualenv

This sets up a new `virtualenv` command you can run from the terminal. To make
sure everything's working, try running

    $ virtualenv --version

With virtualenv installed, `cd` to the `squirl` directory we created in step 1:

    $ cd <project directory>/squirl

Then create your virtual Python environment:

    $ virtualenv venv

(Technically, you can use any valid folder name instead of 'venv'; however, the
Squirl source code has already been set up to assume the name of the virtualenv
folder is 'venv', so we recommend you use 'venv').

Finally, you'll need to activate the Squirl virtual environment. You'll need to
do this every time you open a terminal to develop Squirl.

If you're on Windows, run

    $ venv\scripts\activate

If you're on OS X or Linux, run

    $ venv/bin/activate

### 5. Install Requirements

Finally, you should be ready to download the open source Python packages that
Squirl relies on. First, `cd` to the `squirl` directory we created in step 1:

    $ cd <project directory>/squirl

Then, use `pip` to install the required dependencies (which are listed in a
file called `requirements.txt` in the project directory):

    $ pip install -r requirements.txt

This should automatically install all packages required by Squirl. With the
requirements installed, you're now ready to run the actual webiste.

### 6. Start the Development Server

At this point, you should have all developer tools installed and all source
code available. The final setup step is to run the website on your local
machine. To start the web server, first `cd` to the `squirl` directory we
created in step 1:

    $ cd <project directory>/squirl

Finally, use the `runserver` command to start the development server:

    $ python manage.py runserver 8000

If this command is successful, you are now running Squirl locally on your
developer machine! Just open `http://localhost:8000` in a web browser to use
and test your local development copy of Squirl. 

