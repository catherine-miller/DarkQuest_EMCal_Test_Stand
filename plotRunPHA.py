########################################################################
# Title: plotRunPHA
# Description: Reads a Janus output file, located in a folder called
#    DataFiles. Makes an energy histogram for each channel, high gain
#    and low gain. Plots these energy histograms (with several variations).
#    Saves each channel's energy information in a ROOT histogram.
# Arguments: Run number
# Run with (e.g.): python3 plotRunPHA.py 2923 -l -q -b
########################################################################




import sys
sys.argv.append( '-b' )
from ROOT import *
from array import array

gROOT.SetBatch(True)

#arguments:

chlist = [0,1,2,3] #[0,1,2,3,4,5,6,7,8,9,10,11]
chlist_str = ["00","01","02","03","04","05","06","07","08","09","10","11"]
cols=[1,2,3,4,5,6,7,8,9,46,38,30]

ch_lg = {}
ch_hg = {}

for ch in chlist:
  ch_lg[ch] = []
  ch_hg[ch] = []

nevents=0
homedir = "/home/cmiller6/"
with open(homedir+"DataFiles/Run"+str(sys.argv[1])+"_list.txt") as infile:

  for line in infile:
    if ("//" in line): continue
    if ("Tstamp" in line): continue
    for ch in chlist:
      if ("00  "+chlist_str[ch] in line):
        if (ch==0):
          nevents+=1
          ch_lg[ch].append(float(line.split()[4]))
          ch_hg[ch].append(float(line.split()[5]))
        else:
          ch_lg[ch].append(float(line.split()[2]))
          ch_hg[ch].append(float(line.split()[3]))

lg_max=[]
hg_max=[]

lg_sum=[]
hg_sum=[]

#for i in range(len(ch0_lg)): 
##  print [ch0_lg[i],ch1_lg[i],ch2_lg[i],ch3_lg[i]]
##  print max([ch0_lg[i],ch1_lg[i],ch2_lg[i],ch3_lg[i]])
#  lg_max.append(max([ch0_lg[i],ch1_lg[i],ch2_lg[i],ch3_lg[i]]))
#  hg_max.append(max([ch0_hg[i],ch1_hg[i],ch2_hg[i],ch3_hg[i]]))
#
#  lg_sum.append(sum([ch0_lg[i],ch1_lg[i],ch2_lg[i],ch3_lg[i]]))
#  hg_sum.append(sum([ch0_hg[i],ch1_hg[i],ch2_hg[i],ch3_hg[i]]))

nbin=800; low=0; high=8000;
hgmax=1000;
h_hg = {}
for ch in chlist:
  h_hg[ch] = TH1F("h_hgch"+chlist_str[ch],"h_hgch"+chlist_str[ch],nbin,low,high)

lgmax = 8000
nbin=1600; low=0; high=8192;
h_lg = {}
for ch in chlist:
  h_lg[ch] = TH1F("h_lgch"+chlist_str[ch],"h_lgch"+chlist_str[ch],nbin,low,high)

#h_lgmax = TH1F("h_lgmax","h_lgmax",nbin,low,high)
#h_hgmax = TH1F("h_hgmax","h_hgmax",nbin,low,high)
#h_lgsum = TH1F("h_lgsum","h_lgsum",nbin,low,high*2)
#h_hgsum = TH1F("h_hgsum","h_hgsum",nbin,low,high*2)

h_lgch0vsch1 = TH2F("h_lgch0vsch1","h_lgch0vsch1",256,0,2048,256,0,2048)
h_lgch0vsch2 = TH2F("h_lgch0vsch2","h_lgch0vsch2",256,0,1024,256,0,1024)
h_lgch0vsch3 = TH2F("h_lgch0vsch3","h_lgch0vsch3",256,0,1024,256,0,1024)
h_lgch1vsch3 = TH2F("h_lgch1vsch3","h_lgch1vsch3",256,0,1024,256,0,1024)
h_lgch2vsch3 = TH2F("h_lgch2vsch3","h_lgch2vsch3",256,0,1024,256,0,1024)

#nbin=500; low=200; high=2500;
#h_lgch0_max = TH1F("h_lgch0_max","h_lgch0_max",nbin,low,high)
#h_lgch1_max = TH1F("h_lgch1_max","h_lgch1_max",nbin,low,high)
#h_lgch2_max = TH1F("h_lgch2_max","h_lgch2_max",nbin,low,high)
#h_lgch3_max = TH1F("h_lgch3_max","h_lgch3_max",nbin,low,high)

for i in range(len(ch_lg[0])):
#  h_lgmax.Fill(float(lg_max[i]))
#  h_lgsum.Fill(float(lg_sum[i]))

