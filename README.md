## LOAD MODEL STARTUP DATA

run load-<det2|yolo>-files.bash script in scripts folder
e.g bash ./scripts/load-yolo-files.bash -u user1 -p 1234qwerASDF

## SETUP CONFIG

copy-paste .env-template to .env file and fill all needed params

## INSTALL & RUN

run docker compose up -d --build
OR
setup venv
install deps by requirements.txt and ./scripts/install-rec-deps.bash script
export env vars with ./scripts/env-export.sh
run python3 main.py

## USEFULL LINKS

 - https://detectron2.readthedocs.io/en/latest/tutorials/install.html
 - https://pytorch.org/
 - https://docs.ultralytics.com/quickstart/#install-ultralytics