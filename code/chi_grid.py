from pathlib import Path
import rioxarray
import pandas as pd
import geopandas as gpd
from shapely.geometry import box

area = "chi"
area_prj = "EPSG:3435"
data_dir = Path("input/")
output_dir = Path(f"output/{area}/")
output_dir.mkdir(exist_ok=True, parents=True)

rast_path = sorted(list(data_dir.rglob("*.tif")))[0]
rast_crs = rioxarray.open_rasterio(rast_path).rio.crs

area_geometry = (
    gpd.GeoSeries([box(-88.8, 41.3, -87.1, 42.5)], crs = rast_crs)
    .to_crs(area_prj)
    .buffer(1000)
)

id_gdf = (
    pd.read_parquet(f"{output_dir.parent}/us/us_prism_id.parquet")
    .pipe(
        lambda x: gpd.GeoDataFrame(
            x, geometry=gpd.points_from_xy(x.x, x.y), crs=rast_crs
        )
    )
    .to_crs(area_geometry.crs)
)

area_id = id_gdf.clip(area_geometry).drop(
    columns=["geometry"]
).rename(columns={"id": "grid800mID"})
area_id.to_parquet(f"{output_dir}/{area}_prism_id.parquet", index=False)
area_id.to_csv(f"{output_dir}/{area}_prism_id.csv", index=False)
