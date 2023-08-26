# Update portainer on Synology NAS
## Description
Update portainer on a Synology NAS to the latest version.
## Process
1. Login to the Synology NAS via ssh; if necessary change the default ssh port.
```
ssh administrator@192.168.1.3
```
2. Change to root user and update the container image:
```
sudo -i
docker container ls
docker stop portainer
docker rm portainer
docker pull portainer/portainer-ce:latest
docker run -d -p 8000:8000 -p 9000:9000 -p 9443:9443 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```
## References
* [Source](https://www.wundertech.net/how-to-update-portainer/)