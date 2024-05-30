from ROOT import TCanvas, TGraphErrors, TF1, Math, TLegend
from ROOT import gROOT
from array import array
import pandas
import sys
import numpy as np

#get data from file
cols = ["run","LED voltage","lgmpv","lgmpverr","lgstddev","lgstddeverr","hgmpv","hgmpverr","hgstddev","hgstddeverr"]
df = pandas.read_csv("/home/cmiller6/DataFiles/LEDvoltagescan.csv", names=cols,index_col=False,header=None,sep=',')
df=df.sort_values(by="run",ascending = True)
df = df.reset_index()
n = df.shape[0]
voltage = []
verr = [0]*n
mpv = []
mpverr = []
stddev = []
stddeverr = []

#fill arrays with data from dataframe
#use high gain
scale_factor = 1
sigma_sf = 1
for i in range(n):
    if i > 0:
        if (float(df.loc[i,"LED voltage"]) - float(df.loc[i-1,"LED voltage"]) < 0.001):
            #if we repeat a voltage, means that there was a rescaling
            # don't write down the duplicated mpv
            #but do change the scale factor
            scale_factor = scale_factor*float(df.loc[i-1,"hgmpv"])/float(df.loc[i,"hgmpv"])
            sigma_sf = sigma_sf*float(df.loc[i-1,"hgstddev"])/float(df.loc[i,"hgstddev"])
        else:
            #print("adding to mpv array")
            voltage.append(df.loc[i,"LED voltage"])
            mpv.append(df.loc[i,"hgmpv"]*scale_factor)
            mpverr.append(df.loc[i,"hgmpverr"]*scale_factor)
            stddev.append(df.loc[i,"hgstddev"]*sigma_sf)
            stddeverr.append(df.loc[i,"hgstddeverr"]*sigma_sf)
    else:
        voltage.append(df.loc[i,"LED voltage"])
        mpv.append(df.loc[i,"hgmpv"]*scale_factor)
        mpverr.append(df.loc[i,"hgmpverr"]*scale_factor)
        stddev.append(df.loc[i,"hgstddev"]*sigma_sf)
        stddeverr.append(df.loc[i,"hgstddeverr"]*sigma_sf)

legend = TLegend(0.7,0.65,0.85,0.85)
#new dataframe and file to save calibration
df2 = pandas.DataFrame(data=np.transpose([voltage,mpv,mpverr,stddev,stddeverr]),columns=["LED voltage","mpv","mpverr","stddev","stddeverr"])
df2.to_csv(path_or_buf="/home/cmiller6/DataFiles/ledcalibration_scaled.csv",header=False,index=False)
res = np.array(stddev)/np.array(mpv) #resolution
reserr = np.array(stddeverr)/np.array(mpv) #(rougly) error in resolution
gainfactor = np.array(mpv)/mpv[0]
gferr = np.array(mpverr)/mpv[0]

'''
df3 = pandas.DataFrame(data=np.transpose([gain,gainfactor,gferr,res,reserr]))
df3.to_csv(path_or_buf="/home/cmiller6/DataFiles/gainfactors.csv",header=False,index=False)
'''
c1 = TCanvas( 'c1', 'LED Pulser Calibration', 200, 10, 700, 500 )
c1.cd() 
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
gr = TGraphErrors(len(voltage), array('f',voltage), array('f',mpv),array('f',verr), array('f',mpverr))
gr.SetTitle("LED Pulser Calibration; Driving Voltage; ADC (Arbitrary Units)")
gr.SetMarkerColor(4)
gr.SetMarkerStyle( 21 )
#c1.SetLogy()
#gr.GetXaxis().SetLimits(42.1,42.4) 
#gr[ch].GetXaxis().SetLimits(40.0,40.5)
#gr[ch].GetYaxis().SetRangeUser(390,410)
#gr.Draw( 'ALP' )
#fitting
#f[ch].SetParameters(2,0.1,25)
#f[ch].SetLineColor(ch+2)
#Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")
#result[ch] = gr[ch].Fit("parab"+str(ch),"SQR")
#legend.AddEntry(f[ch],"Ch. "+str(ch),"l")
#result[ch].Print()
gr.Draw("AP")
#f[ch].Draw("same")

c1.Update()
c1.SaveAs("/home/cmiller6/Figures/ledcalibration_HG.pdf")
c1.SaveAs("/home/cmiller6/Figures/ledcalibration_HG.png")
print("saving file /home/cmiller6/Figures/ledcalibration_HG.pdf")

c2 = TCanvas( 'c2', 'Resolution v gain', 200, 10, 700, 500 )
c2.cd() 
c2.SetGrid()
c2.GetFrame().SetFillColor( 21 )
c2.GetFrame().SetBorderSize( 12 )
gr2 = TGraphErrors(len(voltage), array('f',voltage), array('f',res),array('f',verr), array('f',reserr))
gr2.SetTitle(r"Resolution vs. LED Driving Voltage; LED Driving Voltage; Resolution ($sigma$/MPV)")
gr2.SetMarkerColor(4)
gr2.SetMarkerStyle( 21 )
#c2.SetLogy()
#gr.GetXaxis().SetLimits(42.1,42.4) 
#gr[ch].GetXaxis().SetLimits(40.0,40.5)
#gr[ch].GetYaxis().SetRangeUser(390,410)
#gr.Draw( 'ALP' )
#fitting
#f[ch].SetParameters(2,0.1,25)
#f[ch].SetLineColor(ch+2)
#Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")
#result[ch] = gr[ch].Fit("parab"+str(ch),"SQR")
#legend.AddEntry(f[ch],"Ch. "+str(ch),"l")
#result[ch].Print()
gr2.Draw("AP")
#f[ch].Draw("same")

c2.Update()
c2.SaveAs("/home/cmiller6/Figures/voltageres.pdf")
c2.SaveAs("/home/cmiller6/Figures/voltageres.png")
print("saving file /home/cmiller6/Figures/voltageres.pdf")
        
