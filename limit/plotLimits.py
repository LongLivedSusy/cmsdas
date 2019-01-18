import ROOT
#from ROOT import TGraph,TColor
from ROOT import *
from array import array
import CMS_lumi
from operator import itemgetter
ROOT.gROOT.SetBatch()
hexcolor=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
intcolor=[TColor.GetColor(i) for i in hexcolor]

x_13,y_th_13,y_13_obs,y_th = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )
x_13.append(1.000)
x_13.append(1.250)
x_13.append(1.500)
x_13.append(2.000)
x_13.append(2.500)
x_13.append(3.000)
x_13.append(3.500)
x_13.append(4.000)
x_13.append(4.500)
x_13.append(5.000)
#x_th_13.append(6.000)

y_th_13.append(1.3*20.05)
y_th_13.append(1.3*7.92)
y_th_13.append(1.3*3.519)
y_th_13.append(1.3*0.9528)
y_th_13.append(1.3*0.3136)
y_th_13.append(1.3*0.1289)
y_th_13.append(1.3*0.05452)
y_th_13.append(1.3*0.02807)
y_th_13.append(1.3*0.01603)
y_th_13.append(1.3*0.009095)
#y_th_13.append(0.00960796535494)

y_13_obs.append(0.76)
y_13_obs.append(0.82)
y_13_obs.append(0.28)
y_13_obs.append(0.091)
y_13_obs.append(0.044)
y_13_obs.append(0.021)
y_13_obs.append(0.018)
y_13_obs.append(0.021)
y_13_obs.append(0.019)
y_13_obs.append(0.024)

#y_th.append(1.3*1.153)
#y_th.append(1.3*1.556*0.1)
#y_th.append(1.3*3.585*0.01)
#y_th.append(1.3*1.174*0.01)
#y_th.append(1.3*4.939*0.001)
#

#xsecInPb = 0.00276133
xsecInPb = 1.00
y_th.append(xsecInPb)
y_th.append(xsecInPb)
y_th.append(xsecInPb)
y_th.append(xsecInPb)

masses=[10,30,100,1000]
nbins = len(masses)
x=array('d',[10.0,30.0,100.00,1000.000])
theory = TGraph( nbins, x, y_th )
theory.SetLineWidth(3)
theory.SetLineColor(ROOT.kAzure)
theory.SetMarkerColor(ROOT.kAzure)

theory_13 = TGraph( 10, x_13, y_th_13 )
theory_13.SetLineWidth(3)
theory_13.SetLineColor(ROOT.kRed)
theory_13.SetMarkerColor(ROOT.kRed)

obs_13 = TGraph( 10, x_13, y_13_obs )
obs_13.SetLineWidth(3)
obs_13.SetLineColor(ROOT.kRed)
obs_13.SetMarkerColor(ROOT.kRed)

limits=[]
sig3=[]
sig5=[]

def rounding(numero):
	return '%s' % float('%.2g' % float(numero))

