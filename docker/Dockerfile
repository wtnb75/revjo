FROM python:3-alpine
ARG tag=master
RUN pip install -r https://raw.githubusercontent.com/wtnb75/projectname/${tag}/requirements.txt
RUN pip install https://github.com/wtnb75/projectname/archive/${tag}.zip
ENTRYPOINT ["projectname"]
