import urllib.request, json
from pathlib import Path

# Rovers available: Curiosity, Spirit, Opportunity
rover = "spirit"

# Filters available:
# sol (integer)
# earth_date (YYYY-M-D)
# camera (FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES)
# Separate multiple filters with &

filters = "earth_date=2004-1-5"



apiurl = f"http://mars-photos.herokuapp.com/api/v1/rovers/{rover}/photos?{filters}&page="
page = 1
while True:
    with urllib.request.urlopen(f"{apiurl}{page}") as url:
        data = json.loads(url.read().decode())

    if len(data["photos"]) > 0:
        for photo in data["photos"]:
            photoid = photo["id"]
            earth_date = photo["earth_date"]
            sol = photo["sol"]
            rover = photo["rover"]["name"]
            camera = photo["camera"]["name"]
            photourl = photo["img_src"]
            ext = Path(photourl).suffixes[0]
            filename = f"{rover}/{photoid}_{earth_date}_{sol}_{rover}_{camera}{ext}"
            print(f"Saving {filename}")
            Path(rover).mkdir(exist_ok=True)
            urllib.request.urlretrieve(photourl, filename)

        page += 1
    else:
        break