#  h_hgmax.Fill(float(hg_max[i]))
#  h_hgsum.Fill(float(hg_sum[i]))

  for ch in chlist:
    h_lg[ch].Fill(float(ch_lg[ch][i]))
    h_hg[ch].Fill(float(ch_hg[ch][i]))

  #if (float(ch0_lg[i])==float(lg_max[i])): h_lgch0_max.Fill(float(ch0_lg[i]))
  #if (float(ch1_lg[i])==float(lg_max[i])): h_lgch1_max.Fill(float(ch1_lg[i]))
  #if (float(ch2_lg[i])==float(lg_max[i])): h_lgch2_max.Fill(float(ch2_lg[i]))
  #if (float(ch3_lg[i])==float(lg_max[i])): h_lgch3_max.Fill(float(ch3_lg[i]))

  #h_lgch0vsch1.Fill(float(ch0_lg[i]),float(ch1_lg[i]))  
  #if (lg_max[i]==ch2_lg[i]):
  #  h_lgch0vsch2.Fill(float(ch2_lg[i]),float(ch0_lg[i]))
  #  h_lgch2vsch3.Fill(float(ch2_lg[i]),float(ch3_lg[i]))
  #h_lgch0vsch3.Fill(float(ch0_lg[i]),float(ch3_lg[i]))
  #h_lgch1vsch3.Fill(float(ch1_lg[i]),float(ch3_lg[i]))


#gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

#c1 = TCanvas("c1","c1",800,600)
#c1.cd()
#c1.SetLogy()
#h_lgmax.SetLineColor(4)
#h_lgmax.SetMarkerColor(4)
#h_lgmax.SetMarkerSize(1.2)
#h_lgmax.GetXaxis().SetTitle("ADC Value (Low Gain)")
#h_lgmax.GetYaxis().SetTitle("Counts")
#h_lgmax.Draw("ehist")
#h_lgmax.SaveAs("h_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_LG.root")
#legend = TLegend(0.60,0.7,0.8,0.8)
#legend.AddEntry(h_lgmax,"Maximum Channel","ep")
#legend.Draw("same")
#c1.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_LG.pdf")
#c1.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_LG.png")

#c2 = TCanvas("c2","c2",800,600)
#c2.cd()
#c2.SetLogy()
#h_lgsum.SetLineColor(4)
#h_lgsum.SetMarkerColor(4)
#h_lgsum.SetMarkerSize(1.2)
#h_lgsum.GetXaxis().SetTitle("ADC Value (Low Gain)")
#h_lgsum.GetYaxis().SetTitle("Counts")
#h_lgsum.Draw("ehist")
#legend = TLegend(0.60,0.7,0.8,0.8)
#legend.AddEntry(h_lgsum,"4-Channel Sum","ep")
#legend.Draw("same")
#c2.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chSum_LG.pdf")
#c2.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chSum_LG.png")

#c3 = TCanvas("c3","c3",800,600)
#c3.cd()
#c3.SetLogy()
#h_hgmax.SetLineColor(4)
#h_hgmax.SetMarkerColor(4)
#h_hgmax.SetMarkerSize(1.2)
#h_hgmax.GetXaxis().SetTitle("ADC Value (Low Gain)")
#h_hgmax.GetYaxis().SetTitle("Counts")
#h_hgmax.Draw("ehist")
#h_hgmax.SaveAs("h_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_HG.root")
#legend = TLegend(0.60,0.7,0.8,0.8)
#legend.AddEntry(h_hgmax,"Maximum Channel","ep")
#legend.Draw("same")
#c3.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_HG.pdf")
#c3.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_4chMax_HG.png")

#maximums = [h_lgch0.GetMaximum(),h_lgch1.GetMaximum(),h_lgch2.GetMaximum(),h_lgch3.GetMaximum()]

c4 = TCanvas("c4","c4",800,600)
c4.cd()
#c4.SetLogy()
for ch in chlist:
  h_lg[ch].SetLineColor(cols[ch])
  h_lg[ch].SetMarkerColor(cols[ch])
  h_lg[ch].SetMarkerSize(0.5)
  h_lg[ch].SetMarkerStyle(20)
  if (ch==0):
    h_lg[ch].GetXaxis().SetTitle("ADC Value (Low Gain)")
    h_lg[ch].SetTitle("DarkQuest EMCal Test Stand")
    h_lg[ch].GetXaxis().SetRangeUser(0,lgmax)
    h_lg[ch].GetYaxis().SetTitle("Counts")
    #h_lg[ch].SetMaximum(1.5*max(maximums))
    h_lg[ch].SetMaximum(nevents)
    h_lg[ch].Draw("ehist")
  else:
    h_lg[ch].Draw("ehistsame")
  h_lg[ch].SaveAs(homedir+"DataFiles/h_lgch"+chlist_str[ch]+"_Run"+str(sys.argv[1]).replace(".txt","")+".root")

