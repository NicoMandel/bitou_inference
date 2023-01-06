# FROM conitnuumio/miniconda3
# FROM pytorchlightning/pytorch_lightning:base-conda-py3.9-torch1.12
FROM python:3.9 as base
# FROM python:3.10
# Working with Conda inside docker: https://pythonspeed.com/articles/activate-conda-dockerfile/

WORKDIR /app

# RUN apt-get update && apt-get install -y apt-utils
# Creating the environment
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install numpy mkl-fft opencv-python==4.6.0.66
# mkl-fft opencv-python==4.6.0
RUN pip install -r requirements.txt

# local installs
COPY 'setup.py' .
COPY src src/
RUN pip install -e .
# RUN pip install flask

FROM base as dev
RUN pip install debugpy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Activating the environment
# RUN conda activate csuinf
# RUN echo "Making sure flask is installed:"
# RUN python -c "import flask"

# If things worked:
# COPY . .

# only makes it accessible internally - does not publish it, see [here](https://www.mend.io/free-developer-tools/blog/docker-expose-port/)
# EXPOSE 5000

# ENTRYPOINT [ "python", "upload_img.py" ]