for lumi in ['35.9']:
#for lumi in ['300','1000','3000','36']:
#for lumi in ['36','new_36','double_36']:
	c=ROOT.TCanvas('unodlimit_'+lumi,'',1200,1000)
	c.SetLogy()
	margine=0.15
	c.SetRightMargin(0.10)
	c.SetLeftMargin(margine)
	c.SetTopMargin(0.10)
	c.SetBottomMargin(margine)
	theta_exp_result = open('limits_info.txt','r')
	theta_exp_lines=theta_exp_result.readlines()
	lines_exp=[filter(None, i.split(' ')) for i in theta_exp_lines[1:] ]
	y_exp=array('d',[float(lines_exp[i][1]) for i in range(len(lines_exp))])
	y_err2down=array('d',[float(lines_exp[i][1])-float(lines_exp[i][2]) for i in range(len(lines_exp))])
	y_err1down=array('d',[float(lines_exp[i][1])-float(lines_exp[i][4]) for i in range(len(lines_exp))])
	y_err1up=array('d',[float(lines_exp[i][5])-float(lines_exp[i][1]) for i in range(len(lines_exp))])
	y_err2up=array('d',[float(lines_exp[i][3])-float(lines_exp[i][1]) for i in range(len(lines_exp))])
	zeros=array('d',[0]*len(lines_exp))
	print lumi 
	for i in range(len(lines_exp)):
		print masses[i],'&',rounding(lines_exp[i][2]),'&',rounding(lines_exp[i][4]),'&',rounding(lines_exp[i][1]),'&',rounding(lines_exp[i][5]),'&',rounding(lines_exp[i][3]),'\\\\'

	exp1sigma=ROOT.TGraphAsymmErrors(nbins,x,y_exp,zeros,zeros,y_err1down,y_err1up)
	exp2sigma=ROOT.TGraphAsymmErrors(nbins,x,y_exp,zeros,zeros,y_err2down,y_err2up)
	explim=TGraph(nbins,x,y_exp)
	explim.SetLineWidth(2)
	explim.SetLineStyle(2)
	explim.SetTitle('')
	limits.append(explim.Clone())
	exp2sigma.SetTitle('')
	exp1sigma.SetTitle('')
	exp1sigma.SetFillColor(ROOT.kGreen+1)
	exp2sigma.SetFillColor(ROOT.kOrange)
	exp2sigma.SetMaximum(10000)
	
	for i, limit in enumerate(masses):
		exp1sigma.GetXaxis().SetBinLabel(i+1, str(masses[i]))
	
	exp2sigma.SetMinimum(0.0007)
	exp2sigma.Draw('a3lp')

	exp2sigma.GetXaxis().SetTitle("Track Proper Decay Lengths (cm)")
	exp2sigma.GetXaxis().SetRangeUser(10,1000)
	
	exp2sigma.GetYaxis().SetTitleOffset(1)
	exp2sigma.GetYaxis().SetTitle(r"#sigma/#sigma_{SUSY}")

	sizefactor=1.5
	exp2sigma.GetXaxis().SetTitleSize(sizefactor*exp2sigma.GetXaxis().GetTitleSize())
	exp2sigma.GetYaxis().SetTitleSize(sizefactor*exp2sigma.GetYaxis().GetTitleSize())
	exp2sigma.GetXaxis().SetLabelSize(sizefactor*exp2sigma.GetXaxis().GetLabelSize())
	exp2sigma.GetYaxis().SetLabelSize(sizefactor*exp2sigma.GetYaxis().GetLabelSize())
	#exp2sigma.GetYaxis().SetMoreLogLabels(1)
	offset=1.2
	exp2sigma.GetXaxis().SetTitleOffset(offset*exp2sigma.GetXaxis().GetTitleOffset())
	exp2sigma.GetYaxis().SetTitleOffset(offset*exp2sigma.GetYaxis().GetTitleOffset())

	exp1sigma.Draw('3 same')
	explim.Draw('lp')
	theory.Draw('l')

	legend=ROOT.TLegend(0.335,0.55,0.9,0.9)
 	legend.SetTextSize(0.030)
  	legend.SetBorderSize(0)
  	legend.SetTextFont(42)
  	legend.SetLineColor(1)
  	legend.SetLineStyle(1)
  	legend.SetLineWidth(1)
  	legend.SetFillColor(0)
  	legend.SetFillStyle(0)
  	#legend.SetHeader('g_{KK}#rightarrow t#bar{t}')
  	legend.AddEntry(explim,'Expected','l')
  	legend.AddEntry(exp1sigma,'#pm 1 std. deviation','f')
  	legend.AddEntry(exp2sigma,'#pm 2 std. deviation','f')
  	legend.AddEntry(theory,"#tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}_{1}^{#pm}, #tilde{#chi}_{1}^{#pm}#rightarrow #tilde{#chi}_{1}^{0}, W^{*}",'l')
  	legend.Draw()
  	if '3000' in lumi:
		CMS_lumi.CMS_lumi(c, 3, 11)
	elif '1000' in lumi:
		CMS_lumi.CMS_lumi(c, 2, 11)
	elif '300' in lumi:
		CMS_lumi.CMS_lumi(c, 1, 11)
	elif '36' in lumi:
		CMS_lumi.CMS_lumi(c, 0, 11)
	c.SaveAs('unodlimit_'+lumi+'.pdf')

