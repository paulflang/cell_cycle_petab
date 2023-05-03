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
V = np.array([155, 0, 255])/255
T = np.array([0, 255, 255])/255


# Options
exp = '../Stallaert_CellSystems2021_Data_2rounds.tsv'
opt = 'optimisation.tsv'
con = 'convergence_v4.0.0.csv'  # concatenating the sheets PEtab_PL_v4_0_0_comm_Nov14_it1 + PEtab_PL_v4_0_0_comm_Nov14_it2 + PL_v4_0_0_commit_Jan10_2022_it1
image_file = 'v4.0.0_manu' # 'corr_n300_std0.8_vars9.png'
df_exp = pd.read_csv(exp, sep='\t').pivot(index='time', columns='observableId', values='measurement').iloc[::10, :]
df_opt = pd.read_csv(opt, sep='\t').pivot(index='time', columns='observableId', values='measurement')
df_con = pd.read_csv(con)

x_label = 'Time (h)'
y_label = 'Abundance (AU)'
y_label1 = 'Abundance (AU)'

legend_labels1 = ['CCNE', 'CCNA', 'CCNB1']
legend_labels2 = ['E2F1', 'RB1(Ser807_Ser811~p)', 'SKP2']
legend_labels3 = ['CDKN1A', 'CDKN1B']

variables1 = ['obs_cycE__nuc_median', 'obs_cycA__nuc_median', 'obs_cycB1__nuc_median']
variables2 = ['obs_E2F1__nuc_median', 'obs_pRB__nuc_median', 'obs_Skp2__nuc_median']
variables3 = ['obs_p21__nuc_median', 'obs_p27__nuc_median']

variables4 = ['obs_cycE__cyt_median', 'obs_cycA__cyt_median', 'obs_cycB1__cyt_median']
variables5 = ['obs_E2F1__cyt_median', 'obs_pRB__cyt_median', 'obs_Skp2__cyt_median']
variables6 = ['obs_p21__cyt_median', 'obs_p27__cyt_median']

fig, axs = plt.subplots(4,2, figsize=(textwidth, 2*textwidth/1.33))
((a, b), (c, d), (e, f), (g, h)) = axs
fig.subplots_adjust(left=0.1, right=0.99, bottom=2*0.1/1.5, hspace=0.7, wspace=0.4)


##### Plotting A #####
colors = [B, G, O, Y, R, GRAY, V, T]
x_exp = df_exp.index/3600
x_opt = df_opt.index/3600 # df.loc[:, x_var_name]
a.set_prop_cycle(color=colors)
y = df_exp.loc[:, variables1] # df.loc[order, y_var_names]
a.plot(x_exp, np.array(y), 'o', markersize=1) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables1] # df.loc[order, y_var_names]
a.set_prop_cycle(color=colors)
a.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
a.set_xlabel(x_label)
a.set_ylabel(y_label)

# Scientific notation
a.ticklabel_format(style='sci', scilimits=(-3,3))

a.annotate('a', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')
a.set_title('Nucleus', fontdict={'fontweight': 'bold'})


##### Plotting B #####
x_exp = df_exp.index/3600
x_opt = df_opt.index/3600 # df.loc[:, x_var_name]
b.set_prop_cycle(color=colors)
y = df_exp.loc[:, variables4] # df.loc[order, y_var_names]
b.plot(x_exp, np.array(y), 'o', markersize=1, ) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables4] # df.loc[order, y_var_names]
b.set_prop_cycle(color=colors)
b.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
b.set_xlabel(x_label)
b.set_ylabel(y_label1)

# Scientific notation
b.ticklabel_format(style='sci', scilimits=(-3,3))

b.annotate('b', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')
b.set_title('Cytoplasm', fontdict={'fontweight': 'bold'})


##### Plotting C #####
y = df_exp.loc[:, variables2] # df.loc[order, y_var_names]
c.set_prop_cycle(color=colors[3:])
c.plot(x_exp, np.array(y), 'o', markersize=1, ) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables2] # df.loc[order, y_var_names]
c.set_prop_cycle(color=colors[3:])
c.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
c.set_xlabel(x_label)
c.set_ylabel(y_label)

