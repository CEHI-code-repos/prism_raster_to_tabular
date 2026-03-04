from pathlib import Path
import rioxarray
import pandas as pd
import geopandas as gpd

data_dir = Path("input/")
output_dir = Path("output/chi/")
output_dir.mkdir(exist_ok=True, parents=True)

rast_path = sorted(list(data_dir.rglob("*.tif")))[0]
rast_crs = rioxarray.open_rasterio(rast_path).rio.crs

chi = (
    gpd.read_file("input/ChicagoBoundaries_20260304.geojson")
    .to_crs("EPSG:3435")
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
    .to_crs(chi.crs)
)

chi_id = id_gdf.sjoin(chi, how="inner", predicate="within").drop(
    columns=["geometry", "index_right"]
)
chi_id.to_parquet(f"{output_dir}/chi_prism_id.parquet", index=False)
chi_id.to_csv(f"{output_dir}/chi_prism_id.csv", index=False)
