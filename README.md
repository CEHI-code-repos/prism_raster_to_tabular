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

3. Create area grid  `code/{area}_grid.py`  
   a. Read in national grid and project to a local projection  
   b. Buffer area of interest using a local projection, respectively
   c. Do a spatial join to filter the national grid points to North Carolina or Chicago  
   d. Reproject lon lat back to WGS 1984  
   e. Write to table  `output/{area}/{area}_prism_id.*`

4. Convert national rasters to tabular data  `code/to_national_tables.py`  
   a. Read in each daily raster and assign each point its id  
   b. Convert rasters to parquets  `output/us/{measure}/{year}/prism_{measure}_us_800m_{YYYYMMDD}.parquet`

5. Subset national tabular data to North Carolina  `code/to_{area}_tables.py`  
   a. Read in each daily national parquet  
   b. Read in the area of interest's grid  
   c. Conduct an inner join between national daily data and the area of interest's grid to filter data to the area of interest  
   d. Write to table  `output/{area}/{measure}/{year}/prism_{measure}_{area}_800m_{YYYYMMDD}.*`

6. Combine daily tables into yearly tables  `code/summarize_yearly_{area}.py`  
  `output/{area}/{measure}/{year}/prism_{measure}_{area}_800m_{YYYY}.*`
