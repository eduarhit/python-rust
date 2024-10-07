# syntax=docker/dockerfile:1
FROM rust:latest

ARG CURRENT_USER="jenkins"
ARG CURRENT_ID="1000"

RUN apt-get -y update
RUN apt-get install -y sudo

RUN useradd -rm -d /home/${CURRENT_USER} -s /bin/bash -g root -G sudo -u ${CURRENT_ID} ${CURRENT_USER}

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN chown -R ${CURRENT_USER} /home/${CURRENT_USER}

USER ${CURRENT_USER}

RUN sudo apt-get install -y python3 python3-pip python3.11-venv make build-essential libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev git


ENV VIRTUAL_ENV=/home/${CURRENT_USER}/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY requirements.txt .
RUN pip install -r requirements.txt

ENV HOME /home/${CURRENT_USER}
ENV CARGO_ROOT /usr/local/cargo
ENV PATH $CARGO_ROOT/bin:$PATH

