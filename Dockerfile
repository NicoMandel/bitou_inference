FROM python:3.9 as base

WORKDIR /app

# Creating the environment
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools wheel
RUN pip install numpy mkl-fft opencv-python==4.6.0.66
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV="docker"
ENV FLASK_APP=app.py
EXPOSE 5000

# COPY . . 
# ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/model.py src/csuinf/model.py
# ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/utils.py src/csuinf/utils.py
# ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/src/csupl/geotiff_utils.py src/csuinf/geotiff_utils.py
# ADD https://cloudstor.aarnet.edu.au/plus/s/dojRidMLnrHK8nV/download best.pt
# ADD https://raw.githubusercontent.com/NicoMandel/bitou_segmentation/main/config/colour_code.json config/colour_code.json
# RUN pip install -e .

RUN pip install debugpy
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . . 
RUN pip install -e .
# RUN python setup_model.py

# CMD [ "python", "app.py"]