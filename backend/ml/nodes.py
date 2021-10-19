"""
Node class used in "licchavi.py"
"""

import torch


class Node:
    def __init__(
            self, vid1, vid2, rating, vids,
            mask, t_param, s_param, model, weight,
            lr_loc, lr_t, lr_s, opt):
        """
        vid1 (bool 2D tensor): one line is a one-hot-encoded video index
        vid2 (bool 2D tensor): one line is a one-hot-encoded video index
        rating (float tensor): comparisons corresponding to vid1 and vid2 lines
        vids (FIXME): video IDs
        mask (bool tensor): True for all video indexes rated by user
        t_param (float tensor): t (translation) learnable parameter
        s_param (float tensor): s (scaling) learnable parameter
        model (float tensor): learnable tensor of all video scores
        weight (float): node ponderation for generalisation (its influence)
        lr_loc (float): learning rate of self.model
        lr_t (float): learning rate of self.t_param
        lr_s (float): learning rate of self.s_param
        opt (torch.optim.Optimizer): gradient descent optimizer
        """
        self.vid1 = vid1
        self.vid2 = vid2
        self.rating = rating
        self.vids = vids
        self.mask = mask
        self.t_param = t_param
        self.s_param = s_param
        self.model = model
        self.weight = weight
        self.lr_t = lr_t / len(vids)  # adaptative lr
        self.lr_s = lr_s / len(vids)  # adaptative lr
        self.opt = opt(
            [
                {'params': self.model},
            ],
            lr=lr_loc
        )
        self.opt_t_s = opt(
            [
                {'params': self.t_param, 'lr': self.lr_t},
                {'params': self.s_param, 'lr': self.lr_s},
            ]
        )

        self.nb_comps = self._count_comps()  # number of comparisons
        self.delta_na = 1 / torch.sqrt(self.nb_comps)  # needed for loss later
        _ = torch.nan_to_num_(self.delta_na, posinf=1)  # avoiding NaNs

    def _count_comps(self):
        """ Counts number of comparisons for each video

        Returns:
            (int tensor): number of comparisons for each video index
        """
        return torch.sum(self.vid1, axis=0) + torch.sum(self.vid2, axis=0)