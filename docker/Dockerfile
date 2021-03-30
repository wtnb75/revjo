FROM python:3-alpine
ARG tag=main
RUN pip install -r https://raw.githubusercontent.com/wtnb75/revjo/${tag}/requirements.txt
RUN pip install https://github.com/wtnb75/revjo/archive/${tag}.zip
ENTRYPOINT ["revjo", "convert"]
