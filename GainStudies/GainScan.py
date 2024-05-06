from ROOT import TCanvas, TGraphErrors, TF1, Math, TLegend
from ROOT import gROOT
from array import array
import pandas
import sys
import numpy as np

#get data from file
cols = ["run","gain","mpv","mpverr","stddev","stddeverr"]
df = pandas.read_csv("/home/cmiller6/DataFiles/gainstudies_HG.csv", names=cols,index_col=False,header=None,sep=',')
df=df.sort_values(by="run",ascending = True)
df = df.reset_index()
n = df.shape[0]
gain = []
gerr = [0]*n
mpv = []
mpverr = []
stddev = []
stddeverr = []

#fill arrays with data from dataframe
for i in range(n):
    scale_factor = 1
    sigma_sf = 1
    if int(df.loc[i,"run"]) > 2564:
        scale_factor = (6118.5/1771.9)
        sigma_sf = (522.6/327)
        if int(df.loc[i,"run"]) > 2759:
            scale_factor = (6118.5/1771.9)*(4105/2285)
            sigma_sf = (522.6/327)*(794/519)
    gain.append(df.loc[i,"gain"])
    mpv.append(df.loc[i,"mpv"]*scale_factor)
    mpverr.append(df.loc[i,"mpverr"]*scale_factor)
    stddev.append(df.loc[i,"stddev"]*sigma_sf)
    stddeverr.append(df.loc[i,"stddeverr"]*sigma_sf)

legend = TLegend(0.7,0.65,0.85,0.85)
#new dataframe and file to save calibration
df2 = pandas.DataFrame(data=np.transpose([gain,mpv,mpverr,stddev,stddeverr]),columns=cols[1:])
df2.to_csv(path_or_buf="/home/cmiller6/DataFiles/gainscan_scaled.csv",header=False,index=False)
res = np.array(stddev)/np.array(mpv) #resolution
reserr = np.array(stddeverr)/np.array(mpv) #(rougly) error in resolution
gainfactor = np.array(mpv)/np.array(mpv[0])
gferr = np.array(mpverr)/np.array(mpv[0])

df3 = pandas.DataFrame(data=np.transpose([gain,gainfactor,gferr,res,reserr]))
df3.to_csv(path_or_buf="/home/cmiller6/DataFiles/gainfactors.csv",header=False,index=False)

c1 = TCanvas( 'c1', 'LED Pulser Calibration', 200, 10, 700, 500 )
c1.cd() 
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )
gr = TGraphErrors(len(gain), array('f',gain), array('f',gainfactor),array('f',gerr), array('f',gferr))
gr.SetTitle("Gain Setting Studies; Gain Setting; Gain Factor (MPV_{GS}/MPV)")
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
c1.SaveAs("/home/cmiller6/Figures/gainscan.pdf")
c1.SaveAs("/home/cmiller6/Figures/gainscan.png")
print("saving file /home/cmiller6/Figures/gainscan.pdf")

c2 = TCanvas( 'c2', 'Resolution v gain', 200, 10, 700, 500 )
c2.cd() 
c2.SetGrid()
c2.GetFrame().SetFillColor( 21 )
c2.GetFrame().SetBorderSize( 12 )
gr2 = TGraphErrors(len(gain), array('f',gain), array('f',res),array('f',gerr), array('f',reserr))
gr2.SetTitle(r"Resolution vs. Gain Setting; Gain Setting; Resolution ($sigma$/MPV)")
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
c2.SaveAs("/home/cmiller6/Figures/gainres.pdf")
c2.SaveAs("/home/cmiller6/Figures/gainres.png")
print("saving file /home/cmiller6/Figures/gainres.pdf")
        
