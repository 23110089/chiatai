from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from requests import get
from time import sleep
from datetime import datetime, timedelta, timezone

keys = [
    'rnd_a9p5RJRPbp9Y2p7OY2Mhbb99WZM6',
    'rnd_Ly3yBa8rDtEvHIV6lI0eMu912dkP'
]

app = FastAPI()
@app.get('/')
def home(): return

def g(url, head):
    while True:
        try:
            return get(url, headers=head).json()
        except Exception as e:
            print(f"Error fetching data from {url}: {e}")
            sleep(0.1)

def detail(head):
    dl = g('https://api.render.com/v1/services?includePreviews=true', head)[0]['service']
    id = dl['id']; repo = dl['repo']
    dl = dl['serviceDetails']
    region = dl['region']; link = dl['url']
    return id, repo, region, link

def bandwidth(head):
    account = detail(head)

    now = datetime.now(timezone(timedelta(hours=7)))
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start = start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    end = now.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")

    url = f"https://api.render.com/v1/metrics/bandwidth?startTime={start}&endTime={end}&resource={account[0]}"
    dl = g(url, head)[0]['values']
    mb = 0
    for i in dl: mb += i['value']
    return mb, account[3]

@app.get("/getlink")
def get_link():
    head = {
        "accept": "application/json",
        "authorization": "Bearer rnd_a9p5RJRPbp9Y2p7OY2Mhbb99WZM6"
    }
    mb, file_url = bandwidth(head)
    return RedirectResponse(url=file_url+'/download')
