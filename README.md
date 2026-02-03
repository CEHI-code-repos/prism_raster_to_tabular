## Converting PRISM rasters to tabular file formats

### Setup

Create an input folder and put inside of it the 2025 US State boundaries like so:  
`input/tl_2025_us_state/tl_2025_us_state.shp`

Then run each script in successsion.

The original COGs will total to about 1.5 TB. National parquets will total to about 3.5 TB.

### Processing

1. Download raster data - `code/download.py`
   a. For each measure download and unzip daily COGs from 2000-2024
      `input/{measure}/{year}/prism_{measure}_us_800m_{YYYYMMDD}/prism_{measure}_us_30s_{YYYYMMDD}.*`
2. Create national grid - `code/national_grid.py`  
   a. Get the lon lat coordinates for each grid point  
   b. Assign ids to each coordinates  
   c. Write to table  `output/us/us_prism_id.*`

3. Create North Carolina grid  `code/nc_grid.py`  
   a. Read in national grid and project to ESRI:103500  
   b. Buffer North Carolina 2025 TIGER Boundaries by 1 km using ESRI:103500  
   c. Do a spatial join to filter the national grid points to North Carolina  
   d. Reproject lon lat back to WGS 1984  
   e. Write to table  `output/nc/nc_prism_id.*`

4. Convert national rasters to tabular data  `code/to_national_tables.py`  
   a. Read in each daily raster and assign each point its id  
   b. Convert rasters to parquets  `output/us/{measure}/{year}/prism_{measure}_us_800m_{YYYYMMDD}.parquet`

5. Subset national tabular data to North Carolina  `code/to_nc_tables.py`  
   a. Read in each daily national parquet  
   b. Read in North Carolina grid  
   c. Conduct an inner join between national daily data and the North Carolina grid to filter data to North Carolina  
   d. Write to table  `output/nc/{measure}/{year}/prism_{measure}_nc_800m_{YYYYMMDD}.*`

6. Combine daily tables into yearly tables  `code/summarize_yearly_nc.py`  
  `output/nc/{measure}/{year}/prism_{measure}_nc_800m_{YYYY}.*`
