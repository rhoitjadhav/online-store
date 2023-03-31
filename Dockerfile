FROM python:3.8.10

# Exposing port
EXPOSE 8000

# Environment Variables
ENV SQLALCHEMY_DATABASE_URL "sqlite:///./store.db"

# Copying source code
COPY ./requirements.txt /online-store/
COPY ./src/ /online-store/src

# Installing dependencies
RUN pip install -r /online-store/requirements.txt

# Setting working directory
WORKDIR /online-store/src

# Running application
CMD ["python", "main.py"]