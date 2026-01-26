{
  description = "Python Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      # You can add more systems here if needed (e.g., "aarch64-linux")
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      python_env = pkgs.python3.withPackages (
        ps: with ps; [
          xarray
          rioxarray
          dask
          distributed
          scipy
          pandas
          geopandas
          netcdf4
          zarr
          pyarrow
          matplotlib
          ipykernel
        ]
      );

      system_packages = with pkgs; [
        glibcLocales
        stdenv.cc.cc.lib
      ];
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = [
          python_env
          system_packages
        ];

        shellHook = ''
          export LANG=en_US.UTF-8
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib ]}:$LD_LIBRARY_PATH"
        '';
      };
    };
}
