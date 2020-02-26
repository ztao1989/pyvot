import os
import sys
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vot_pytorch import UVWB
import utils

np.random.seed(19)

# Generate data
mean1 = [-0.5, 0.5]
cov1 = [[0.03, 0], [0, 0.01]]
x1, y1 = np.random.multivariate_normal(mean1, cov1, 5000).T
x1 = np.stack((x1, y1), axis=1).clip(-0.99, 0.99)

mean2 = [0.5, 0.5]
cov2 = [[0.01, 0.], [0., 0.03]]
x2, y2 = np.random.multivariate_normal(mean2, cov2, 1000).T
x2 = np.stack((x2, y2), axis=1).clip(-0.99, 0.99)

mean = [0.0, -0.5]
cov = [[0.02, 0], [0, 0.02]]
K = 50
x, y = np.random.multivariate_normal(mean, cov, K).T
x = np.stack((x, y), axis=1).clip(-0.99, 0.99)

use_gpu = False
if use_gpu and torch.cuda.is_available():
    device = 'cuda:0'
else:
    device = 'cpu'

x1 = torch.from_numpy(x1)
x2 = torch.from_numpy(x2)
x = torch.from_numpy(x)

vwb = UVWB(x, [x1, x2], device=device, verbose=False)
output = vwb.cluster(max_iter_h=5000, max_iter_p=1)
e_idx = output['e_idx']

xmin, xmax, ymin, ymax = -1.0, 1.0, 0., 1.


for idx in [21]:
    plt.figure(figsize=(8, 4))
    for i in range(2):
        ce = np.array(plt.get_cmap('viridis')(e_idx[i].cpu().numpy() / (K - 1)))
        utils.scatter_otsamples(vwb.data_p, vwb.data_e[i], size_p=30, marker_p='o', color_e=ce, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, facecolor_p='none')

    p = vwb.data_p[idx]

    for i in range(2):
        es = vwb.data_e[i][e_idx[i] == idx]
        for e in es:
            x = [p[0], e[0]]
            y = [p[1], e[1]]
            plt.plot(x, y, c='lightgray', alpha=0.4)

    # plt.savefig("ship" + str(idx) + ".svg")
    plt.savefig("ship" + str(idx) + ".png", dpi=300, bbox_inches='tight')