# Scientific notation
c.ticklabel_format(style='sci', scilimits=(-3,3))

c.annotate('c', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')


##### Plotting D #####
y = df_exp.loc[:, variables5] # df.loc[order, y_var_names]
d.set_prop_cycle(color=colors[3:])
d.plot(x_exp, np.array(y), 'o', markersize=1, ) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables5] # df.loc[order, y_var_names]
d.set_prop_cycle(color=colors[3:])
d.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
d.set_xlabel(x_label)
d.set_ylabel(y_label)

# Scientific notation
d.ticklabel_format(style='sci', scilimits=(-3,3))

d.annotate('d', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')


##### Plotting E #####
y = df_exp.loc[:, variables3] # df.loc[order, y_var_names]
e.set_prop_cycle(color=colors[6:])
e.plot(x_exp, np.array(y), 'o', markersize=1, ) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables3] # df.loc[order, y_var_names]
e.set_prop_cycle(color=colors[6:])
e.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
e.set_xlabel(x_label)
e.set_ylabel(y_label)

# Scientific notation
e.ticklabel_format(style='sci', scilimits=(-3,3))

e.annotate('e', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')


##### Plotting F #####
y = df_exp.loc[:, variables6] # df.loc[order, y_var_names]
f.set_prop_cycle(color=colors[6:])
f.plot(x_exp, np.array(y), 'o', markersize=1, ) # See matplotlib.lines.Line2D for details
y = df_opt.loc[:, variables6] # df.loc[order, y_var_names]
f.set_prop_cycle(color=colors[6:])
f.plot(x_opt, np.array(y)) # See matplotlib.lines.Line2D for details

# Labelling
f.set_xlabel(x_label)
f.set_ylabel(y_label)

# Scientific notation
f.ticklabel_format(style='sci', scilimits=(-3,3))

f.annotate('f', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')


# ##### Plotting G #####
x = df_con.loc[:, 'time(s)']/3600 # df.loc[:, x_var_name]
y = df_con.loc[:, 'fx'] # df.loc[order, y_var_names]
sacess = g.plot(x, y, markersize=1, color='k', label='saCeSS') # See matplotlib.lines.Line2D for details
# cc.axhline(-429.247946, linestyle=':', color=GRAY, markersize=0.3, label='Ground truth')
# ground_truth = cc.annotate('Ground truth', xy=(0.2, 0.2), xycoords='axes fraction', label='Ground truth')
g.set_title('Convergence curve', fontdict={'fontweight': 'bold'})

# cc.legend(frameon=True)

# Labelling
g.set_xlabel(x_label)
g.set_ylabel('Objective value')

# Scientific notation
g.ticklabel_format(style='sci', scilimits=(-1,1))
g.set_xscale('log')

g.annotate('g', xy=(-0.2, 1.15), fontsize=14, fontweight='bold', xycoords='axes fraction')
# a.set_title('Dot plot of cell population', fontdict={'fontweight': 'bold'})

##### Plotting H #####
h.set_axis_off()

# Legend
handles = []
for c, l in zip(colors, legend_labels1+legend_labels2+legend_labels3):
    handles.append(matplotlib.lines.Line2D([], [], color=c, marker='s', linestyle='None', label=l))

styles = [matplotlib.lines.Line2D([], [], color='k', marker='_', linestyle='None', label='Simulation'), matplotlib.lines.Line2D([], [], color='k', marker='o', linestyle='None', markerfacecolor='k', label='Data', markersize=2)]
handles = handles + styles
f.legend(handles=handles, frameon=True, loc='lower left', bbox_to_anchor=(-0.25, -1.67), ncol=2, columnspacing=0.7, labelspacing=0.7, handletextpad=0.2) # lower right 1.025, -1.75


plt.savefig(image_file+'.pdf', dpi=600)
plt.savefig(image_file+'.png', dpi=600)
plt.savefig(image_file+'.svg', dpi=600)
plt.close()
