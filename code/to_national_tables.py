import shutil
from datetime import datetime
from pathlib import Path
import rioxarray
import numpy as np

measure = "tdmean"
data_dir = Path(f"/media/user/Expansion/PRISM/unzipped/{measure}/")
output_dir = Path(f"/media/user/Expansion/PRISM/output/us/{measure}/")
output_dir.mkdir(exist_ok=True, parents=True)

files = sorted(list(data_dir.rglob("*.tif")))
chunk_size = {"x": 1024, "y": 1024}

for file_path in files:
    date = datetime.strptime(file_path.stem[-8:], "%Y%m%d")
    date_str = date.strftime("%Y%m%d")
    year_str = date.strftime("%Y")

    out_file = output_dir / year_str / f"prism_{measure}_us_800m_{date_str}"
    out_file.mkdir(exist_ok=True, parents=True)

    rast = rioxarray.open_rasterio(str(file_path), chunks=chunk_size).squeeze(drop=True)
    rast = rast.where(rast != rast.rio.nodata).assign_coords(
        x=("x", np.arange(1, rast.sizes["x"] + 1)),
        y=("y", np.arange(1, rast.sizes["y"] + 1)),
    )

    ddf = rast.rename(measure).to_dask_dataframe()
    ddf = (
        ddf.dropna(subset=measure)
        .assign(id=ddf["y"] * 10000 + ddf["x"])[["id", measure]]
        .repartition(npartitions=1)
    )

    ddf.to_parquet(out_file, write_index=False)

    # move the parquet out of the folder
    out_file_parquet = out_file / "part.0.parquet"
    shutil.move(str(out_file_parquet), str(out_file) + ".parquet")
    shutil.rmtree(out_file)
