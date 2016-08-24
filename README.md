# GarageWarden
A web app written in python made to monitor and control a garage door while running on a raspberry pi

# Setup
install python (>=3.4) (sudo apt-get install python3)
install pip for python3 (sudo apt-get install python3-pip)
run setup.py (sudo python3 setup.py)
    sudo is needed because this script ensures the appropriate version of django is installed
    first installs django, runs migrations, and then creates the default super user
    Fill in the prompts when asked to set your username and password

I recommend using gunicorn to serve the backend, but expose it via a reverse proxy.
I prefer using caddy as my reverse proxy.

first install gunicorn (python3 -m pip install gunicorn)
then download the latest caddy server for arm processors and install to your favorite location (such as /opt/caddy)

once you have both installed, you will need to modify the Caddyfile located in the ui folder
In the Caddyfile, change localhost:2015 to the real domain name that you would like to access your garage controller from.
Make sure that you forward port 80 and 443 from your router to your raspberry pi so that you will be able to access it.
Also ensure your dns records are added correctly to your registrar or personal dns servers for your domain.
Once all that's set up, when you start up caddy, it will automatically create valid ssl certs for you.

Now that it's all configured, you need to start gunicorn, then start caddy.
cd into the GarageWarden folder (the folder the setup.py script is in)
then run:
    nohup python3 -m gunicorn GarageWarden.wsgi >> $HOME/gunicorn.log 2>&1 &

this will start gunicorn in the background and write all output to the file $HOME/gunicorn.log

then cd to the ui folder (where your Caddyfile is)
and run:
    nohup caddy >> $HOME/caddy.log 2>&1 &

this will start up caddy.

At this point, you should be able to access your garage controller from your domain that you specified in the Caddyfile,
assuming your dns is resolving correctly already and the port forwarding is set up correctly.