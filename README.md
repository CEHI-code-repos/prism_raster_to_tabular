## Converting PRISM rasters to tabular file formats

### Input data

All input data is stored in the following path structure:

`input/{measure}/{year}/prism_{measure}_us_800m_{YYYYMMDD}/prism_{measure}_us_30s_{YYYYMMDD}.*`

### Processing


1. Create national grid - `code/national_grid.py`  
   a. Get the lon lat coordinates for each grid point  
   b. Assign ids to each coordinates  
   c. Write to table  `output/us/us_prism_id.*`

2. Create North Carolina grid  `code/nc_grid.py`  
   a. Read in national grid and project to ESRI:103500  
   b. Buffer North Carolina 2025 TIGER Boundaries by 1 km using ESRI:103500  
   c. Do a spatial join to filter the national grid points to North Carolina  
   d. Reproject lon lat back to WGS 1984  
   e. Write to table  `output/nc/nc_prism_id.*`

3. Convert national rasters to tabular data  `code/to_national_tables.py`  
   a. Read in each daily raster and assign each point its id  
   b. Convert rasters to parquets  `output/us/{measure}/{year}/prism_{measure}_us_800m_{YYYYMMDD}.parquet`

4. Subset national tabular data to North Carolina  `code/to_nc_tables.py`  
   a. Read in each daily national parquet  
   b. Read in North Carolina grid  
   c. Conduct an inner join between national daily data and the North Carolina grid to filter data to North Carolina  
   d. Write to table  `output/nc/{measure}/{year}/prism_{measure}_nc_800m_{YYYYMMDD}.*`

5. Combine daily tables into yearly tables  `code/summarize_yearly_nc.py`  
  `output/nc/{measure}/{year}/prism_{measure}_nc_800m_{YYYY}.*`
