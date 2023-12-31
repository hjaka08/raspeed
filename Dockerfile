FROM python:3.8
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]