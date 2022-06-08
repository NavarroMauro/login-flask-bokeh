#Install procedure of Login Flask App with Gunicorn + Nginx

1. First, install all necessary packages that will allow us to build the python virtual environment. We will use the same version used by onRtools application, Python 3.8. For the next steps, it is needed to become a root user.

```bash
sudo -i
```

2. Install all necessary package to create our virtual environment.
```bash
sudo apt install python3-pip python3-venv python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

3. Create the virtual environment and activate it:
```python3
python3 -m venv login-flask-bokeh
source login-flask-bokeh/bin/activate
```

4. Now create a folder to hold the project. We will store it in /var/www/login-flask-bokeh, change permissions accordingly.

```
mkdir /var/wwww/login-flask-bokeh
sudo chown -R $USER:www-data /var/www/login-flask-bokeh
```

5. Download the login-flask-bokeh repo to /var/www/login-flask-bokeh.

```bash
git clone https://transluciddata@bitbucket.org/devRockStar/login-flask-bokeh.git
```

6. Install app requirements (to create a list environment file during app development, use: pip3 freeze > requirements.txt)

```
pip install wheel
pip install -r requirements.txt
```

7. Test the connection 
   ```bash
   gunicorn --bind 0.0.0.0:5000 wsgi:app
   ```

9. Add login-flask-bokeh as a system service, so every time the server is restarted, the application will start automatically.

The login-flask-bokeh file is in /var/www/login-flask-bokeh, so the name of the server must be entered in "ExecStart=...".


Start 3 worker processes (though you should adjust this as necessary)
Create and bind to a Unix socket file, myproject.sock, within your project directory.
Set an umask value of 007 so that the socket file is created to give access to the owner andgroup, while restricting other access
Specify the WSGI entry point file name, along with the Python callable within that file (wsgi:app)


flask.service
```bash
[Unit]
#  specifies metadata and dependencies
Description=Flask Web Application Server using Gunicorn
After=network.target

# tells the init system to only start this after the networking target has been reached

# We will give our regular user account ownership of the process since it owns all of the relevant files

[Service]
# Service specify the user and group under which our process will run.
User=root

# give group ownership to the www-data group so that Nginx can communicate easily with the Gunicorn processes.
Group=www-data

# We'll then map out the working directory and set the PATH environmental variable so that the init system knows where our the executables for the process are located (within our virtual environment).
WorkingDirectory=/var/www/flask-login
Environment="PATH=/root/login-flask-bokeh/bin"

# We'll then specify the commanded to start the service
ExecStart=/bin/bash -c 'source /root/login-flask-bokeh/bin/activate; gunicorn --workers 3 --bind unix:/var/www/login-flask-bokeh/app.sock wsgi:app'
Restart=always

# This will tell systemd what to link this service to if we enable it to start at boot. We want this service to start when the regular multi-user system is up and running:
[Install]
WantedBy=multi-user.target
```

Note: In the last line of [Service] file We tell it to start 3 worker processes. We will also tell it to create and bind to a Unix socket file within our project directory called app.sock. We’ll set an unmask value of 007 so that the socket file is created giving access to the owner and group, while restricting other access. Finally, we need to pass in the WSGI entry point file name and the Python callable within.

8. We can now start the Gunicorn service we created and enable it so that it starts at boot:
```bash
sudo systemctl start app
sudo systemctl enable app
```

5. Setting up ENVIRONMENTAL VARIABLES file
First, we do need to have a .env file in the root folder of your project, if you have a Linux-based system or Mac, inside the folder of your project just make:
```bash
touch env.py
```
