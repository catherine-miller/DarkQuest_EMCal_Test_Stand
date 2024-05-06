##################################################################
# Description: Script to fit an ADC distribution to a Landau peak
# and find the MPV. Can work with multiples runs or channels.
#
# Arguments: Channel numbers (separated by commas), Run numbers
# (separated by commas), bias voltages (optional)
#
# Run with (e.g.) python plotMIPPeak.py 0,1,0,1 1948,1948,1949,1949
# This would plot channels 1 and 2 for runs 1948 and 1949
#
# Catherine Miller
# cmiller6@bu.edu
###################################################################

import sys
from ROOT import *
from array import array
#import pandas
import os
from IPython.display import display

gStyle.SetOptStat(0)
#gStyle.SetOptTitle(0)

#Arguments
channels = str(sys.argv[1]).split(",")
runs = str(sys.argv[2]).split(",")
voltages = len(channels)*[0]
for i in range(len(sys.argv)-3):
  voltages[i]=float(sys.argv[i+3])

cols=[1,2,4,6,8,10,12,14,16]
f={}
h={}
fit={}
maximums = []
bias = [40.0,40.5,41.0,41.5,42.0]
mpv = []
dmpv = []
title = ["Low Gain","High Gain"]
filenm = ["LG","HG"]
adcmax=[800,800]
fitmin = [[50,100,100,400],[20,20,20,20]]
fitmax = [[600,600,600,3000],[800,800,800,800]]
hist = ["h_lgch","h_hgch"]
maxx= 50
for i in range(1):
  for ch in range(len(channels)):
    #f[ch]=TFile.Open("h_lgch"+channels[ch]+"_max_Run"+runs[ch]+".root","READ")
    #h[ch]=f[ch].Get("h_lgch"+channels[ch]+"_max")
    f[ch]=TFile.Open(hist[i]+channels[ch]+"_Run"+runs[ch]+".root","READ")
    h[ch]=f[ch].Get(hist[i]+channels[ch])
    h[ch].SetLineColor(cols[ch])
    h[ch].SetMarkerColor(cols[ch])
    h[ch].SetMarkerSize(0.5)
    h[ch].SetMarkerStyle(20)
    #fit[ch]=TF1("fit"+channels[ch],"landau(0)+expo(3)",300,2024)
    #fit[ch]=TF1("fit"+channels[ch],"landau(0)",320,1200)
    fit[ch]=TF1("fit"+channels[ch],"landau(0)",fitmin[i][ch],fitmax[i][ch])
    fit[ch].SetLineColor(cols[ch])
    h[ch].Fit("fit"+channels[ch],"R")
    h[ch].SetTitle("MPV for Channel"+str(ch)+", V="+str(voltages[ch]))
    maximums.append(h[ch].GetMaximum())

    print(maximums)
    print(max(maximums))

  legend =[]
  c1 = TCanvas("c1","c1",800,600)
  c1.Divide(2,int(len(channels)/2+len(channels)%2))
  #c1.SetLogy()
  for ch in range(len(channels)):
    c1.cd(ch+1)
    h[ch].SetMaximum(maxx)
    #h[ch].SetMaximum(1400)
    #h[ch].GetXaxis().SetRangeUser(200,1200)
    h[ch].GetXaxis().SetRangeUser(0,adcmax[i])
    h[ch].SetTitle("Channel "+str(ch)+"; ADC (Low Gain); Counts")
    #h[ch].GetYaxis().SetRangeUser(0,600)
    if (ch==0):
      h[ch].Draw("ep")
      legend.append(TLegend(0.6,0.55,0.85,0.85))
      legend[ch].SetTextSize(0.05)
      legend[ch].AddEntry(fit[ch],"V = "+str(voltages[ch]),"l")
      #fit[ch].Draw("lsame")
    else:
      h[ch].Draw("ep")
      #fit[ch].Draw("lsame")
      legend.append(TLegend(0.6,0.55,0.85,0.85))
      legend[ch].SetTextSize(0.05)
      legend[ch].AddEntry(fit[ch],"V = "+str(voltages[ch]),"l")
      #legend[ch].Draw("same")
    c1.SaveAs("MIPPeak_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".pdf")
    c1.SaveAs("MIPPeak_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".png")
 
  c3 = TCanvas("c3","c3",800,600)
  c3.Divide(2,int(len(channels)/2+len(channels)%2))
  #c1.SetLogy()
  for ch in range(len(channels)):
    c3.cd(ch+1)
    h[ch].SetMaximum(maxx)
    #h[ch].SetMaximum(1400)
    #h[ch].GetXaxis().SetRangeUser(200,1200)
    h[ch].GetXaxis().SetRangeUser(0,adcmax[i])
    h[ch].SetTitle("Channel "+str(ch)+"; ADC ("+title[i]+"); Counts")
    #h[ch].GetYaxis().SetRangeUser(0,600)
    if (ch==0):
      h[ch].Draw("ep")
      #fit[ch].Draw("lsame")
    else:
      h[ch].Draw("ep")
      #fit[ch].Draw("lsame")
      legend.append(TLegend(0.6,0.55,0.85,0.85))
      legend[ch].SetTextSize(0.05)
      legend[ch].AddEntry(fit[ch],"V = "+str(voltages[ch]),"l")
      #legend[ch].Draw("same")
    c3.SaveAs("MIPPeak_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".pdf")
    c3.SaveAs("MIPPeak_"+filenm[i]+"_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".png")

  #draw superimposed
  c2 = TCanvas("c2","c2",800,600)
  c2.cd()
  leg2 = TLegend(0.6,0.55,0.85,0.85)
  legs = ["Channel 2, PLU trigger","Channel 3, PLU trigger","Channel 2, mini-DAQ trigger","Channel 3, mini-DAQ trigger"]
  for ch in range(len(channels)):
    #leg2.AddEntry(fit[ch],"Ch. "+channels[ch],"l")
    #leg2.AddEntry(fit[ch],"Ch. "+channels[ch]+" , V = "+str(voltages[ch])+" V","l")
    leg2.AddEntry(fit[ch],legs[ch],"l")
    if (ch==0):
      h[ch].SetTitle("DarkQuest EMCal Cosmic Ray Test Stand; ADC ("+title[i]+"); Counts")
      #h[ch].SetTitle("Inter-Channel Calibration Test; ADC; Counts")
      h[ch].Draw("ep")
      fit[ch].Draw("lsame")
    else:
      h[ch].Draw("epsame")
      fit[ch].Draw("lsame")
      leg2.Draw()
    c2.SaveAs("MIPPeak_"+filenm[i]+"_superimp_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".pdf")
    c2.SaveAs("MIPPeak_"+filenm[i]+"_superimp_Ch_"+str(sys.argv[1]).replace(",","_")+"_Run_"+str(sys.argv[2]).replace(",","_")+".png")



  mpv = []
  mpverr = []
  for ch in range(len(channels)):
    mpv.append(fit[ch].GetParameter(1))
    mpverr.append(fit[ch].GetParError(1))
  print(mpv,mpverr)
 
#write to file which will be used to make plot
'''
if not os.path.isfile("mpv_5.csv"): 
  with open('mpv_5.csv', 'w') as creating_new_csv_file: 
    pass
  close("mpv_5.csv")
df = pandas.read_csv("mpv_5.csv", names=["run","ch","V","mpv","mpverr"],index_col=False)
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
#df.to_csv(path_or_buf="mpv_5.csv",header=False,index=False)
'''
