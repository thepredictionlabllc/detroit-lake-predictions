import numpy as np
import matplotlib.pylab as plt
from matplotlib.pyplot import figure, show, rc
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from collections import OrderedDict
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd


####### PREDICTION PLOT
sns.set_style('white')
sns.set_context('notebook')
sns.set_style("whitegrid", {'axes.grid' : False})

def make_colormap(seq):
    """Return a LinearSegmentedColormap
    seq: a sequence of floats and RGB-tuples. The floats should be increasing
    and in the interval (0,1).
    """
    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])

    return mcolors.LinearSegmentedColormap('CustomMap', cdict)

c = mcolors.ColorConverter().to_rgb
rvb = make_colormap(
[c('red'), 0.125, c('red'), c('orange'), 0.25, c('orange'),c('green'),0.5, c('green'),0.7, c('green'), c('blue'), 0.75, c('blue')])


######################! Data
#path = "./Data/or_detroit_lake_dashboard/proc_dashboard_data/"
path = "/tmp/nj_oradell_reservoir_dashboard/proc_dashboard_data/"
pwd = path+"now_cast_tab/"
data = pd.read_csv(pwd + "nj_oradell_reservoir_nowcast_current_predictions.csv",parse_dates=["date"])
#data = pd.read_csv(pwd + "or_detroit_lake_nowcast_predictions.csv",parse_dates=["date"])
lag = 14

######################! Plot double pie
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(13,5))

labels = ('No Bloom', 'Bloom')
probs  = np.asarray([data.iloc[-lag]["bloom_1_p"],data.iloc[-lag]["bloom_p"]])
sizes  = probs * 100
explode = np.ones(len(sizes))*0.03
colors = cm.Greens([0.2,0.5])
patches, texts, autotexts = ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=5, pctdistance=0.8, explode = explode)
texts[0].set_fontsize(14)
texts[1].set_fontsize(14)
centre_circle = plt.Circle((0,0),0.30,fc='white')
ax1.add_artist(centre_circle)
ax1.axis('equal')  
ax1.annotate('-'+str(lag)+" days",
    xy=(0, 0),  # theta, radius
    horizontalalignment='center',
    verticalalignment='center',
    color='k',zorder=21,fontsize=23)

labels = ('No Bloom', 'Bloom')
probs  = np.asarray([data.iloc[-1]["bloom_1_p"],data.iloc[-1]["bloom_p"]])
sizes  = probs * 100
explode = np.ones(len(sizes))*0.03
colors = cm.Reds([0.2,0.5])
patches, texts, autotexts = ax2.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=5, pctdistance=0.8, explode = explode)
texts[0].set_fontsize(14)
texts[1].set_fontsize(14)
centre_circle = plt.Circle((0,0),0.30,fc='white')
ax2.add_artist(centre_circle)
ax2.axis('equal')  
ax2.annotate('+7 days',
    xy=(0, 0),  # theta, radius
    horizontalalignment='center',
    verticalalignment='center',
    color='k',zorder=21,fontsize=23)

plt.tight_layout()
plt.savefig("./Figs/Fig_prediction.png",dpi=600)




