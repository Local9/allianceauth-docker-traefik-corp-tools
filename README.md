# Alliance Auth Docker Stack: Docker Pre-Loaded with Corp Tools and other modules

## System Requirments

* Host Operating System - Debian/Ubuntu Server. Any RPM based distro should be fine too with some minor tweaks.
* Domain Name
* Proper DNS Records - A minimum of 2 records. A record pointing to WAN IP and CNAME record (or a wildcard (*)) pointing to the root domain.
* Cloudflare SSL Settings - Full SSL
* Port 80 and 443 Forwarding for Traefik

## Prerequesites
You should have the following available on the system you are using to set this up:
* Docker - https://docs.docker.com/get-docker/
* git
* curl

## Cloudflare Setup

This repo relies on having your DNS behind clouldflare.
Will be using the DNS Challenge method to make Traefik get wildcard certificates from LetsEncrypt.

You will need to use the global API key when prompted when running env prepare script.

![CloudFlareAPI](https://raw.githubusercontent.com/voltatek/allianceauth-docker-traefik-corp-tools/main/docs/images/cloudflare-global-api-keys.png "CloudFlareAPI")

If you want to use one of the other DNS providers instead of Cloudflare, make sure to include the required configuration parameters in the compose file on line 70.

## Modules Preloaded 

* Corp Tools - https://github.com/Solar-Helix-Independent-Transport/allianceauth-corp-tools
* Secure Groups - https://github.com/Solar-Helix-Independent-Transport/allianceauth-secure-groups
* AA Prom Client - https://github.com/Solar-Helix-Independent-Transport/allianceauth-prom-client
![AA Prom Client](https://raw.githubusercontent.com/voltatek/allianceauth-docker-traefik-corp-tools/main/docs/images/esidashboard.png "AA Prom Client")
* AA Loki Logging - https://github.com/Solar-Helix-Independent-Transport/allianceauth-loki-logging
![AA Loki Logging](https://raw.githubusercontent.com/voltatek/allianceauth-docker-traefik-corp-tools/main/docs/images/lokilogs.png "AA Loki Logging")

## Services Preloaded

* Mumble
* Discord

## Discord Service

This stack assumes you have a discord server already set up if not following the following 

1. Navigate to the [Discord Developers site](https://discord.com/developers/applications/me). Press the plus sign to create a new application.
1. Give it a name and description relating to your auth site. Add a redirect to https://auth.example.com/discord/callback/, substituting your domain. Press Create Application.
1. Keep a note of the following details
 - The server ID (known as `GUILD ID`) [following this procedure.](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)
 - From the General Information panel, `DISCORD_APP_ID` is the Client/Application ID
 - From the OAuth2 > General panel, `DISCORD_APP_SECRET` is the Client Secret
 - From the Bot panel, `DISCORD_BOT_TOKEN` is the Token

Above are snippets from guide on readthedocs [Auth Discord Service Guide](https://allianceauth.readthedocs.io/en/v3.3.0/features/services/discord.html#creating-a-server)


## Install Auth Guide

1. run `./scripts/prepare-env.sh` to set up your environment
1. run `docker-compose build` to build the custom images - note on mumble docker `Building wheel for zeroc-ice (setup.py): still running...` will take a while to load
1. run `docker-compose --env-file=.env up -d`
1. run `docker-compose exec allianceauth bash` to open up a terminal inside your auth container
1. run `auth migrate`
1. run `auth collectstatic --noinput`
1. run `auth createsuperuser`
1. run `auth ct_setup`
1. run `auth setup_securegroup_task`


## Adding Discord Bot To Server

Navigate to the services page of your Alliance Auth install as the superuser account. At the top there is a big green button labelled Link Discord Server. Click it, then from the drop down select the server you created, and then Authorize.

This adds a new user to your Discord server with a BOT tag, and a new role with the same name as your Discord application. Don’t touch either of these. If for some reason the bot loses permissions or is removed from the server, click this button again.

To manage roles, this bot role must be at the top of the hierarchy. Edit your Discord server, roles, and click and drag the role with the same name as your application to the top of the list. This role must stay at the top of the list for the bot to work. Finally, the owner of the bot account must enable 2 Factor Authentication (this is required from Discord for kicking and modifying member roles). If you are unsure what 2FA is or how to set it up, refer to this support page. It is also recommended to force 2FA on your server (this forces any admins or moderators to have 2fa enabled to perform similar functions on discord).

Note that the bot will never appear online as it does not participate in chat channels.

## Configure Mumle for SuperUser Access

1. Your Mumble SU password will be generated on first boot and printed to the logs. if you wish to change it or forget it.
   1. open mumble_auth docker shell `docker-compose exec mumble_auth bash`
   2. run command `/usr/bin/mumble-server -fg -ini /data/mumble_server_config.ini -supw YouPassHere`
   3. run command `supervisorctl restart mumbleserver:mumble`
   4. run command `supervisorctl restart mumbleserver:authenticator`  - Important you restart Mumble first then the authenticator
   5. exit the terminal with `exit`

## Adding extra packages
There are a handful of ways to add packages:
* Running `pip install` in the container
* Modifying the container's initial command to install packages
* Building a custom Docker image (recommended, and less scary than it sounds!)

### Using a custom docker image
Using a custom docker image is the preferred approach, as it gives you the stability of packages only changing when you tell them to, along with packages not having to be downloaded every time your container restarts

1. Add each additional package that you want to install to a single line in `conf/requirements.txt`. It is recommended, but not required, that you include a version number as well. This will keep your packages from magically updating. You can lookup packages on https://package.wiki, and copy everything after `pip install` from the top of the page to use the most recent version. It should look something like `allianceauth-signal-pings==0.0.7`. Every entry in this file should be on a separate line
1. In `docker-compose.yml`, comment out the `image` line under `allianceauth` (line 36... ish) and uncomment the `build` section
1. run `docker-compose --env-file=.env up -d`, your custom container will be built, and auth will have your new packages. Make sure to follow the package's instructions on config values that go in `local.py`
1. run `docker-compose exec allianceauth bash` to open up a terminal inside your auth container
1. run `allianceauth update myauth`
1. run `auth migrate`
1. run `auth collectstatic`

_NOTE: It is recommended that you put any secret values (API keys, database credentials, etc) in an environment variable instead of hardcoding them into `local.py`. This gives you the ability to track your config in git without committing passwords. To do this, just add it to your `.env` file, and then reference in `local.py` with `os.environ.get("SECRET_NAME")`_

## Updating Auth

### Base Image
Whether you're using a custom image or not, the version of auth is dictated by $AA_DOCKER_TAG in your `.env` file.
1. To update to a new version of auth, update the version number at the end (or replace the whole value with the tag in the release notes).
1. run `docker-compose pull`
1. run `docker-compose --env-file=.env up -d`
1. run `docker-compose exec allianceauth bash` to open up a terminal inside your auth container
1. run `allianceauth update myauth`
1. run `auth migrate`
1. run `auth collectstatic`

_NOTE: If you specify a version of allianceauth in your `requirements.txt` in a custom image it will override the version from the base image. Not recommended unless you know what you're doing_

### Custom Packages
1. Update the versions in your `requirements.txt` file
1. Run `docker-compose build`
1. Run `docker-compose --env-file=.env up -d`

```
# allianceauth-docker-traefik
