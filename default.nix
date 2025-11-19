{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages(p: with p; [
      xarray
      rioxarray
      dask
      distributed
      scipy
      geopandas
      netcdf4
      zarr
      pyarrow
      matplotlib
    ]))
  ];
}