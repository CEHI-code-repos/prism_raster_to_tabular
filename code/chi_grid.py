from pathlib import Path
import rioxarray
import pandas as pd
import geopandas as gpd

area = "chi"
area_prj = "EPSG:3435"
area_shp_path = "input/ChicagoBoundaries_20260304.geojson"
data_dir = Path("input/")
output_dir = Path(f"output/{area}/")
output_dir.mkdir(exist_ok=True, parents=True)

rast_path = sorted(list(data_dir.rglob("*.tif")))[0]
rast_crs = rioxarray.open_rasterio(rast_path).rio.crs

area_geometry = (
    gpd.read_file(area_shp_path)
    .to_crs(area_prj)
    .assign(geometry=lambda x: x.geometry.buffer(1000))
    .pipe(lambda x: x[["geometry"]])
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

area_id = id_gdf.sjoin(area_geometry, how="inner", predicate="within").drop(
    columns=["geometry", "index_right"]
)
area_id.to_parquet(f"{output_dir}/{area}_prism_id.parquet", index=False)
area_id.to_csv(f"{output_dir}/{area}_prism_id.csv", index=False)
