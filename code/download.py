import os
import shutil
import requests
import pandas as pd
from itertools import product

base_url = "https://services.nacse.org/prism/data/get"
base_path = "input"

dates = pd.date_range(start="2000-01-01", end="2024-12-31").strftime("%Y%m%d")
measures = ["ppt", "tmin", "tmax", "tmean", "tdmean"]

parameters = list(product(dates, measures))

for date_str, measure in parameters:
    url = f"{base_url}/us/800m/{measure}/{date_str}"

    year = date_str[:4]
    dir_path = os.path.join(base_path, measure, year)
    os.makedirs(dir_path, exist_ok=True)
    path = os.path.join(dir_path, f"prism_{measure}_us_800m_{date_str}.zip")

    resp = requests.get(url)
    resp.raise_for_status()

    with open(path, "wb") as f:
        f.write(resp.content)

    shutil.unpack_archive(path, os.path.splitext(path)[0])
    os.remove(path)
