FROM mumblevoip/mumble-server:latest
#FROM python:3.10-slim
ENV VIRTUAL_ENV=/home/allianceauth/venv
ENV AUTH_HOME=/home/allianceauth
ENV AUTH_USER=allianceauth
ENV AUTH_GROUP=allianceauth
ENV AUTH_USERGROUP=${AUTH_USER}:${AUTH_GROUP}

USER root

# Setup user and directory permissions
SHELL ["/bin/bash", "-c"]
RUN groupadd -g 61000 ${AUTH_GROUP}
RUN useradd -g 61000 -l -M -s /bin/false -u 61000 ${AUTH_USER}
RUN mkdir -p ${VIRTUAL_ENV} \
    && chown ${AUTH_USERGROUP} ${VIRTUAL_ENV} \
    && mkdir -p ${AUTH_HOME} \
    && chown ${AUTH_USERGROUP} ${AUTH_HOME}

# Install build dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    python3 python3-pip python3-dev python3-venv gcc git htop build-essential libssl-dev libbz2-dev libmariadb-dev python-dev supervisor

# Switch to non-root user
USER ${AUTH_USER}
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
WORKDIR ${AUTH_HOME}

# OPTIONAL TEMPLINKS? Use and emv variable
RUN git clone https://gitlab.com/aaronkable/mumble-authenticator.git 

WORKDIR ${AUTH_HOME}/mumble-authenticator

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install wheel gunicorn mysqlclient
RUN echo "Ice install will take quite some time (5+ Min) please be patient..."
RUN pip install -r requirements.txt

# Initialize authenticator
ADD ./docker-entrypoint.sh /home/allianceauth/docker-entrypoint.sh
ADD ./authenticator.ini /home/allianceauth/mumble-authenticator/authenticator.ini
ADD ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

USER root

ENTRYPOINT /home/allianceauth/docker-entrypoint.sh
