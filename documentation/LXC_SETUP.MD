## Step 1

Create a user for running the application.

```
sudo adduser ####
sudo usermod -aG sudo ####
```

## Step 2

Update ssh config

```
sudo nano /etc/ssh/sshd_config
```

Uncomment the line Password Authentification 
```
# To disable tunneled clear text passwords, change to no here!
PasswordAuthentication yes
#PermitEmptyPasswords no
```

To aplly the changes restart sshd

```
sudo systemctl restart sshd
```

## Step 3

Setup program, if not already done logout with root user and login with application user created in Step one

Clone the application from git

```
git clone -b #BRANCHNAME# #HTTPS ADRESS TO GIT REPO# #FOLDERNAME' 
```

Create enviroment

```
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

## Step 4

Create a service file to run the website as service

```
sudo nano /etc/systemd/MYAPP.service

```

### Content MYAPP.service

```

[Unit]
Description=Gunicorn instance to server my Flask app
#Defines that the service should start after the network is up and running
After=network.target

[Service]
#Add the username and group from step one 
User= USERNAME
Group= USERGROUP
#Add the FOLDERNAME from step three
WorkingDirectory=/home/USERNAMEN/FOLDERNAME/
Environment="PATH=/home/USERNAME/FOLDERNAME/env/bin"
ExecStart=/home/USERNAME/FOLDERNAME/env/bin/gunicorn -w 2 -b 0.0.0.0:8000 app:app
Restart=on-failure           
RestartSec=5                 


[Install]
WantedBy=multi-user.target

```

## Step 5

Start the service

```
sudo systemctl deamon-reload
sudo systemctl enable MYAPP
sudo systemctl start MYAPP
```

Check the status of the service

```
systemctl status myapp
```