# -*- coding: utf-8 -*-
"""This script uses the Google Earth Engine Python API
 to visualise flood Hazard zones using the flood hazard
 dataset from the Joint Research Centre (JRC) of the European Commission,
 associated with the Copernicus Emergency Management Service (CEMS)
  and GloFAS (Global Flood Awareness System).

Flood hazard extent and intensity rasters over 10, 20, 50 and 100
year return periods are displayed over the selected basemap.

Originally written and run on Google Colab.

"""


import ee
import geemap
import matplotlib.pyplot as plt
from google.colab import userdata
import time

################# INPUT PARAMS ###################
# 2021 Kosi Flood event location
latitude = 29.4580
longitude = 79.1493

basemap = "SATELLITE"
buffer_distance_m = 5000
location_name = "Kosi"

################# START PROCEDURE ###################
### Authenticate and initialize the Google Earth Engine client
ee.Authenticate()
ee.Initialize(
    project = userdata.get("EE_PROJECT_ID"),
    opt_url = "https://earthengine-highvolume.googleapis.com"
)

## Initialize an interactive geospatial map for EE layers
map = geemap.Map(basemap=basemap)
map

# Create ROI by adding a buffer and a bounding box
roi = ee.Geometry.Point([longitude, latitude]).buffer(buffer_distance_m).bounds()

## Create an EE Feature Collection and add style properties
roi_fc = ee.FeatureCollection(ee.Feature(roi))
roi_fc_styled = roi_fc.style(color="red", width=2, fillColor="00000000")

## Visualise the styled ROI on the interactive map
map.addLayer(roi_fc_styled, {}, f"{location_name} Point")
map.centerObject(roi, 12)
map

# Load the jrc dataset
jrc = (ee.ImageCollection("JRC/CEMS_GLOFAS/FloodHazard/v1")
        .filterBounds(roi)
)
jrc

print(sorted(jrc.aggregate_array("return_period").getInfo()))

### 10-year return period flood hazard data
flood_10 = (
    jrc.filterBounds(roi)
       .filter(ee.Filter.eq("return_period", 10))
       .mosaic()

)

print("Flooed 10 info", flood_10.getInfo())


print("Projection of JRC", jrc.first().projection().crs())

map.addLayer(flood_10.clip(roi),user:yourusername
             {"palette":["skyblue", "blue", "darkblue"]},
             "flood_10")
map

### 20 year return period flood hazard data
flood_20 = (
    jrc.filter(ee.Filter.eq("return_period", 20))
       .mosaic()
)


map.addLayer(
    flood_20.clip(roi),
    {"palette": ["skyblue", "blue", "darkblue"]},
    "flood_20"

)
map

### 50 year return period flood hazard data
flood_50 = (
    jrc.filter(ee.Filter.eq("return_period", 50))
       .mosaic()
)


map.addLayer(
    flood_50.clip(roi),
    {"palette": ["skyblue", "blue", "darkblue"]},
    "flood_50"

)
map

### 100-year return period flood hazard data

flood_100 = (
    jrc.filter(ee.Filter.eq("return_period", 100))
       .mosaic()
)


map.addLayer(
    flood_100.clip(roi),
    {"palette": ["skyblue", "blue", "darkblue"]},
    "flood 100"
)

map


## Export the 10 m flood hazard raster
task = ee.batch.Export.image.toDrive(
    image=flood_10.clip(roi),
    description=f"flood10_{location_name}",
    folder="GEE_Downloads",
    fileNamePrefix=f"flood10_{location_name}",
    region=roi,
    scale=90,
    crs="EPSG:4326",
    maxPixels=1e13
)

task.start()

print(task.status())

### Loop task status
while task.active():
    print("Export running...")
    time.sleep(10)

final_status = task.status()

if final_status["state"] == "COMPLETED":
    print("Export completed successfully!")
else:
    print("Export failed:")
    print(final_status)
