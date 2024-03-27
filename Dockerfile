FROM python:3

ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV TZ=Asia/Bangkok

RUN django-admin startproject AN_OPEN_NETRA_BE

COPY . /AN_OPEN_NETRA_BE

WORKDIR /AN_OPEN_NETRA_BE

ENV KUBECONFIG=/AN_OPEN_NETRA_BE/kube-config

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
