FROM ubuntu:16.04
VOLUME /workdir
VOLUME /clickpecker
VOLUME /clickpecker-pytest
COPY requirements.txt /root/
COPY ./requirements/* /root/requirements/
RUN apt-get update -qq && apt-get install -yqq \
      curl \
      libleptonica-dev \
      libsm6 \
      libtesseract-dev \
      libxext6 \
      python-software-properties \
      software-properties-common \
      tesseract-ocr \
      unzip \
    && add-apt-repository ppa:jonathonf/python-3.6 \
    && apt-get update -qq && apt-get install -yqq \
       python3.6 \
       python3.6-dev \
       python3-pip \
       python3.6-venv
RUN python3.6 -m pip install -q --upgrade pip \
    && python3.6 -m pip install -r /root/requirements.txt -q
RUN curl -o /root/platform-tools.zip https://dl.google.com/android/repository/platform-tools-latest-linux.zip \
    && unzip /root/platform-tools.zip -d /root/ \ 
    && rm /root/platform-tools.zip
ENV PATH /root/platform-tools:$PATH
WORKDIR /workdir
CMD python3.6 -m pip install -e /clickpecker > /dev/null \
    && python3.6 -m pip install -e /clickpecker-pytest > /dev/null \
    && sleep infinity