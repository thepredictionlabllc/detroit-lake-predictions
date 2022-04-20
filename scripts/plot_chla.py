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


from mpl_toolkits import axes_grid1

def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


### Setup map
def image_spoof(self, tile): # this function pretends not to be a Python script
    url = self._image_url(tile) # get the url of the street map API
    req = Request(url) # start request
    req.add_header('User-agent','Anaconda 3') # add user agent to request
    fh = urlopen(req)
    im_data = io.BytesIO(fh.read()) # get image
    fh.close() # close url
    img = Image.open(im_data) # open image with PIL
    img = img.convert(self.desired_tile_form) # set image format
    return img, self.tileextent(tile), 'lower' # reformat for cartopy

cimgt.OSM.get_image = image_spoof # reformat web request for street map spoofing
#osm_img = cimgt.OSM() # spoofed, downloaded street map << Open Street Map
osm_img = cimgt.QuadtreeTiles() # spoofed, downloaded street map << Sat image



################ SATELLITE CHL-A ####################
#path = "./Data/or_detroit_lake_dashboard/proc_dashboard_data/"
path = "/tmp/nj_oradell_reservoir_dashboard/proc_dashboard_data/"
files = sorted(glob.glob(path+"satellite_map/*.csv"))

##! find colorbounds
#chl_min = [] 
#chl_min = [] 
#for i in np.arange(int(len(files)/2),len(files)):
#	data = pd.read_csv(files[i],parse_dates=["date"])
#	chl_min = np.append(chl_min,np.percentile(data['Chlorophyll'],5))
#	chl_max = np.append(chl_max,np.percentile(data['Chlorophyll'],95))
#	print(i)
#chl_min = np.percentile(chl_min,5)
#chl_max = np.percentile(chl_max,95)

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
for i in np.arange(-X,-1):
    df1 = pd.read_csv(files[i],parse_dates=["date"])
    df["Chlorophyll"] = (df["Chlorophyll"] + griddata((df1["lon"],df1["lat"]), df1["Chlorophyll"], 
            (lons, lats), method='nearest')) / 2



#################### MAKE MAP (average of last week) ################
#! Data to plot
x = np.asarray(df.lon)
y = np.asarray(df.lat)
z = np.asarray(df.Chlorophyll)
ID = np.where(z!=0)[0]
x = x[ID]; y = y[ID]; z = z[ID]
zl = np.log10(z+1)

fig = plt.figure(figsize=(7,5.5)) # open matplotlib figure
ax1 = plt.axes(projection=osm_img.crs) # project using coordinate reference system (CRS) of street map

date_time = data.date[0].strftime("%m/%d/%Y")
plt.title("Chlorophyll-a (Sentinel 2a): " + date_time)

center_pt = [np.mean(data.lat), np.mean(data.lon)] # lat/lon of One World Trade Center in NYC
zoom = 0.025 # for zooming out of center point
extent = [center_pt[1]-(zoom*2.0),center_pt[1]+(zoom*2.0), \
	center_pt[0]-zoom,center_pt[0]+zoom] # adjust to zoom
ax1.set_extent(extent) # set extents

scale = np.ceil(-np.sqrt(2)*np.log(np.divide(zoom,350.0))) # empirical solve for scale based on zoom
scale = (scale<14) and scale or 14 # scale cannot be larger than 19
ax1.add_image(osm_img, int(scale)) # add OSM with zoom specification
# NOTE: zoom specifications should be selected based on extent:
# -- 2     = coarse image, select for worldwide or continental scales
# -- 4-6   = medium coarseness, select for countries and larger states
# -- 6-10  = medium fineness, select for smaller states, regions, and cities
# -- 10-12 = fine image, select for city boundaries and zip codes
# -- 14+   = extremely fine image, select for roads, blocks, buildings

#! colorlimits (in this specific data)
#vmin = np.percentile(z,5)
#vmax = np.percentile(z,95)
vmin = 0.5
vmax = 2.25

#! plot points
im = ax1.scatter(x,y,4,z,marker='s',alpha=.9,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree(),cmap="jet",edgecolors='none')

#! Colorbar
cax = fig.add_axes([ax1.get_position().x1+0.01,ax1.get_position().y0,0.02,ax1.get_position().height])
cbar = plt.colorbar(im,cax=cax)
ticks = cbar.get_ticks()
ticks = len(ticks)*[None]
ticks[0] = "Low"
ticks[-1] = "High"
cbar.ax.set_yticklabels(ticks)


plt.savefig("./Figs/Fig_chla_week.png",dpi=300,bbox_inches='tight')
plt.close("all")
