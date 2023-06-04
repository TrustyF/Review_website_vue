FROM python:3.10.8

WORKDIR /src
COPY . /src

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python"]
CMD ["main.py"]