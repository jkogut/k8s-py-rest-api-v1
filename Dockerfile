FROM python:alpine3.7
COPY /app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5002
CMD python ./rest_server.py
