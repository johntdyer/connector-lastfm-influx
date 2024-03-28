FROM python:3.6

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# Bundle app source
COPY main.py /app

# EXPOSE 8080
CMD [ "python", "main.py" ]