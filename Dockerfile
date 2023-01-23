FROM python:3.9 as base

WORKDIR /app

# Creating the environment
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install numpy mkl-fft opencv-python==4.6.0.66
RUN pip install -r requirements.txt

FROM base as prod
COPY . . 
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/model.py src/csuinf/model.py
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/utils.py src/csuinf/utils.py
ADD https://cloudstor.aarnet.edu.au/plus/s/dojRidMLnrHK8nV/download best.pt
ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/config/colour_code.json config/colour_code.json
RUN pip install -e .
RUN python setup_model.py
ENTRYPOINT [ "python", "app.py"]

FROM prod as dev
# RUN pip install -e .
RUN pip install debugpy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1