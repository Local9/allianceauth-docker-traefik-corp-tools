#!/bin/bash
sed -ri 's@&&AA_DB_NAME&&@'${AA_DB_NAME}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&AA_DB_USER&&@'${AA_DB_USER}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&AA_DB_PASSWORD&&@'${AA_DB_PASSWORD}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&AA_MUMBLE_DB_PREFIX&&@'${AA_MUMBLE_DB_PREFIX}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&AA_DB_HOST&&@'${AA_DB_HOST}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&AA_DB_PORT&&@'${AA_DB_PORT}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&MUMBLE_ICE_SECRET&&@'${MUMBLE_ICE_SECRET}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&MUMBLE_HOST_NAME&&@'${MUMBLE_HOST_NAME}'@' /home/allianceauth/mumble-authenticator/authenticator.ini
sed -ri 's@&&MUMBLE_ICE_PORT&&@'${MUMBLE_ICE_PORT}'@' /home/allianceauth/mumble-authenticator/authenticator.ini

# Bootstrap Murmurs config parser, but echo its command instead of launching mumble
bash /entrypoint.sh echo

# Start Mumble and authenticatot
echo "Starting Supervisor Services"
supervisord