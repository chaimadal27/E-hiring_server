FROM python:3.8

LABEL MAINTAINER="Infinity Management"

# install dependencies & set working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY ./src ./src

EXPOSE 5000

# Create New user & group
RUN groupadd -r uswgi && useradd -r -g uswgi uswgi
USER uswgi

COPY ./entrypoint.sh ./entrypoint.sh

# Runtime configuration
ENTRYPOINT ["./entrypoint.sh"]
