from pathlib import Path
import rioxarray

data_dir = Path("input/")
output_dir = Path("output/us/")
output_dir.mkdir(exist_ok=True, parents=True)

rast_path = sorted(data_dir.rglob("*.tif"))[0]
rast = rioxarray.open_rasterio(rast_path).squeeze(drop=True)
    
df = (
    rast
    .where(rast != rast.rio.nodata)
    .rename("ppt")
    .to_dataframe()
    .sort_index(level=['x', 'y'], ascending=[True, False])
    .reset_index()
    .assign(
        x_seq = lambda x: x.groupby('y').cumcount() + 1,
        y_seq = lambda x: x.groupby('x').cumcount() + 1,
        id = lambda x: x['y_seq'] * 10000 + x['x_seq'] 
    )
    .dropna(subset="ppt")
    .drop(columns=["ppt", "spatial_ref"])
    .reindex(columns = ["id", "x_seq", "y_seq", "x", "y"])
)

df.to_parquet("output/us/us_prism_id.parquet", index=False)
df.to_csv("output/us/us_prism_id.csv", index=False)
