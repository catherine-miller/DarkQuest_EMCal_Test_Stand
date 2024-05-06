###########################################################################
# Title: VoltageStudies
# Description: Generate a plot of gain factor vs. overvoltage and resolution
#     vs. overvoltage.
# Run with: python3 VoltageScan.py
# Author: Catherine Miller, cmiller6@bu.edu
# Date: 29 April 2024
###########################################################################

from ROOT import TCanvas, TGraphErrors, TF1, Math, TLegend
from ROOT import gROOT
from array import array
import pandas
import sys
import numpy as np

sipmnames =['1','2','3','4']
homedir = '/home/cmiller6/'

c1 = TCanvas( 'c1', 'Gain factor v voltage', 200, 10, 700, 500 )
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
leg1 = TLegend(0.7,0.65,0.85,0.85)

c2 = TCanvas( 'c2', 'Resolution v gain', 200, 10, 700, 500 )
c2.cd() 
c2.SetGrid()
c2.GetFrame().SetFillColor( 21 )
c2.GetFrame().SetBorderSize( 12 )
leg2 = TLegend(0.7,0.65,0.85,0.85)

#get data from file
cols = ["run","voltage","mpv","mpverr","stddev","stddeverr"]
for ch in range(4):
    df = pandas.read_csv(homedir+"DataFiles/voltagestudies_HG_ch"+str(ch)+".csv", names=cols,index_col=False,header=None,sep=',')
    df=df.sort_values(by="voltage",ascending = True)
    df = df.reset_index()
    n = df.shape[0]
    voltage = []
    gerr = [0]*n
    mpv = []
    mpverr = []
    stddev = []
    stddeverr = []

    #fill arrays with data from dataframe
    for i in range(n):
        scale_factor = 1
        sigma_sf = 1
        scale_factor = 1./df.loc[10,"mpv"]
        voltage.append(df.loc[i,"voltage"]-0.05)
        mpv.append(df.loc[i,"mpv"]*scale_factor)
        mpverr.append(df.loc[i,"mpverr"]*scale_factor)
        stddev.append(df.loc[i,"stddev"]*sigma_sf)
        stddeverr.append(df.loc[i,"stddeverr"]*sigma_sf)

    #new dataframe and file to save calibration
    '''df2 = pandas.DataFrame(data=np.transpose([voltage,mpv,mpverr,stddev,stddeverr]),columns=cols[1:])
    df2.to_csv(path_or_buf="/home/cmiller6/DataFiles/gainscan_scaled_ch"+str(ch)+".csv",header=False,index=False)'''
    res = np.array(stddev)/np.array(mpv) #resolution
    reserr = np.array(stddeverr)/np.array(mpv) #(rougly) error in resolution
    gainfactor = np.array(mpv)/np.array(mpv[0])
    gferr = np.array(mpverr)/np.array(mpv[0])

    df3 = pandas.DataFrame(data=np.transpose([voltage,gainfactor,gferr,res,reserr]))
    df3.to_csv(path_or_buf=homedir+"/DataFiles/gainfactors_ch"+str(ch)+".csv",header=False,index=False)

    c1.cd()
    gr = TGraphErrors(len(voltage), array('f',voltage), array('f',gainfactor),array('f',gerr), array('f',gferr))
    gr.SetTitle("Gain Factor vs. Voltage; V_{i}-V_{op} (V); Gain Factor (MPV_{V}/MPV)")
    gr.SetMarkerColor(ch)
    gr.SetMarkerStyle( 21 )
    gr.Draw("AP")
    leg1.AddEntry(gr,"SiPM "+sipmnames[ch])
    c1.Update()


    c2.cd()
    gr2 = TGraphErrors(len(voltage), array('f',voltage), array('f',res),array('f',gerr), array('f',reserr))
    gr2.SetTitle(r"Resolution vs. Voltage; V_{i}-V_{op} (V); Resolution ($sigma$/MPV)")
    gr2.SetMarkerColor(ch)
    gr2.SetMarkerStyle( 21 )
    gr2.Draw("AP")
    leg2.AddEntry(gr2,"SiPM "+sipmnames[ch])
    c2.Update()

c1.SaveAs("/home/cmiller6/Figures/voltagescan.pdf")
c1.SaveAs("/home/cmiller6/Figures/voltagescan.png")
print("saving file /home/cmiller6/Figures/voltagescan.pdf")

c2.SaveAs("/home/cmiller6/Figures/voltageres.pdf")
c2.SaveAs("/home/cmiller6/Figures/voltageres.png")
print("saving file /home/cmiller6/Figures/voltageres.pdf")
        
