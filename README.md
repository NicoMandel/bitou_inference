# bitou_inference
Inference Repository for the bitou model - deployment

# Usage
## Docker
1. Ensure that you have docker installed on your computer
2. Only once - Build the image defined in the [`Dockerfile`](./Dockerfile).
    1. Either through `docker compose build flask-deploy`. This will build the image with the name `bitouflask`
    2. Through running `docker build --target prod -t bitouflask` in the command line
3. Deploy the image with the name `bitouflask` (which should show up as built when running `docker images`)
    1. Either through `docker compose up flask-deploy`
    2. Or through `docker run -p 5000:5000 bitouflask`
4. Open a **private** browser window (otherwise the content of the html will be cached and updates not displayed correctly) and enter `127.0.0.1:5000`
5. Select an image and click "upload" to show inference results

### Notes
* Building the image (steps 1 and 2) are only necessary when definitions have changed. Otherwise start at step 3 to use the local image
* Building the image will take a significant amount of time (~45 minutes) and Hard drive space (~8 GB)

## Conda
The package can also be installed using conda on Ubuntu Linux 22.04. 
1. run `conda env create -f csuinf.txt` to create the environment
2. run `conda activate csuinf` to activate the environment. This has flask and all necessary files installed
3. download / symlink the files `model.py` and `utils.py` from the [bitou segmentation repository](https://github.com/NicoMandel/bitou_segmentation)
    1. Download [`model.py`](https://github.com/NicoMandel/bitou_segmentation/blob/main/src/csupl/model.py) and place it in [`src/csuinf`](./src/csuinf/)
    2. Download [`utils.py`](https://github.com/NicoMandel/bitou_segmentation/blob/main/src/csupl/utils.py) and place it in [`src/csuinf`](./src/csuinf/)
4. Install the local files locally into the conda environment through running `pip install -e .`
5. Download the [`colour_code.json`](https://github.com/NicoMandel/bitou_segmentation/blob/main/config/colour_code.json) and place it in [`config`](./config/)
6. Run [`app.py`](./app.py) by running `python app.py`. Alternatively use the default flask config that is targeted.
7. Access `127.0.0.1:500` in a local **private** browser and upload an image. The uploaded images can be found in the [`images`](./images/) directory and are persistent!

# Explanation

## Debugging Configuration
A debugging configuration is provided that allows running the model inside a docker container and attaching to it through a vscode debugger.
1. build the `dev` configuration of the container.
    1. Through `docker compose build flask-debug`
    2. Through `docker build --target dev -t dev/pytorchflask .`
2. Deploy the container through running `docker compose up flask-debug` - this will ensure correct port forwarding
3. Place a breakpoint in [`app.py`](./app.py) in vscode. 
4. Use the launch configuration `Python: Remote Attach` defined in [launch.json](./.vscode/launch.json#L34) to run `app.py`
5. Open a **private** browser and enter `127.0.0.1:5000` and follow the desired commands
6. vscode should stop at the breakpoint


## Tutorials and helpful resources
1. [x] This basic one from the pytorch development team, [on their website](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html)
1. [x] This one from docker itself how to run a flask application inside docker [on git](https://github.com/docker/awesome-compose/tree/master/flask)
    * [x] With a Tutorial to go alongside in the [docker blog](https://docs.docker.com/compose/gettingstarted/)
2. [ ] This one from an AI Engineer on [Medium](https://medium.com/nlplanet/deploy-a-pytorch-model-with-flask-on-gcp-vertex-ai-8e81f25e605f)
3. [ ] This one from another engineer, which also includse docker [on his website](https://www.paepper.com/blog/posts/pytorch-gpu-inference-with-docker/)
4. [ ] This one from some guy who already wrote a git for this stuff [on GitHub](https://github.com/imadtoubal/Pytorch-Flask-Starter)
5. [ ] This better Github Version of a dockerfile on [GitHub](https://github.com/nikitajz/pytorch-flask-inference)
6. [x] Something about Docker Port mapping and exposing [here](https://www.mend.io/free-developer-tools/blog/docker-expose-port/)
7. [ ] This one about uploading images with flask to a website from some guy on [Youtube](https://www.youtube.com/watch?v=dP-2NVUgh50)
8. [ ] Image Upload and display without saving to storage - on [GitHub](https://github.com/geeksloth/flaskimio)
9. [ ] Image upload and display with saving to storage - a [blog post](https://roytuts.com/upload-and-display-image-using-python-flask/)
10. [x] Debugging flask and python [with vscode](https://code.visualstudio.com/docs/python/tutorial-flask)
11. [x] Displaying an image in flask with python [on Stackoverflow](https://stackoverflow.com/questions/46785507/python-flask-display-image-on-a-html-page)
12. [ ] Debugging docker and flask inside vscode in [this medium post](https://medium.com/@lassebenninga/how-to-debug-flask-running-in-docker-compose-in-vs-code-ef37f0f516ee)

### Notes
[ ] Considering to change ownership or mode when [downloading files into a docker container](https://renehernandez.io/snippets/download-files-from-urls/)