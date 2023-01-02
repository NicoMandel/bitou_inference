# bitou_inference
Inference Repository for the bitou model - deployment


## To run the current status
1. run in the terminal `docker run -p 5000:80 pytorchflask` which maps the port 80 in the container to 5000 on the host
2. cd into the directory with the image files: `cd ~/src/csu/data/birdies_fuji_crops/crops/positive`
3. `conda activate csuinf`
4. `python`
    1. `import requests`
    2. post request: `resp = requests.post("http://localhost:5000/predict", files={"file":open('DSCF7210_3.png', 'rb')})`
    3. jsonify response: `resp.json()`


## Tutorials
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