legend = TLegend(0.55,0.55,0.8,0.8)
for ch in chlist:
  legend.AddEntry(h_lg[ch],"Ch. "+chlist_str[ch]+" (Run "+str(sys.argv[1])+")","ep")
legend.Draw("same")
c4.SaveAs(homedir+"Figures/plot_Run"+str(sys.argv[1])+"_EachCh_LG.pdf")
c4.SaveAs(homedir+"Figures/plot_Run"+str(sys.argv[1])+"_EachCh_LG.png")

c5 = TCanvas("c5","c5",800,600)
c5.cd()
#c5.SetLogy()
for ch in chlist:
  h_hg[ch].SetLineColor(cols[ch])
  h_hg[ch].SetMarkerColor(cols[ch])
  h_hg[ch].SetMarkerSize(0.5)
  h_hg[ch].SetMarkerStyle(20)
  if (ch==0):
    h_hg[ch].GetXaxis().SetTitle("ADC Value (High Gain)")
    h_hg[ch].SetTitle("DarkQuest EMCal Test Stand")
    h_hg[ch].GetXaxis().SetRangeUser(0,hgmax)
    h_hg[ch].GetYaxis().SetTitle("Counts")
    #h_hg[ch].SetMaximum(1.5*max(maximums))
    #h_hg[ch].SetMaximum(0.5*nevents)
    h_hg[ch].Draw("hist")
  else:
    h_hg[ch].Draw("histsame")
  h_hg[ch].SaveAs(homedir+"DataFiles/h_hgch"+chlist_str[ch]+"_Run"+str(sys.argv[1]).replace(".txt","")+".root")

legend = TLegend(0.55,0.55,0.8,0.8)
for ch in chlist:
  legend.AddEntry(h_hg[ch],"Ch. "+chlist_str[ch]+" (Run "+str(sys.argv[1])+")","ep")
legend.Draw("same")
c5.SaveAs(homedir+"Figures/plot_Run"+str(sys.argv[1])+"_EachCh_HG.pdf")
c5.SaveAs(homedir+"Figures/plot_Run"+str(sys.argv[1])+"_EachCh_HG.png")


#c5 = TCanvas("c5","c5",800,600)
#c5.cd()
##c5.SetLogx()
##c5.SetLogy()
#h_lgch0vsch2.GetXaxis().SetTitle("ADC Value (Low Gain) Ch. 2")
#h_lgch0vsch2.GetYaxis().SetTitle("ADC Value (Low Gain) Ch. 0")
#h_lgch0vsch2.GetZaxis().SetTitle("Counts")
#h_lgch0vsch2.Draw("colz")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh2.pdf")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh2.png")

#c5 = TCanvas("c5","c5",800,600)
#c5.cd()
##c5.SetLogx()
##c5.SetLogy()
#h_lgch1vsch3.GetXaxis().SetTitle("ADC Value (Low Gain) Ch. 1")
#h_lgch1vsch3.GetYaxis().SetTitle("ADC Value (Low Gain) Ch. 3")
#h_lgch1vsch3.GetZaxis().SetTitle("Counts")
#h_lgch1vsch3.Draw("colz")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch1vsCh3.pdf")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch1vsCh3.png")

#c5 = TCanvas("c5","c5",800,600)
#c5.cd()
##c5.SetLogx()
##c5.SetLogy()
#h_lgch0vsch1.GetXaxis().SetTitle("ADC Value (Low Gain) Ch. 0")
#h_lgch0vsch1.GetYaxis().SetTitle("ADC Value (Low Gain) Ch. 1")
#h_lgch0vsch1.GetZaxis().SetTitle("Counts")
#h_lgch0vsch1.Draw("colz")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh1.pdf")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh1.png")

#c5 = TCanvas("c5","c5",800,600)
#c5.cd()
##c5.SetLogx()
##c5.SetLogy()
#h_lgch2vsch3.GetXaxis().SetTitle("ADC Value (Low Gain) Ch. 2")
#h_lgch2vsch3.GetYaxis().SetTitle("ADC Value (Low Gain) Ch. 3")
#h_lgch2vsch3.GetZaxis().SetTitle("Counts")
#h_lgch2vsch3.Draw("colz")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch2vsCh3.pdf")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch2vsCh3.png")

