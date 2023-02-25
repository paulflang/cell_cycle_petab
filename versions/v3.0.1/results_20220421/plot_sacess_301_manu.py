from sys import builtin_module_names
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

cm = 1/2.54
textwidth = 14.79788*cm

matplotlib.rc('font', size=8)
plt.xlim(left=0)

B = np.array([0, 51, 204])/255
G = np.array([0, 128, 0])/255
O = np.array([255, 153, 0])/255
Y = np.array([255, 190, 0])/255
R = np.array([255, 0, 0])/255
GRAY = np.array([100, 100, 100])/255


# Options
exp = '../Stallaert_CellSystems2021_Data_2rounds.tsv'
opt = 'optimisation.tsv'
con = 'convergence_v3.0.1.csv'
image_file = 'v3.0.1_manu' # 'corr_n300_std0.8_vars9.png'
df_exp = pd.read_csv(exp, sep='\t').pivot(index='time', columns='observableId', values='measurement').iloc[::10, :]
df_opt = pd.read_csv(opt, sep='\t').pivot(index='time', columns='observableId', values='measurement')
df_con = pd.read_csv(con)

x_label = 'Time (h)'
y_label = 'Abundance (AU)'

legend_labels1 = ['CCNE', 'CCNA', 'CCNB1']
legend_labels2 = ['E2F1', 'RB1(Ser807_Ser811~p)']

variables1 = ['obs_cycE__nuc_median', 'obs_cycA__nuc_median', 'obs_cycB1__nuc_median']
variables2 = ['obs_E2F1__nuc_median', 'obs_pRB__nuc_median']

fig, axs = plt.subplots(2,2, figsize=(textwidth, textwidth/1.33))
((a, b), (cc, d)) = axs
fig.subplots_adjust(left=0.08, right=0.99, bottom=0.1, hspace=0.7, wspace=0.4)


##### Plotting A #####
colors = [B, G, O, Y, R, GRAY]
x_exp = df_exp.index/3600
x_opt = df_opt.index/3600 # df.loc[:, x_var_name]
a.set_prop_cycle(color=colors)
y = df_exp.loc[:, variables1] # df.loc[order, y_var_names]
a.plot(x_exp, np.array(y), 'o', markersize=2, markerfacecolor='none') # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables1] # df.loc[order, y_var_names]
a.set_prop_cycle(color=colors)
a.plot(x_opt, np.array(y), markersize=1) # See matplotlib.lines.Line2D for details

# Labelling
a.set_xlabel(x_label)
a.set_ylabel(y_label)

# Scientific notation
a.ticklabel_format(style='sci', scilimits=(-3,3))

a.annotate('a', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')
# a.set_title('Dot plot of cell population', fontdict={'fontweight': 'bold'})


##### Plotting B #####
y = df_exp.loc[:, variables2] # df.loc[order, y_var_names]
b.set_prop_cycle(color=colors[3:])
b.plot(x_exp, np.array(y), 'o', markersize=2, markerfacecolor='none') # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables2] # df.loc[order, y_var_names]
b.set_prop_cycle(color=colors[3:])
b.plot(x_opt, np.array(y), markersize=1) # See matplotlib.lines.Line2D for details

# Legend
handles = []
for c, l in zip(colors[:-1], legend_labels1+legend_labels2):
    handles.append(matplotlib.lines.Line2D([], [], color=c, marker='s', linestyle='None', markersize=6, label=l))

styles = [matplotlib.lines.Line2D([], [], color='k', marker='_', linestyle='None', markersize=8, label='Optimisation'), matplotlib.lines.Line2D([], [], color='k', marker='o', linestyle='None', markersize=2, markerfacecolor='none', label='Data')]
handles = handles + styles
b.legend(handles=handles, frameon=True, fontsize=8, loc='lower left', bbox_to_anchor=(0.05, -1.75)) # lower right 1.025, -1.75

# Labelling
b.set_xlabel(x_label)
b.set_ylabel(y_label)

# Scientific notation
b.ticklabel_format(style='sci', scilimits=(-3,3))

b.annotate('b', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')


##### Plotting C #####
x = df_con.loc[:, 'time(s)']/3600 # df.loc[:, x_var_name]
y = df_con.loc[:, 'fx'] # df.loc[order, y_var_names]
sacess = cc.plot(x, y, markersize=1, color='k', label='saCeSS') # See matplotlib.lines.Line2D for details
# cc.axhline(-429.247946, linestyle=':', color=GRAY, markersize=0.3, label='Ground truth')
# ground_truth = cc.annotate('Ground truth', xy=(0.2, 0.2), xycoords='axes fraction', label='Ground truth')

# cc.legend(frameon=True)

# Labelling
cc.set_xlabel(x_label)
cc.set_ylabel('Objective value')

# Scientific notation
cc.ticklabel_format(style='sci', scilimits=(-1,1))
cc.set_xscale('log')

cc.annotate('c', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')
# a.set_title('Dot plot of cell population', fontdict={'fontweight': 'bold'})

# Plot D
d.set_axis_off()


plt.savefig(image_file+'.pdf', dpi=600)
plt.savefig(image_file+'.png', dpi=600)
plt.close()
