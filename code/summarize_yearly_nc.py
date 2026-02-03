import pandas as pd
from pathlib import Path

measures = ["ppt", "tdmean", "tmin", "tmean", "tmax"]
for measure in measures:
    data_dir = Path(f"output/nc/{measure}/")
    files = list(data_dir.rglob("*.parquet"))

    file_dict = {}
    for f in files:
        year = f.stem.split("_")[-1][:4]
        file_dict.setdefault(year, []).append(f)

    for year, yearly_files in file_dict.items():
        dfs = []
        for f in yearly_files:
            date_str = f.stem.split("_")[-1]
            date = pd.to_datetime(date_str)

            df = pd.read_parquet(f)
            df["date"] = date
            df = df[["id", "date", measure]]
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        out_dir = data_dir / str(year)
        out_dir.mkdir(parents=True, exist_ok=True)

        out_file_parquet = out_dir / f"prism_{measure}_nc_800m_{year}.parquet"
        out_file_csv = out_dir / f"prism_{measure}_nc_800m_{year}.csv"
        df.to_parquet(out_file_parquet, index=False)

        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        df.to_csv(out_file_csv, index=False)
