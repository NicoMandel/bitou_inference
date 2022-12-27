FROM conitnuumio/miniconda3
# Working with Conda inside docker: https://pythonspeed.com/articles/activate-conda-dockerfile/

WORKDIR /app

# Creating the environment
COPY csuinf.txt .
RUN conda env create -f csuinf.txt

# Activating the environment
RUN conda activate csuinf
RUN echo "Making sure flask is installed:"
RUN python -c "import flask"

# If things worked:
COPY scripts/run.py .
ENTRYPOINT [ "python", "run.py" ]