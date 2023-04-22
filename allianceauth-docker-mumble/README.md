# allianceauth-docker-mumble
Containerized Mumble Service for Alliance Auth

## Assumptions
Everything below assumes you want to run this on the same server as your current docker installed auth and have the `.env` file setup from that install.

if you wish to run mumble detached from auth, you will need to setup something to allow the ice/sql connection, ie a SSH tunnel, and update the env variables to match, this is outside of the scope of this guide.

## Setup
1. Add this to the specified sections of your `docker-compose.yml`
```yml
services:
 ... snip ...
  mumble_auth:
    container_name: ${MUMBLE_HOST_NAME}
    hostname: ${MUMBLE_HOST_NAME}
    image: mumble_auth:latest ##TODO fix this to work this is a local built image
    env_file:
      - ./.env
    restart: unless-stopped
    ports:
        - 64738:64738
        - 64738:64738/udp
    volumes:
      - mumble-data:/data

volumes:
 ... snip ...
    mumble-data:
```
2. Add the following secrets to your .env and update the secrets as required
```bash
#Mumble Settings 
MUMBLE_HOST_NAME=mumble_auth
MUMBLE_ICE_PORT=6502
MUMBLE_ICE_SECRET="IAmAStupidPasswordChangeMe"
MUMBLE_CONFIG_SERVER_PASSWORD="IAmAStupidPasswordChangeMe"
MUMBLE_CONFIG_WELCOMETEXT="Welcome to Mumble. Fleet up. Die. Repeat"

#Murmur Image Configuration Do Not edit unless you are familiar with what they do.
MUMBLE_CONFIG_ICE="tcp -p ${MUMBLE_ICE_PORT}"
MUMBLE_CONFIG_UNAME=mumble
MUMBLE_CONFIG_ICESECRETREAD=${MUMBLE_ICE_SECRET}
MUMBLE_CONFIG_ICESECRETWRITE=${MUMBLE_ICE_SECRET}
```
3. restart your services

4. Your Mumble SU password will be generated on first boot and printed to the logs. if you wish to change it or forget it.
   1. open mumble_auth docker shell `docker-compose exec mumble_auth bash`
   2. run command `/usr/bin/mumble-server -fg -ini /data/mumble_server_config.ini --supw YouPassHere`
   3. exit the terminal `exit`
