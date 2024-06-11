FROM python:3.9

RUN pip install numpy matplotlib scipy fastapi uvicorn
COPY . /app
WORKDIR /app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
