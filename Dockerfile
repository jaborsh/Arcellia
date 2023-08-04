# Dockerfile

FROM evennia/evennia:latest

# Set work directory
WORKDIR /usr/src/game

COPY requirements.txt /usr/src/game/arcellia/
# RUN pip install -r requirements.txt

ENTRYPOINT evennia start -l