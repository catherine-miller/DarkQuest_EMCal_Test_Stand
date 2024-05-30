from ROOT import TCanvas, TGraphErrors, TF1, Math, TLegend, TGraph
from ROOT import gROOT
from array import array
import pandas
import sys
import numpy as np
import scipy.optimize as fit

plotfilename = "1stop"
plottitle = "1-Stop N.D. Filter"
homedir = "/home/cmiller6/"
if len(sys.argv) > 1:
    label = str(sys.argv[1:])
else:
    label = "No Attenuator"

def sat_model(x,a,b):
    y = b*(1-np.exp(a*x))
    return y
def inv_sqrt(x,a,b):
    y = 1./np.sqrt(b*x)+a/x
    return y
def line(x,a):
    y = a*x
    return y
 
c1 = TCanvas( 'c1', 'LED Pulser Calibration', 200, 10, 700, 500 )
c1.cd() 
c1.SetGrid()
c1.GetFrame().SetFillColor( 21 )
c1.GetFrame().SetBorderSize( 12 )



#get data from inital calibration file
cols = ["LED voltage","mpv","mpverr","stddev","stddeverr"]
df = pandas.read_csv("/home/cmiller6/DataFiles/ledcalibration_scaled.csv", names=cols,header=None,sep=',')
df=df.sort_values(by="LED voltage",ascending = True)
df = df.reset_index()
#get data from SiPM saturation curve run
cols2 = ["run","LED voltage","lgmpv","lgmpverr","lgstddev","lgstddeverr","hgmpv","hgmpverr","hgstddev","hgstddeverr"]
df2 = pandas.read_csv(homedir+"/DataFiles/SiPMscan_"+plotfilename+".csv", names=cols2,index_col=False,header=None,sep=',')
#df2=df2.sort_values(by="LED voltage",ascending = True)
#df2 = df2.reset_index()
#initialize lists
n = df2.shape[0]
mpv = []
mpverr = []
relmpverr = []
E = [] #lowgain
Eerr = []
relerr = [] #error in mpv/mpv
sigma = []
relEres = []
relEerr = []
relmpv = []
nonlin = []
mpv_stderr = []
relmpverr = []

#fill lists with data from dataframe
j = 0 #index of point in initial calibration data
E_ADC = 0.731 #theoretically calculated energy deposition from run in detector
#in MeV/HGADC
#which corresponds to an MPV of 182.3
E_conv_factor = E_ADC*df2.loc[2,"hgmpv"]/df.loc[10,"mpv"]*10**(-3) #in GeV/HGADC
#assume a perfect 10 attenuation factor
#have to convert between SiPM scan adc and intensity (from df mpv)
print(df2.loc[2,"LED voltage"])
print(df.loc[10,"LED voltage"])
scale_factor = 1
for i in range(n):
    while float(df2.loc[i,"LED voltage"]) - float(df.loc[j,"LED voltage"]) > 0.01:
        j+=1
    while float(df2.loc[i,"LED voltage"]) - float(df.loc[j,"LED voltage"])
    if i > 0:
        if df2.loc[i,"LED voltage"] < df2.loc[i-1,"LED voltage"]:
            scale_factor = scale_factor*2053.3/82.18
            print('changed scale factor')
    relmpv.append(df.loc[j,"mpv"]*scale_factor)
    E.append(df.loc[j,"mpv"]*E_conv_factor)
    Eerr.append(df.loc[j,"mpverr"]*E_conv_factor) #standard error = sigma/sqrt(n)
    relerr.append(df2.loc[i,"lgstddev"]/df2.loc[i,"lgmpv"])
    sigma.append(df2.loc[i,"lgstddev"])
    mpv.append(df2.loc[i,"lgmpv"])
    mpv_stderr.append(df2.loc[i,"lgmpverr"])
    relEerr.append(Eerr[i]/E[i])
    relmpverr.append(mpv_stderr[i]/mpv[i])

#we have the ADC relative error stored in relerr, but we need to calculate the energy relative error
#yerr = xerr*dy/dx    or something. haha what do I know about error propagation
for i in range(n-1):
    dE_dA = (E[i+1]-E[i])/(mpv[i+1]-mpv[i]) #A for ADC
    relEres.append(sigma[i]*dE_dA/E[i])
    
relEres.append(sigma[-1]*dE_dA/E[-1]) #calculate derivative "backward" instead of forward for the last point

#calculate nonlinearity
popt1,pcov1 = fit.curve_fit(line, np.array(E)[8:10], np.array(mpv)[8:10], p0 = [300])
for i in range(n):
    adc_lin = popt1[0]*E[i]
    err = (adc_lin-mpv[i])/adc_lin
    nonlin.append(err)
