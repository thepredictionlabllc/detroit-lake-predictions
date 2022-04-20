import numpy as np
import matplotlib.pylab as plt
from matplotlib.pyplot import figure, show, rc
import matplotlib.cm as cm
from datetime import date
import pandas as pd
import runpy
today = date.today()



######## Climatology for long-term forecast
## Data
path = "/tmp/nj_oradell_reservoir_dashboard/proc_dashboard_data/"
pwd = path+"now_cast_tab/"
#data = pd.read_csv(pwd + "or_detroit_lake_nowcast_expected_longrun_predictions.csv",parse_dates=["date"])
data = pd.read_csv(pwd + "nj_oradell_reservoir_nowcast_longrun_predictions.csv",parse_dates=["date"])


data["month"] = data["date"].dt.month
data["week"] = data["date"].dt.week
data["year"] = data["date"].dt.year
data['dayofyear'] = data['date'].dt.dayofyear


######### Plot
import seaborn as sns
sns.set(style="whitegrid")

fig, ax = plt.subplots(figsize=(12,5))

#! Bar plots
ax = sns.barplot(x="month", y="prob_exp", data=data,capsize=.2)
mn = np.asarray(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
ax.set_xticklabels(mn)
plt.xlabel("Month",fontsize=14)
plt.ylabel("Bloom Risk Index",fontsize=14)

#! Time of the year
today = date.today()
mn = today.month
dy = today.day
x  = mn + (dy/30) - 1
plt.plot([x,x],[0,data["prob_exp"].max()],'r',linewidth=3)

#! Add text
font = {'family': 'sans-serif',
        'color':  'tomato',
        'weight': 'normal',
        'size': 16,
        }
plt.text(x,data["prob_exp"].max(),'Today',fontdict=font)

#! Save
plt.tight_layout()
plt.savefig("./Figs/Fig_climatology.png",dpi=600)
plt.show()


