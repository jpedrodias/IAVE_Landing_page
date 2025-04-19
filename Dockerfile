FROM python:3.12-bookworm

WORKDIR /app
COPY ./flaskapp/ /app/

# security
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nano dos2unix cron && \
    apt autoclean -y && \
    apt autoremove -y

RUN dos2unix -i -o ./*.sh && \
    chmod +x ./*.sh

RUN python -m pip install pip --upgrade
RUN python -m pip install -r requirements.txt --no-cache-dir

USER appuser

#CMD [ "python", "app.py" ]