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
import botocore.session
import s3fs

session = botocore.session.get_session()
AWS_SECRET = session.get_credentials().secret_key
AWS_ACCESS_KEY = session.get_credentials().access_key 

s3 = s3fs.S3FileSystem(anon=False, key=AWS_ACCESS_KEY, secret=AWS_SECRET)

username =  os.environ.get('USER')

mapbox = importfile(f"/home/{username}/.mapbox/credentials")

MAPBOX_KEY = mapbox.mapbox_id

################ SATELLITE CHL-A ####################
#path = "./Data/or_detroit_lake_dashboard/proc_dashboard_data/"
# path = "/tmp/or_detroit_lake_dashboard/proc_dashboard_data/"
# files = sorted(glob.glob(path+"cyan_map/*.csv"))

files = sorted(s3.glob(f"s3://cwa-assets/or_detroit_lake/assets/cyan_map/*.csv"))

#! Latest data
data = pd.read_csv(f"s3://{files[-1]}",parse_dates=["date"])
data["month"] = data["date"].dt.month
data["week"] = data["date"].dt.week
data["year"] = data["date"].dt.year
data['dayofyear'] = data['date'].dt.dayofyear

#! Xd trailing average
X = 3; # number of trailing days to average over
lons = data["lon"]
lats = data["lat"]
df = data.copy()
allCyan = df["log_CI_cells_mL"].to_numpy().reshape((-1,1))

# get lagged readings
for i in np.arange(-X,-1):
    df1 = pd.read_csv(f"s3://{files[i]}",parse_dates=["date"])
    newCyan = griddata((df1["lon"],df1["lat"]), df1["log_CI_cells_mL"],(lons, lats), method='nearest').reshape((-1,1))
    allCyan = np.hstack([allCyan, newCyan])

df["log_CI_cells_mL"] = np.nanmean(allCyan, 1)



#################### MAKE MAP (average of last week) ################
#! Data to plot
x = np.asarray(df.lon)
y = np.asarray(df.lat)
z = np.asarray(df.log_CI_cells_mL)
ID = np.where(z!=0)[0]
x = x[ID]; y = y[ID]; z = np.exp(z[ID])


df = {'x': x,
        'y': y,
        'z': z}
df = pd.DataFrame(df)

import plotly.figure_factory as ff
import plotly.express as px

px.set_mapbox_access_token(MAPBOX_KEY)
date_time = data.date[0].strftime("%m/%d/%Y")
title = "CyAN (cells per ml): " + date_time

some_lat = 44.70589274280469
some_lon = -122.18866619594027

fig = ff.create_hexbin_mapbox(
    data_frame=df, lat="y", lon="x", color="z",
    nx_hexagon=5, opacity=0.5,
    range_color=[6000, 100000],
    labels={"color": "Cells/ml"}, agg_func=np.mean, color_continuous_scale="jet"
)
fig.update_layout(
    title_text=title, title_y=0.92, title_x=0.2,
    mapbox=dict(
        style="satellite",
        zoom=13,  # Adjust this value to zoom out (lower values mean more zoomed out)
        center=dict(lat=some_lat, lon=some_lon)  # Replace with the center of your data
    )
)
fig.write_image("Figs/Fig_cyan.png", scale=1)

# fig = ff.create_hexbin_mapbox(
#     data_frame=df, lat="y", lon="x", color="z",
#     nx_hexagon=20, opacity=0.5,
#     range_color=[6000,100000],
#     labels={"color": "Cells/ml"},agg_func=np.nanmean,color_continuous_scale="jet")
# fig.update_layout(title_text=title,title_y=0.92,title_x=0.2)
# fig.update_layout(mapbox_style="satellite")
# fig.write_image("Figs/Fig_cyan.png",scale=2)
# plt.close("all")