'''
E2 = []
for e in E:
    if e < 120:
        E2.append(e)
E = E2'''
gr = TGraphErrors(len(E), array('f',E), array('f',np.sqrt(10)*np.array(mpv)),array('f',Eerr), array('f',mpv_stderr))
gr.SetTitle("Hamamatsu S14160-6010PS SiPM Saturation ("+plottitle+"); Estimated Energy in Detector (GeV); Low Gain ADC")
gr.SetMarkerColor(4)
gr.SetMarkerStyle( 21 )
gr.GetXaxis().SetRangeUser(0,80) #120
gr.GetYaxis().SetRangeUser(0,8000) #3500
gr.Draw("AP")
popt,pcov = fit.curve_fit(sat_model, E, mpv, p0 = [-.01,4000])
x = np.arange(0,120,0.5)
gr3 = TGraph(len(x),x,sat_model(x,*popt))
#gr3.GetXaxis().SetRangeUser(0,80)
#gr3.Draw("same")
leg = TLegend(0.6,0.15,0.85,0.35)
leg.AddEntry(gr,"Measured ADC")
leg.AddEntry(gr3,"Fit to Saturation Model a*(1-exp(b*x))")
#leg.Draw()
c1.Update()
c1.SaveAs(homedir+"Figures/S14160energy_"+plotfilename+".pdf")
c1.SaveAs(homedir+"Figures/S14160energy_"+plotfilename+".png")
print("Saturation Parameters: \n a (amplitude) = "+str(popt[1])+", b (exponential coefficient) = "+str(popt[0]))

#resolution plots
gr2 = {} #for hypothetical plots
c2 = TCanvas( 'c1', 'LED Pulser Calibration', 200, 10, 700, 500 )
c2.SetGrid()
c2.GetFrame().SetFillColor( 21 )
c2.GetFrame().SetBorderSize( 12 )
c2.cd()
legend = TLegend(0.6,0.65,0.85,0.85)
for i in range(1):
    gr2[i] = TGraphErrors(len(E), array('f',np.array(E)), array('f',relerr)) #,array('f',2**(i)*np.array(Eerr)), array('f',relEerr))
    gr2[i].SetMarkerColor(1+i)
    gr2[i].SetMarkerStyle( 21 )
    if i == 0:
        gr2[i].SetTitle("S14160-6010PS SiPM Resolution ("+plottitle+"); Estimated Energy in Detector (GeV); Relative Resolution (#sigma_{MPV}/MPV)")
        #gr3 = TGraphErrors(len(E), array('f',E), array('f',relEres),array('f',Eerr), array('f',relEerr))
        #popt,pcov = fit.curve_fit(inv_sqrt, np.array(E), np.array(relEres), p0 = [.08,1000])
        #x = np.arange(.05,25,0.05)
        #gr4 = TGraph(len(x),x,inv_sqrt(x,*popt))
        #print(popt)
    
        #legend.AddEntry(gr3,"Energy resolution,\n \sigma_{E}/E")
        #legend.AddEntry(gr4,"Fit to inverse square root model")
        gr2[i].GetXaxis().SetRangeUser(0,10)
        gr2[i].GetYaxis().SetRangeUser(0,0.1)
        gr2[i].Draw("AeP")
        legend.AddEntry(gr2[i],"S14160-6010PS","p")
    else:
        gr2[i].Draw("ePsame")
        legend.AddEntry(gr2[i],"S14160-3010PS","p")
#gr3.Draw("P")
#legend.Draw()
#gr4.Draw("same")
c2.Update()
c2.SaveAs(homedir+"Figures/resolutionS14160_"+plotfilename+".pdf")
c2.SaveAs(homedir+"Figures/resolutionS14160_"+plotfilename+".png")

#nonlinearity plot
gr5 = {}
c3 = TCanvas( 'c1', 'LED Pulser Calibration', 200, 10, 700, 500 )
c3.SetGrid()
c3.GetFrame().SetFillColor( 21 )
c3.GetFrame().SetBorderSize( 12 )
legend2 = TLegend(0.60,0.65,0.85,0.85)
c3.cd()
for j in range(1):
    i = 1-j
    gr5[i] = TGraphErrors(len(E), array('f',np.array(E)), array('f',nonlin),array('f',8*2**(-i)*np.array(Eerr)),array('f',relmpverr)) 
    gr5[i].SetMarkerStyle( 21 )
    gr5[i].SetMarkerColor(1+i)
    if i == 1:
        gr5[i].SetTitle("S14160-6010PS SiPM Nonlinearity ("+plottitle+"); Estimated Energy in Detector (GeV); Nonlinearity")
        gr5[i].GetXaxis().SetRangeUser(0,80)
        gr5[i].Draw("AeP")
        legend2.AddEntry(gr5[i],"S14160-6010PS","p")
    else:
        gr5[i].Draw("ePsame")
        legend2.AddEntry(gr5[i],"14160-3010PS","p")
#legend2.Draw()
c3.Update()
c3.SaveAs(homedir+"Figures/nonlinearityS14160_6010PS_"+plotfilename+".pdf")
c3.SaveAs(homedir+"Figures/nonlinearityS14160_6010PS_"+plotfilename+".png")

#print(Eerr)
#print(relmpverr)
