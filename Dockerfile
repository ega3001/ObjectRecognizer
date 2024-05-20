FROM python:3.10

WORKDIR /app
ARG GITUSER
ARG GITPASS
ARG FTPUSER
ARG FTPPASS


RUN apt-get update && apt-get install libgl1 -y

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu118                                                                                                                                
RUN pip3 install --force-reinstall pillow==9.5.0
RUN pip3 install git+https://${GITUSER}:${GITPASS}@github.com/ega3001/Det2Recognizer
RUN pip install git+https://${GITUSER}:${GITPASS}@github.com/ega3001/YOLORecognizer
RUN wget -r -nd -P . ftp://${FTPUSER}:${FTPPASS}@172.24.18.81:21/

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt


COPY . .

ENTRYPOINT [ "python3", "/app/main.py" ]