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
path = "/tmp/or_detroit_lake_dashboard/proc_dashboard_data/"
pwd = path+"now_cast_tab/"
data = pd.read_csv(pwd + "or_detroit_lake_nowcast_multiclass_predictions_current.csv",parse_dates=["date"])
lag = 14 #number of days to look behind
probs_14 = np.asarray([data.iloc[[-lag]]['none_bloom_p'],data.iloc[[-lag]]['low_bloom_p'],\
			data.iloc[[-lag]]['mid_bloom_p'],data.iloc[[-lag]]['high_bloom_p']])
probs_1 = np.asarray([data.iloc[[-1]]['none_bloom_p'],data.iloc[[-1]]['low_bloom_p'],\
			data.iloc[[-1]]['mid_bloom_p'],data.iloc[[-1]]['high_bloom_p']])


# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Plot the first pie chart with legend and no labels
labels = ('No Detection', 'Algae Present', 'Algal Bloom')
probs = probs_14.flatten()
probs = [probs[0], probs[1] + probs[2], probs[3]]
probs = probs / np.sum(probs)
sizes = probs * 100
explode = np.ones(len(sizes)) * 0.03
colors = plt.cm.Greens(np.linspace(0.15, 0.7, len(probs)))
ax1.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=95, pctdistance=0.8, explode=explode, labels=None)
centre_circle1 = plt.Circle((0, 0), 0.30, fc='white')
ax1.add_artist(centre_circle1)
ax1.axis('equal')
ax1.annotate('-14days',
             xy=(0, 0),  # theta, radius
             horizontalalignment='center',
             verticalalignment='center',
             color='k', zorder=21, fontsize=23)
ax1.legend(labels, loc="best", fontsize=12)

# Plot the second pie chart with legend and no labels
labels = ('No Detection', 'Algae Present', 'Algal Bloom')
probs = probs_1.flatten()
probs = [probs[0], probs[1] + probs[2], probs[3]]
probs = probs / np.sum(probs)
sizes = probs * 100
explode = np.ones(len(sizes)) * 0.03
colors = plt.cm.Reds(np.linspace(0.15, 0.7, len(probs)))
ax2.pie(sizes, colors=colors, autopct='%1.1f%%', startangle=95, pctdistance=0.8, explode=explode, labels=None)
centre_circle2 = plt.Circle((0, 0), 0.30, fc='white')
ax2.add_artist(centre_circle2)
ax2.axis('equal')
ax2.annotate('+7days',
             xy=(0, 0),  # theta, radius
             horizontalalignment='center',
             verticalalignment='center',
             color='k', zorder=21, fontsize=23)
ax2.legend(labels, loc="best", fontsize=12)

plt.tight_layout()
plt.savefig("./Figs/Fig_prediction.png", dpi=600)
plt.show()






# Old figure without legend
######################! Plot double pie
fig, (ax1,ax2) = plt.subplots(1,2,figsize=(13,5))

labels = ('No Detection', 'Algae Present', 'Algal Bloom')
probs  = probs_14.flatten()
probs = [probs[0],probs[1]+probs[2],probs[3]]
probs = probs / np.sum(probs)
sizes  = probs * 100
explode = np.ones(len(sizes))*0.03
colors = cm.Greens(np.linspace(0.15,.7,len(probs)))
patches, texts, autotexts = ax1.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=95, pctdistance=0.8, explode = explode)
texts[0].set_fontsize(14)
texts[1].set_fontsize(14)
texts[2].set_fontsize(14)
#texts[3].set_fontsize(14)
centre_circle = plt.Circle((0,0),0.30,fc='white')
ax1.add_artist(centre_circle)
ax1.axis('equal')  
ax1.annotate('-14days',
    xy=(0, 0),  # theta, radius
    horizontalalignment='center',
    verticalalignment='center',
    color='k',zorder=21,fontsize=23)

labels = ('No Detection', 'Algae Present', 'Algal Bloom')
probs  = probs_1.flatten()
probs = [probs[0],probs[1]+probs[2],probs[3]]
probs = probs / np.sum(probs)
sizes  = probs * 100
explode = np.ones(len(sizes))*0.03
colors = cm.Reds(np.linspace(0.15,.7,len(probs)))
patches, texts, autotexts = ax2.pie(sizes, colors = colors, labels=labels, autopct='%1.1f%%', startangle=95, pctdistance=0.8, explode = explode)
texts[0].set_fontsize(14)
texts[1].set_fontsize(14)
texts[2].set_fontsize(14)
#texts[3].set_fontsize(14)
centre_circle = plt.Circle((0,0),0.30,fc='white')
ax2.add_artist(centre_circle)
ax2.axis('equal')
ax2.annotate('+7days',
    xy=(0, 0),  # theta, radius
    horizontalalignment='center',
    verticalalignment='center',
    color='k',zorder=21,fontsize=23)

plt.tight_layout()
plt.savefig("./Figs/Fig_prediction.png",dpi=600)




