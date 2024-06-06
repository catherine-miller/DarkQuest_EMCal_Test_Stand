##############################################################
# Title: plotGauss
# Description: Fit a Gaussian distribution to one or multiple
#     ROOT histograms.
# Arguments: 1. Channels, in two-digit format, separated by commas,
#    2. Runs numbers, separated by commas
#    E.g. python3 plotGauss.py 01,02 5000,5000
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 29 May 2024
###############################################################

import sys
from ROOT import *
from array import array
import pandas
import os
from IPython.display import display

gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0)

#Arguments
channels = str(sys.argv[1]).split(",") #in 2 digit format eg 03 or 12
runs = str(sys.argv[2]).split(",")

cols=[1,2,4,6,8,10,12,14,16]
f={}
h={}
fit={}
maximums = []
mpv = []
dmpv = []
title = ["High Gain","Low Gain"]
filenm = ["HG","LG"]
adcmax=[2000,8000]
fitmin = [150,100]
fitmax = [600,300]
hist = ["h_hgch","h_lgch"]
maxx= 30
homedir = "/home/cmiller6/"
for i in range(1):
  for ch in range(len(channels)):
    #f[ch]=TFile.Open("h_lgch"+channels[ch]+"_max_Run"+runs[ch]+".root","READ")
    #h[ch]=f[ch].Get("h_lgch"+channels[ch]+"_max")
    f[ch]=TFile.Open(homedir+"DataFiles/"+hist[i]+channels[ch]+"_Run"+runs[ch]+".root","READ")
    h[ch]=f[ch].Get(hist[i]+channels[ch])
    h[ch].SetLineColor(cols[ch])
    h[ch].SetMarkerColor(cols[ch])
    h[ch].SetMarkerSize(0.5)
    h[ch].SetMaximum(maxx)
    h[ch].SetMarkerStyle(20)
    h[ch].GetXaxis().SetRangeUser(fitmin[i],fitmax[i])
    fit[ch]=TF1("fit"+channels[ch],"gaus",fitmin[i],fitmax[i])
    fit[ch].SetLineColor(cols[ch])
    h[ch].Fit("fit"+channels[ch],"R")
    maximums.append(h[ch].GetMaximum())


  #draw superimposed
  c2 = TCanvas("c2","c2",800,600)
  c2.cd()
  leg2 = TLegend(0.6,0.55,0.85,0.85)
  #legs = ["Channel 0","Channel 1","No resistor"]
  for ch in range(len(channels)):
    leg2.AddEntry(fit[ch],"Channel "+channels[ch],"l")
    if (ch==0):
      h[ch].SetTitle("DarkQuest EMCal Cosmic Ray Test Stand, Run "+runs[i]+"; ADC ("+title[i]+"); Counts")
      #h[ch].SetTitle("Inter-Channel Calibration Test; ADC; Counts")
      h[ch].Draw("ep")
      fit[ch].Draw("lsame")
    else:
      h[ch].Draw("epsame")
      fit[ch].Draw("lsame")
      leg2.Draw()
    c2.SaveAs(homedir+"Figures/gaussian_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".pdf")
    c2.SaveAs(homedir+"Figures/gaussian_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".png")



  mpv = []
  mpverr = []
  for ch in range(len(channels)):
    mpv.append(fit[ch].GetParameter(1))
    mpverr.append(fit[ch].GetParError(1))
  print("Channel means:")
  print(mpv)
  print("Error in channel means:")
  print(mpverr)
  
''' 
#write to file which will be used to make plot
if not os.path.isfile("led_calib.csv"): 
  with open('led_calib.csv', 'w') as creating_new_csv_file: 
    pass
  close("mpv_5.csv")
df = pandas.read_csv("mpv_5.csv", names=["run","V","mpv","mpverr"],index_col=False)
#read a csv whose format is:
#run, channel, voltage, mpv, mpverr
dfsz = range(df.shape[0])
for i in range(len(channels)):
  replace = False
  for j in dfsz:
   # if int(channels[i])==df.loc[j,"ch"] and voltages[i]==df.loc[j,"V"]:
    if df.iat[j,1]==int(channels[i]) and df.iat[j,2]==voltages[i]:
      #if this channel and voltage are already stored in file, replace
      df.loc[j,"mpv"] = mpv[i]
      df.loc[j,"mpverr"] = mpverr[i]
      replace = True
  if replace == False:
    df1 = pandas.DataFrame(data=[[int(runs[i]),int(channels[i]),voltages[i],mpv[i],mpverr[i]]],columns=["run","ch","V","mpv","mpverr"])
    df = pandas.concat([df,df1])
#write to file
df.to_csv(path_or_buf="mpv_5.csv",header=False,index=False)
'''
