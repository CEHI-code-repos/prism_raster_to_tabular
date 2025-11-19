import pandas as pd
from pathlib import Path

data_dir = Path("output/nc/ppt/")
files = list(data_dir.rglob("*.parquet"))

dfs = []
for f in files:
    date_str = f.stem.split("_")[-1]
    date = pd.to_datetime(date_str)

    df = pd.read_parquet(f)
    df["date"] = date
    df["year"] = date.year
    df = df[["id", "date", "year", "ppt"]]
    dfs.append(df)

combined = pd.concat(dfs, ignore_index=True)

by_year = {y: g.drop(columns=["year"]) for y, g in combined.groupby("year")}

for year, df in by_year.items():
    out_dir = data_dir / str(year)
    out_dir.mkdir(parents=True, exist_ok=True)

    out_file_parquet = out_dir / f"prism_ppt_nc_800m_{year}.parquet"
    out_file_csv = out_dir / f"prism_ppt_nc_800m_{year}.csv"
    df.to_parquet(out_file_parquet, index=False)

    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df.to_csv(out_file_csv, index=False)
