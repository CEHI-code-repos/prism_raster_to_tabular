import shutil
from datetime import datetime
from pathlib import Path
import dask.dataframe as dd

measures = ["ppt", "tdmean", "tmin", "tmean", "tmax"]
for measure in measures:
    data_dir = Path(f"output/us/{measure}/")
    output_dir = Path(f"output/nc/{measure}/")
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(list(data_dir.rglob("*.parquet")))

    nc = dd.read_parquet("output/nc/nc_prism_id.parquet")[["id"]].persist()

    for f in files:
        date = datetime.strptime(f.stem[-8:], "%Y%m%d")
        date_str = date.strftime("%Y%m%d")
        year_str = date.strftime("%Y")

        out_file = output_dir / year_str / f"prism_{measure}_nc_800m_{date_str}"
        out_file_csv = str(out_file) + ".csv"
        out_file.mkdir(exist_ok=True, parents=True)

        ddf = (
            dd.read_parquet(f)
            .merge(nc, on="id", how="inner")
            .repartition(npartitions=1)
        )
        ddf.to_csv(out_file_csv, single_file=True, index=False)
        ddf.to_parquet(out_file, write_index=False)

        # move the parquet out of the folder
        out_file_parquet = out_file / "part.0.parquet"
        shutil.move(str(out_file_parquet), str(out_file) + ".parquet")
        shutil.rmtree(out_file)
