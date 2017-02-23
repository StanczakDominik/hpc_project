import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
from matplotlib.ticker import MaxNLocator
import scipy
import os

# gather files
location = "/home/dominik/hpc/dane/"
prelude = """# 16500 events
master_workers,node1_workers,node2_workers,real_time\n"""
with open("klaster2.csv", "w") as of:
    of.write(prelude)
    for filename in os.listdir(location):
        with open(os.path.join(location, filename)) as f:
            of.write(f.readline() + "\n")


# csv read
with open("klaster2.csv") as f:
    first_line = f.readline()
    number_events = int(first_line.split()[1])
    df = pd.read_csv(f, index_col=None)
df['speed'] = number_events/df['real_time']
df['total_node_workers'] = df['node1_workers'] + df['node2_workers']
df['total_workers'] = df['total_node_workers'] + df['master_workers']
print(df)

# 2d plot

fig, ax = plt.subplots(figsize=(10,7))
for master_workers in range(4):
    cur_df = df[df['master_workers']==master_workers]
    x = cur_df['total_workers']
    y = cur_df['speed']
    ax.scatter(x,y, label=f"{master_workers} master workers")
plt.legend()
plt.grid()
plt.xlabel("Total workers")
plt.ylabel("Speed (Ev/s)")
plt.savefig('liniowy.png',bbox_inches='tight')
plt.show()

# 3d plot
workerrange = np.arange(0, 4.5, 0.5)
X,Y = np.meshgrid(workerrange, workerrange)
XX = X.flatten()
YY = Y.flatten()


fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
colors = ['b', 'y', 'g', 'r']
for master_workers in range(4):
    cur_df = df[(df['master_workers']==master_workers) & (df['total_workers'] < 12) & (df['total_workers'] > 1)]
    x = cur_df['node1_workers']
    y = cur_df['node2_workers']
    z = cur_df['speed']

    A = np.c_[x, y, np.ones(x.size)]
    C,_,_,_ = scipy.linalg.lstsq(A, z)    # coefficients
    print(master_workers, C)

    # evaluate it on grid
    Z = C[0]*X + C[1]*Y + C[2]

    ax.scatter(x,y,z, color=colors[master_workers], label=f"{master_workers} master workers")
    ax.plot_surface(X, Y, Z, color=colors[master_workers], rstride=1, cstride=1, alpha=0.2)

plt.legend()
plt.grid()
plt.xlabel("Node 1 workers")
plt.ylabel("Node 2 workers")
ax.set_zlabel("Speed (Ev/s)")
ax.set_xlim(0, 4)
ax.set_ylim(0, 4)
plt.savefig('3d.png',bbox_inches='tight' )
plt.show()

A = np.c_[ df['master_workers'], df['node1_workers'], df['node2_workers']]
C,_,_,_ = scipy.linalg.lstsq(A, df['speed'])    # coefficients
print(C)
