# plot_limits.py

from __future__ import division
from ROOT import *
import glob
import uuid
import os
import json

gROOT.SetBatch(True)
gStyle.SetOptStat(0)
TH1D.SetDefaultSumw2()


def plotLimit(json_file):
    with open(json_file, "r") as read_file:
        data = json.load(read_file)
    
    ctau_list = [float(ct) for ct in data]
    ctau_list.sort()
    
    for ctau in ctau_list:
        print "{0} : {1}".format(ctau, data[str(ctau)]["exp0"])
    
    exp0_list = [data[str(ct)]["exp0"] for ct in ctau_list]
    
    print ctau_list
    print exp0_list
    n_bins = len(exp0_list)
    h_exp0 = TH1D("h_exp0","h_exp0", n_bins, 0, n_bins)
    for i, limit in enumerate(exp0_list):
        h_exp0.Fill(i, limit) 
    canvas = TCanvas("canvas", "canvas", 900, 800)
    h_exp0.Draw("hist")
    h_exp0.GetYaxis().SetRangeUser(0, 0.2)
    h_exp0.SetTitle("Limits")
    h_exp0.SetLineColor(kBlack)
    canvas.SaveAs("limits.pdf")

# # Physics processes
# procs = [
#     'Signal',
#     'PrEle',
#     'PrMu',
#     'Fake'
#     ]
# 
# # limits for each bin
# limits = [0.5, 1.0, 2.0, 4.0]
# plotLimit(limits)

# limit plot: each bin is a different ctau

json_file = "limits.json"

plotLimit(json_file)

