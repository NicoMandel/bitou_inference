import requests


if __name__=="__main__":
    url = "https://cloudstor.aarnet.edu.au/plus/s/dojRidMLnrHK8nV"
    r = requests.get(url=url, allow_redirects=False)
    with open('best.pt', 'wb') as f:
        f.write(r.content)
    