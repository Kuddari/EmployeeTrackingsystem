# Use the official Python image from Docker Hub
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the project files to the working directory

RUN apt-get update && apt-get -y upgrade

COPY requirement.txt /code

RUN pip install -r requirement.txt

RUN pip install django

COPY . .

CMD ["python","manage.py","runserver"]
