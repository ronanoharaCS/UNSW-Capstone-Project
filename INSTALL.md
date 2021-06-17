THE NEWSROOM INSTALLATION INSTRUCTIONS

NOTE: This project requires software that was not available on UNSW Vlab. This was approved by our tutor Ali Derejeh. 

# WINDOWS 10 (Tested on Windows 10 1903) 

## Requirements

https://www.omgubuntu.co.uk/how-to-install-wsl2-on-windows-10
* Hyper V enabled (If you have WSL2 this will already be enabled) 
* WSL2 Download Kernel 
* Windows 1903 or higher


## Pre-Installation

1. Enable virtualization in BIOS (This will already be enabled if you are using WSL)

2. Install WSL and Linux Kernel
    https://docs.microsoft.com/en-us/windows/wsl/install-win10

    1. Enable WSL
        `dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart`

    2. a. If using Windows 10 (version 2004)

    To enable Virtual Machine Platform on Windows 10 (2004) open PowerShell as Administrator and run:

    `dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart`
    

    b. If using Windows 10 version 1903, 1903
        
    To enable Virtual Machine Platform on Windows 10 (1903, 1909) open PowerShell as Administrator and run:
 
    `Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform -NoRestart`
 
   Open PowerShell as Administrator and run this command to set WSL 2 as the default version of WSL: 
   3. `wsl --set-default-version 2`
    
    Install Linux Kernel update package: 
    https://docs.microsoft.com/en-us/windows/wsl/wsl2-kernel

3. Install Ubuntu 20.04 from Microsoft Store 
 https://www.microsoft.com/en-au/p/ubuntu/9nblggh4msv6?activetab=pivot:overviewtab
 
4. Install Docker 
    All the following Instructions can be found here 
    https://docs.docker.com/engine/install/ubuntu/
    and 
    
    1. Update packages and Install packages
     `sudo apt-get update`
     `sudo apt-get install \ apt-transport-https \ ca-certificates \ curl \ gnupg-agent \ software-properties-common`
    2. add Docker's GPG key
     `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -` 
     
    3. Add the repository
    `sudo add-apt-repository \ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable"`

    4. Install Docker Engine
      `sudo apt-get update`
      `sudo apt-get install docker-ce docker-ce-cli containerd.io`
 
    5. Install Docker Compose
     `sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
     
    3. Apply executable permissions to the binary
        `sudo chmod +x /usr/local/bin/docker-compose`
 
5. Install Postgres
     `sudo apt install postgresql`
     
6. Install npm
    `sudo apt install npm`



## SETUP (IMPORTANT) 
`sudo service postgresql stop`
`sudo service docker start`
`sudo mkdir /sys/fs/cgroup/systemd && sudo mount -t cgroup -o none, name=systemd cgroup /sys/fs/cgroup/systemd`



## Troubleshooting



Ports required:

The website runs on localhost:3000
Graphiql uses localhost:5000
postgres uses localhost:5432


# LINUX (Tested on Ubuntu 20.04) 

1. Install Docker 
    All the following Instructions can be found here.
    Docker Engine: https://docs.docker.com/engine/install/ubuntu/
    Docker Compose: https://docs.docker.com/compose/install/
    
    1. Update packages and Install packages
     `sudo apt-get update`
     `sudo apt-get install \ apt-transport-https \ ca-certificates \ curl \ gnupg-agent \ software-properties-common`
    2. add Docker's GPG key
     `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -` 
     
    3. Add the repository
    `sudo add-apt-repository \ "deb [arch=amd64] https://download.docker.com/linux/ubuntu \ $(lsb_release -cs) \ stable"`

    4. Install Docker Engine
      `sudo apt-get update`
      `sudo apt-get install docker-ce docker-ce-cli containerd.io`
 
    5. Install Docker Compose
     `sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose` 
    
    6. Apply executable permissions to the binary
        `sudo chmod +x /usr/local/bin/docker-compose`

3. Install Postgres
    `sudo apt install postgresql`

5. Install npm
    `sudo apt install npm`

## SETUP (IMPORTANT) 
`sudo service postgresql stop`
`sudo service docker start`

# MAC OSX

# Requirements

## Pre-Installation

1. https://docs.docker.com/docker-for-mac/install/
Do the Docker Desktop install (if there is an option to include docker-compose in the download, say yes)

2. Install postgresql
    https://www.postgresql.org/download/ 

3. Install npm
    https://www.npmjs.com/get-npm
 
https://docs.docker.com/engine/install/ubuntu/

## SETUP (IMPORTANT) 
`service start docker`

## Troubleshooting
* Exit Error 34 Docker port is 5432 postgresql default port...o

### Windows Specific 
* ERROR: Service 'graphql-engine' failed to build : cgroups: cannot find cgroup mount destination: unknown
 


