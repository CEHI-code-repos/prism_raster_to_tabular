from pathlib import Path
import rioxarray
import pandas as pd
import geopandas as gpd

data_dir = Path("input/")
output_dir = Path("output/nc/")
output_dir.mkdir(exist_ok=True, parents=True)

rast_path = sorted(list(data_dir.rglob("*.tif")))[0]
rast_crs = rioxarray.open_rasterio(rast_path).rio.crs

nc = (
    gpd.read_file("input/tl_2025_us_state/tl_2025_us_state.shp")
    .query("NAME == 'North Carolina'")
    .to_crs("ESRI:103500")
    .assign(geometry=lambda x: x.geometry.buffer(1000))
    .pipe(lambda x: x[["geometry"]])
)

id_gdf = (
    pd.read_parquet("output/us/us_prism_id.parquet")
    .pipe(
        lambda x: gpd.GeoDataFrame(
            x, geometry=gpd.points_from_xy(x.x, x.y), crs=rast_crs
        )
    )
    .to_crs(nc.crs)
)

nc_id = id_gdf.sjoin(nc, how="inner", predicate="within").drop(
    columns=["geometry", "index_right"]
)
nc_id.to_parquet("output/nc/nc_prism_id.parquet", index=False)
nc_id.to_csv("output/nc/nc_prism_id.csv", index=False)
