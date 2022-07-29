import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import matplotlib as mpl
import cartopy.feature as cfeature
import numpy as np
import io
from urllib.request import urlopen, Request
from PIL import Image
from scipy.interpolate import griddata
from mpl_toolkits.axes_grid1 import make_axes_locatable
import os
from pydoc import importfile

username =  os.environ.get('USER')

mapbox = importfile(f"/home/{username}/.mapbox/credentials")

MAPBOX_KEY = mapbox.mapbox_id

################ SATELLITE CHL-A ####################
#path = "./Data/or_detroit_lake_dashboard/proc_dashboard_data/"
path = "/tmp/or_detroit_lake_dashboard/proc_dashboard_data/"
files = sorted(glob.glob(path+"satellite_map/*.csv"))

#! Latest data
data = pd.read_csv(files[-1],parse_dates=["date"])
data["month"] = data["date"].dt.month
data["week"] = data["date"].dt.week
data["year"] = data["date"].dt.year
data['dayofyear'] = data['date'].dt.dayofyear

#! Xd trailing average
X = 3; # number of trailing days to average over
lons = data["lon"]
lats = data["lat"]
df = data.copy()
allChl = df["Chlorophyll"].to_numpy().reshape((-1,1))

# get lagged readings
for i in np.arange(-X,-1):
    df1 = pd.read_csv(files[i],parse_dates=["date"])
    newChl = griddata((df1["lon"],df1["lat"]), df1["Chlorophyll"],(lons, lats), method='nearest').reshape((-1,1))
    allChl = np.hstack([allChl, newChl])

df["Chlorophyll"] = np.nanmean(allChl, 1)



#################### MAKE MAP (average of last week) ################
#! Data to plot
x = np.asarray(df.lon)
y = np.asarray(df.lat)
z = np.asarray(np.log(1 + df.Chlorophyll))
ID = np.where(z!=0)[0]
x = x[ID]; y = y[ID];
z = z[ID]
#z = z / z.max()
#z = np.round(z * 100)

df = {'x': x,
        'y': y,
        'z': z}
df = pd.DataFrame(df)

import plotly.figure_factory as ff
import plotly.express as px

px.set_mapbox_access_token(MAPBOX_KEY)
date_time = data.date[0].strftime("%m/%d/%Y")
title = "Chlorophyll-a Index (Sentinel 2a): " + date_time

fig = ff.create_hexbin_mapbox(
    data_frame=df, lat="y", lon="x", color="z",
    nx_hexagon=70, opacity=0.5,
    range_color=[0, 0.90],
    labels={"color": "Chl-a Index"},agg_func=np.mean,color_continuous_scale="jet")

fig.update_layout(title_text=title,title_y=0.92,title_x=0.2)
#fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(mapbox_style="satellite")
fig.write_image("Figs/Fig_chla.png",scale=2)
plt.close("all")