#c5 = TCanvas("c5","c5",800,600)
#c5.cd()
##c5.SetLogx()
##c5.SetLogy()
#h_lgch0vsch3.GetXaxis().SetTitle("ADC Value (Low Gain) Ch. 0")
#h_lgch0vsch3.GetYaxis().SetTitle("ADC Value (Low Gain) Ch. 3")
#h_lgch0vsch3.GetZaxis().SetTitle("Counts")
#h_lgch0vsch3.Draw("colz")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh3.pdf")
#c5.SaveAs("plot_"+str(sys.argv[1]).replace(".txt","")+"_Ch0vsCh3.png")

#h_lgch1_max.Scale(h_lgch0_max.Integral()/h_lgch1_max.Integral())
#h_lgch2_max.Scale(h_lgch0_max.Integral()/h_lgch2_max.Integral())
#h_lgch3_max.Scale(h_lgch0_max.Integral()/h_lgch3_max.Integral())

'''
maximums = [h_lgch0_max.GetMaximum(),h_lgch1_max.GetMaximum(),h_lgch2_max.GetMaximum(),h_lgch3_max.GetMaximum()]
c6 = TCanvas("c6","c6",800,600)
c6.cd()
#c6.SetLogy()
h_lgch0_max.SetLineColor(1)
h_lgch0_max.SetMarkerColor(1)
h_lgch0_max.SetMarkerSize(0.5)
h_lgch0_max.SetMarkerStyle(20)
h_lgch0_max.GetXaxis().SetTitle("ADC Value (Low Gain)")
h_lgch0_max.GetYaxis().SetTitle("Counts")
h_lgch0_max.SetMaximum(1.5*max(maximums))
f_lgch0_max = TF1("f_lgch0_max","landau",300,600)
h_lgch0_max.Fit("f_lgch0_max","RN")
f_lgch0_max.SetLineColor(1)
h_lgch0_max.Draw("ehist")
f_lgch0_max.Draw("lsame")

h_lgch1_max.SetLineColor(2)
h_lgch1_max.SetMarkerColor(2)
h_lgch1_max.SetMarkerSize(0.5)
h_lgch1_max.SetMarkerStyle(20)
f_lgch1_max = TF1("f_lgch1_max","landau",300,600)
h_lgch1_max.Fit("f_lgch1_max","RN")
f_lgch1_max.SetLineColor(2)
h_lgch1_max.Draw("ehistsame")
f_lgch1_max.Draw("lsame")


h_lgch2_max.SetLineColor(4)
h_lgch2_max.SetMarkerColor(4)
h_lgch2_max.SetMarkerSize(0.5)
h_lgch2_max.SetMarkerStyle(20)
f_lgch2_max = TF1("f_lgch2_max","landau",300,600)
h_lgch2_max.Fit("f_lgch2_max","RN")
f_lgch2_max.SetLineColor(4)
h_lgch2_max.Draw("ehistsame")
f_lgch2_max.Draw("lsame")

h_lgch3_max.SetLineColor(6)
h_lgch3_max.SetMarkerColor(6)
h_lgch3_max.SetMarkerSize(0.5)
h_lgch3_max.SetMarkerStyle(20)
f_lgch3_max = TF1("f_lgch3_max","landau",300,600)
h_lgch3_max.Fit("f_lgch3_max","RN")
f_lgch3_max.SetLineColor(6)
h_lgch3_max.Draw("ehistsame")
f_lgch3_max.Draw("lsame")

legend = TLegend(0.55,0.55,0.8,0.8)
legend.AddEntry(h_lgch0_max,"Ch. 0 (Run "+str(sys.argv[1])+")","ep")
legend.AddEntry(h_lgch1_max,"Ch. 1 (Run "+str(sys.argv[1])+")","ep")
legend.AddEntry(h_lgch2_max,"Ch. 2 (Run "+str(sys.argv[1])+")","ep")
legend.AddEntry(h_lgch3_max,"Ch. 3 (Run "+str(sys.argv[1])+")","ep")
h_lgch0_max.SaveAs("h_lgch0_max_Run"+str(sys.argv[1])+".root")
h_lgch1_max.SaveAs("h_lgch1_max_Run"+str(sys.argv[1])+".root")
h_lgch2_max.SaveAs("h_lgch2_max_Run"+str(sys.argv[1])+".root")
h_lgch3_max.SaveAs("h_lgch3_max_Run"+str(sys.argv[1])+".root")
legend.Draw("same")
c6.SaveAs("plot_Run"+str(sys.argv[1])+"_EachCh_Max.pdf")
c6.SaveAs("plot_Run"+str(sys.argv[1])+"_EachCh_Max.png")

#save last time in a file
#if sys.argv[2] == "-tv":
  #f = open("timevsvoltage.txt",
'''


print("nevents",nevents)
