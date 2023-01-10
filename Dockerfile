# FROM conitnuumio/miniconda3
# FROM pytorchlightning/pytorch_lightning:base-conda-py3.9-torch1.12
FROM python:3.9 as base
# FROM python:3.10
# Working with Conda inside docker: https://pythonspeed.com/articles/activate-conda-dockerfile/

WORKDIR /app

# RUN apt-get update && apt-get install -y git
# Creating the environment
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install numpy mkl-fft opencv-python==4.6.0.66
# mkl-fft opencv-python==4.6.0
RUN pip install -r requirements.txt

FROM base as prod
# local installs
# COPY 'setup.py' .
COPY . . 
# RUN ls src/csuinf && ls 
# RUN git clone https://github.com/NicoMandel/bitou_segmentation.git
# RUN mv bitou_segmentation/src/csupl/model.py src/csuinf/model.py && mv bitou_segmentation/src/csupl/utils.py src/csuinf/utils.py
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/model.py src/csuinf/model.py
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/utils.py src/csuinf/utils.py
ADD https://cloudstor.aarnet.edu.au/plus/s/dojRidMLnrHK8nV/download best.pt
# RUN chmod 755 src/csuinf/model.py src/csuinf/utils.py
# best.pt
# COPY . . 
# COPY src src/
RUN pip install -e .
# RUN python setup.py bdist_wheel
# RUN pip install dist/csuinf-0.1.0-py3-none-any.whl
RUN python testimports.py
# RUN pip install flask
ENTRYPOINT [ "python", "app.py"]

FROM base as dev
RUN pip install -e .
RUN pip install debugpy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# COPY testimports.py .
# CMD [ "python", "testimports.py" ]

# Activating the environment
# RUN conda activate csuinf
# RUN echo "Making sure flask is installed:"
# RUN python -c "import flask"

# If things worked:
# COPY . .

# only makes it accessible internally - does not publish it, see [here](https://www.mend.io/free-developer-tools/blog/docker-expose-port/)
# EXPOSE 5000

# ENTRYPOINT [ "python", "upload_img.py" ]