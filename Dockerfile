FROM nvidia/cuda:11.2.0-cudnn8-devel-ubuntu20.04
#FROM python:3.9 as base

# Set up ubuntu dependencies
RUN apt-get update -y && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata vim wget git build-essential git curl libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

## mmm, both fail, not default python wtih the above base
#RUN which python
#RUN python --version

# use conda to get python3.9 might be a ligter weight way?
# Intall anaconda 3.9
ENV PATH="/app/miniconda3/bin:${PATH}"
ARG PATH="/app/miniconda3/bin:${PATH}"
RUN curl -o miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-py39_22.11.1-1-Linux-x86_64.sh &&\
	mkdir /app/.conda && \
	bash miniconda.sh -b -p /app/miniconda3 &&\
	rm -rf miniconda.sh

RUN conda --version
RUN python --version

# Creating the environment
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install numpy mkl-fft opencv-python==4.6.0.66
RUN pip install -r requirements.txt

## have local changes so I think this clashes with pull ##
#FROM base as prod
COPY . . 
RUN ls
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/model.py src/csuinf/model.py
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/utils.py src/csuinf/utils.py
ADD https://cloudstor.aarnet.edu.au/plus/s/dojRidMLnrHK8nV/download best.pt
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/config/colour_code.json config/colour_code.json
RUN pip install -e .
RUN python setup_model.py
ENTRYPOINT [ "python", "app.py"]

#FROM prod as dev
#RUN pip install -e .
#RUN pip install debugpy
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