#	c2=ROOT.TCanvas('sigma_'+lumi,'',1200,1000)
#	c2.SetLogy()
#	c2.SetRightMargin(0.10)
#	c2.SetLeftMargin(margine)
#	c2.SetTopMargin(0.10)
#	c2.SetBottomMargin(margine)
#	sigma3_file = open('plots/theta_'+lumi+'_3sigmaSignif.txt','r')
#	sigma5_file = open('plots/theta_'+lumi+'_5sigmaSignif.txt','r')
#	sigma3_lines=sigma3_file.readlines()
#	sigma5_lines=sigma5_file.readlines()
#	sigma3_list=[[float(j) for j in filter(None, i.split(' '))] for i in sigma3_lines[1:] ]
#	sigma5_list=[[float(j) for j in filter(None, i.split(' '))] for i in sigma5_lines[1:] ]
#	sigma3_list=sorted(sigma3_list, key=itemgetter(0))
#	sigma5_list=sorted(sigma5_list, key=itemgetter(0))
#	y_sigma3=array('d',[sigma3_list[i][1] for i in range(len(sigma3_list))])
#	y_sigma5=array('d',[sigma5_list[i][1] for i in range(len(sigma5_list))])
#	sigma3=TGraph(5,x,y_sigma3)
#	sigma5=TGraph(5,x,y_sigma5)
#	for i in range(len(sigma3_list)):
#		print masses[i],'&',rounding(sigma3_list[i][1]),'&',rounding(sigma5_list[i][1]),'\\\\'
#
#	sigma3.SetLineWidth(3)
#	#sigma3.SetLineStyle(2)
#	sigma3.SetTitle('')
#	sigma3.SetLineColor(ROOT.kGreen+1)
#	sigma5.SetLineWidth(3)
#	#sigma5.SetLineStyle(2)
#	sigma5.SetTitle('')
#	sigma5.SetLineColor(ROOT.kRed+1)
#	sigma3.SetMaximum(10000)
#	sigma3.SetMinimum(0.0007)
#	sig3.append(sigma3.Clone())
#	sig5.append(sigma5.Clone())
#	sigma3.Draw('al')
#	sigma3.GetXaxis().SetTitle("g_{KK} mass [TeV]")
#	sigma3.GetXaxis().SetRangeUser(1500,6500)
#	sigma3.GetYaxis().SetTitle("Cross section [pb]")
#
#	sigma3.GetXaxis().SetTitleSize(sizefactor*sigma3.GetXaxis().GetTitleSize())
#	sigma3.GetYaxis().SetTitleSize(sizefactor*sigma3.GetYaxis().GetTitleSize())
#	sigma3.GetXaxis().SetLabelSize(sizefactor*sigma3.GetXaxis().GetLabelSize())
#	sigma3.GetYaxis().SetLabelSize(sizefactor*sigma3.GetYaxis().GetLabelSize())
#	sigma3.GetXaxis().SetTitleOffset(offset*sigma3.GetXaxis().GetTitleOffset())
#	sigma3.GetYaxis().SetTitleOffset(offset*sigma3.GetYaxis().GetTitleOffset())
#
#	sigma5.Draw('l')
#	theory.Draw('l')
#
#	legend2=ROOT.TLegend(0.335,0.55,0.9,0.9)
# 	legend2.SetTextSize(0.030)
#  	legend2.SetBorderSize(0)
#  	legend2.SetTextFont(42)
#  	legend2.SetLineColor(1)
#  	legend2.SetLineStyle(1)
#  	legend2.SetLineWidth(1)
#  	legend2.SetFillColor(0)
#  	legend2.SetFillStyle(0)
#  	legend2.SetHeader('g_{KK}#rightarrow t#bar{t}')
#  	legend2.AddEntry(sigma3,'3#sigma significance','l')
#  	legend2.AddEntry(sigma5,'5#sigma significance','l')
#  	legend2.AddEntry(theory,"g_{KK}#rightarrow t#bar{t}",'l')
#  	legend2.Draw()
#  	if '3000' in lumi:
#		CMS_lumi.CMS_lumi(c2, 3, 11)
#	elif '1000' in lumi:
#		CMS_lumi.CMS_lumi(c2, 2, 11)
#	elif '300' in lumi:
#		CMS_lumi.CMS_lumi(c2, 1, 11)
#	elif '36' in lumi:
#		CMS_lumi.CMS_lumi(c2, 0, 11)
#	c2.SaveAs('pdf/sigma_'+lumi+'.pdf')
#
#y_comp = ["Upper cross section limit [pb]",'3#sigma significance','5#sigma significance']
#legends_comp = ["300 fb^{-1} (14 TeV)","1000 fb^{-1} (14 TeV)","3000 fb^{-1} (14 TeV)","36 fb^{-1} (14 TeV)","g_{KK}#rightarrow t#bar{t} (14 TeV)","36 fb^{-1} (13 TeV) 0l+1l+2l","g_{KK}#rightarrow t#bar{t} (13 TeV)"]
##legends_comp = ["36 fb^{-1} (14 TeV)","36 fb^{-1} (14 TeV) no systematics (only stat)","36 fb^{-1} (14 TeV) double systematics","g_{KK}#rightarrow t#bar{t} (14 TeV)","36 fb^{-1} (13 TeV) 0l+1l+2l","g_{KK}#rightarrow t#bar{t} (13 TeV)"]
#to_compare=[limits,sig3,sig5]
##to_compare=[limits]
#comp_names=['limits','sig3','sig5']
#for comparison in range(len(to_compare)):
#	c3=ROOT.TCanvas(comp_names[comparison]+'_comp','',1200,1000)
#	c3.SetLogy()
#	c3.SetRightMargin(0.10)
#	c3.SetLeftMargin(margine)
#	c3.SetTopMargin(0.10)
#	c3.SetBottomMargin(margine)
#	legend3=ROOT.TLegend(0.335,0.55,0.9,0.9)
# 	legend3.SetTextSize(0.030)
#  	legend3.SetBorderSize(0)
#  	legend3.SetTextFont(42)
#  	legend3.SetLineColor(1)
#  	legend3.SetLineStyle(1)
#  	legend3.SetLineWidth(1)
#  	legend3.SetFillColor(0)
#  	legend3.SetFillStyle(0)
#  	legend3.SetHeader('g_{KK}#rightarrow t#bar{t}')
#  	
#	for i in range(len(to_compare[comparison])):
#		to_compare[comparison][i].SetLineColor(intcolor[i])
#		to_compare[comparison][i].SetLineWidth(3)
#		to_compare[comparison][i].SetLineStyle(0)
#		if i==0:
#			to_compare[comparison][i].Draw('al')
#			to_compare[comparison][i].GetXaxis().SetTitle("g_{KK} mass [TeV]")
#			to_compare[comparison][i].GetXaxis().SetRangeUser(1500,6500)
#			to_compare[comparison][i].GetYaxis().SetTitle(y_comp[comparison])
#			to_compare[comparison][i].SetMaximum(10000)
#			to_compare[comparison][i].SetMinimum(0.0007)
#			legend3.AddEntry(to_compare[comparison][i],legends_comp[i],'l')
#		else:
#			to_compare[comparison][i].Draw('l')
#			legend3.AddEntry(to_compare[comparison][i],legends_comp[i],'l')
#	theory.SetLineColor(ROOT.kBlack)
#	theory.SetLineWidth(3)
#	theory.SetLineStyle(0)
#	theory.Draw('l')
#	legend3.AddEntry(theory,legends_comp[-3],'l')
#
#	if comparison==0:
#		obs_13.SetLineColor(ROOT.kRed)
#		obs_13.SetLineWidth(3)
#		obs_13.SetLineStyle(2)
#		obs_13.Draw('l')
#		legend3.AddEntry(obs_13,legends_comp[-2],'l')
#		theory_13.SetLineColor(ROOT.kBlack)
#		theory_13.SetLineWidth(3)
#		theory_13.SetLineStyle(2)
#		theory_13.Draw('l')
#		legend3.AddEntry(theory_13,legends_comp[-1],'l')
#	legend3.Draw()
#
#	c3.SaveAs('pdf/'+c3.GetName()+'.pdf')
#
			


