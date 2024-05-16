FROM python:3.12.3-bullseye

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt .

# Install needed libraries
RUN apt-get update && apt-get install -y \
    gcc \
    netcat \
    pkg-config \
    python3-dev \
    && apt-get clean

RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .

# RUN chmod a+x /code/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
# ENTRYPOINT ["/code/entrypoint.sh"]