import ROOT 
from ROOT import TCanvas, TPad, TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend 
from ROOT import kBlack, kBlue, kRed 
from ROOT import gBenchmark, gStyle, gROOT, gDirectory 
from ROOT import TLatex

########################################## 
# Extra Cosmetics 
gStyle.SetOptStat(0) 
cmsText = "CMS" 
cmsTextFont = 61 
 
#writeExtraText = False
writeExtraText = True
#extraText   = "Preliminary" 
extraText = "Work-in-progress"
extraTextFont = 52;  # default is helvetica-italics 
 
# text sizes and text offsets with respect to the top frame 
# in unit of the top margin size 
lumiTextSize     = 0.30
lumiTextOffset   = 0.2 
 
cmsTextSize     = 0.75; 
cmsTextSize = 0.45; 
cmsTextOffset = 0.1;  # only used in outOfFrame version 
 
relPosX = 0.04 #0.045 default 
relPosY = 0.035 
relExtraDY = 1 
relExtraDX = 1.5 #2.2 default
 
extraOverCmsTextSize  = 0.76 	
lumi_sqrtS = "" 
drawLogo      = False

lumi_13TeV = "35.9 fb^{-1}" # previously 20.1 
lumi_8TeV  = "19.7 fb^{-1}" 
lumi_7TeV  = "5.1 fb^{-1}"       
        

def set_CMS_lumi(pad, iPeriod, iPosX, lumival):
        #pad = TPad('pad1','This is pad1',0.02,0.52,0.48,0.98,21)
        outOfFrame    = False
        if (iPosX/10==0):
            outOfFrame = True
        
        alignY_=3
        alignX_=2
        
        if (iPosX==0):
            alignX_=1
        if (iPosX==0):
            alignY_=1
        if (iPosX/10==1):
            alignX_=1
        if (iPosX/10==2):
            alignX_=2
        if (iPosX/10==3):
            alignX_=3
        align_ = 10*alignX_ + alignY_
        
        H = pad.GetWindowHeight()
        W = pad.GetWindowWidth()
        l = pad.GetLeftMargin()
        r = pad.GetRightMargin()
        t = pad.GetTopMargin()
        b = pad.GetBottomMargin()
        
        pad.cd()
	
	lumi_7TeV = str(lumival)+" fb^{-1}"
	lumi_8TeV = str(lumival)+ " fb^{-1}"
	lumi_13TeV = str(lumival)+" fb^{-1}" 
        
        if (iPeriod==1):
            lumiText = lumi_7TeV
            lumiText += " (7TeV)"
        elif (iPeriod==2):
            lumiText = lumi_8TeV
            lumiText += " (8TeV)"
        elif (iPeriod==3):
            lumiText = lumi_8TeV
            lumiText += " (8 TeV)"
            lumiText += " + "
            lumiText += lumi_7TeV
            lumiText += " (7 TeV)"
        elif (iPeriod==4):
            lumiText = lumi_13TeV
            lumiText += " (13 TeV)"
        elif (iPeriod==7):
            if (outOfFrame):
                lumiText += "#scale[0.85]{"
                lumiText += lumi_13TeV; 
                lumiText += " (13 TeV)";
                lumiText += " + ";
                lumiText += lumi_8TeV; 
                lumiText += " (8 TeV)";
                lumiText += " + ";
                lumiText += lumi_7TeV;
                lumiText += " (7 TeV)";
                if (outOfFrame):
                    lumiText += "}"
        elif (iPeriod==12):
            lumiText += "8 TeV"
        elif (iPeriod==0):
            lumiText += lumi_sqrtS
            
       
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(kBlack)
        
        extraTextSize = extraOverCmsTextSize*cmsTextSize
        
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(lumiTextSize*t)
        latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
        
        if (outOfFrame):
            latex.SetTextFont(cmsTextFont)
            latex.SetTextAlign(11)
            latex.SetTextSize(cmsTextSize*t) 
            latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
        
        pad.cd()
        
        posX_=0
        if (iPosX%10<=1):
            posX_ =   l + relPosX*(1-l-r)
        elif (iPosX%10==2):
            posX_ =  l + 0.5*(1-l-r)
        elif (iPosX%10==3):
            posX_ =  1-r - relPosX*(1-l-r)
        posY_ = 1-t - relPosY*(1-t-b)
        
        if (outOfFrame==False):
            if (drawLogo):
                posX_ =   l + 0.045*(1-l-r)*W/H;
                posY_ = 1-t - 0.045*(1-t-b);
                xl_0 = posX_;
                yl_0 = posY_ - 0.15;
                xl_1 = posX_ + 0.15*H/W;
                yl_1 = posY_;
                #TASImage* CMS_logo = new TASImage("CMSlogoBW.png");
                pad_logo = TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
                pad_logo.raw();
                pad_logo.cd();
                CMS_logo.Draw("X");
                pad_logo.Modified();
                pad.cd();
                
            else:
                latex.SetTextFont(cmsTextFont);
                latex.SetTextSize(cmsTextSize*t);
                latex.SetTextAlign(align_);
                latex.DrawLatex(posX_, posY_, cmsText);
                
                if (writeExtraText==True):
                    #posX_ =   l +  relPosX*(1-l-r);
                    #posY_ =   1-t+lumiTextOffset*t;
                    
                    # posX_= l +  relPosX*(1-l-r)
                    #posY_= 1-t+lumiTextOffset*t
                    latex.SetTextFont(extraTextFont)
                    latex.SetTextAlign(align_)
                    latex.SetTextSize(extraTextSize*t)
                    latex.DrawLatex(posX_+relExtraDX*cmsTextSize*t, posY_, extraText) 
                                    #posY_-relExtraDY*cmsTextSize*t, extraText)
                    #latex.DrawLatex(posX_, posY_, extraText)
                elif (writeExtraText):
                    if (iPosX==0):
                        posX_= l +  relPosX*(1-l-r)
                        posY_= 1-t+lumiTextOffset*t
                    latex.SetTextFont(extraTextFont);
                    latex.SetTextSize(extraTextSize*t);
                    latex.SetTextAlign(align_);
                    latex.DrawLatex(posX_, posY_, extraText);      
                    
        return;

def CMS_lumi(pad, iPeriod, iPosX, isMC):
        #pad = TPad('pad1','This is pad1',0.02,0.52,0.48,0.98,21)
        outOfFrame    = False
        if (iPosX/10==0):
            outOfFrame = True
        
        alignY_=3
        alignX_=2
        
        if (iPosX==0):
            alignX_=1
        if (iPosX==0):
            alignY_=1
        if (iPosX/10==1):
            alignX_=1
        if (iPosX/10==2):
            alignX_=2
        if (iPosX/10==3):
            alignX_=3
        align_ = 10*alignX_ + alignY_
        
        H = pad.GetWindowHeight()
        W = pad.GetWindowWidth()
        l = pad.GetLeftMargin()
        r = pad.GetRightMargin()
        t = pad.GetTopMargin()
        b = pad.GetBottomMargin()
        
        pad.cd()
	if isMC:
	    lumi_7TeV = "1 fb^{-1}"
	    lumi_8TeV = "1 fb^{-1}"
	    lumi_13TeV = "1 fb^{-1}" 
	else:
	    lumi_13TeV = "35.9 fb^{-1}" # previously 20.1 
            lumi_8TeV  = "19.7 fb^{-1}" 
	    lumi_7TeV  = "5.1 fb^{-1}"       
        
        if (iPeriod==1):
            lumiText = lumi_7TeV
            lumiText += " (7TeV)"
        elif (iPeriod==2):
            lumiText = lumi_8TeV
            lumiText += " (8TeV)"
        elif (iPeriod==3):
            lumiText = lumi_8TeV
            lumiText += " (8 TeV)"
            lumiText += " + "
            lumiText += lumi_7TeV
            lumiText += " (7 TeV)"
        elif (iPeriod==4):
            lumiText = lumi_13TeV
            lumiText += " (13 TeV)"
        elif (iPeriod==7):
            if (outOfFrame):
                lumiText += "#scale[0.85]{"
                lumiText += lumi_13TeV; 
                lumiText += " (13 TeV)";
                lumiText += " + ";
                lumiText += lumi_8TeV; 
                lumiText += " (8 TeV)";
                lumiText += " + ";
                lumiText += lumi_7TeV;
                lumiText += " (7 TeV)";
                if (outOfFrame):
                    lumiText += "}"
        elif (iPeriod==12):
            lumiText += "8 TeV"
        elif (iPeriod==0):
            lumiText += lumi_sqrtS
            
       
        latex = ROOT.TLatex()
        latex.SetNDC()
        latex.SetTextAngle(0)
        latex.SetTextColor(kBlack)
        
        extraTextSize = extraOverCmsTextSize*cmsTextSize
        
        latex.SetTextFont(42)
        latex.SetTextAlign(31)
        latex.SetTextSize(lumiTextSize*t)
        latex.DrawLatex(1-r,1-t+lumiTextOffset*t,lumiText)
        
        if (outOfFrame):
            latex.SetTextFont(cmsTextFont)
            latex.SetTextAlign(11)
            latex.SetTextSize(cmsTextSize*t) 
            latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
        
        pad.cd()
        
        posX_=0
        if (iPosX%10<=1):
            posX_ =   l + relPosX*(1-l-r)
        elif (iPosX%10==2):
            posX_ =  l + 0.5*(1-l-r)
        elif (iPosX%10==3):
            posX_ =  1-r - relPosX*(1-l-r)
        posY_ = 1-t - relPosY*(1-t-b)
        
        if (outOfFrame==False):
            if (drawLogo):
                posX_ =   l + 0.045*(1-l-r)*W/H;
                posY_ = 1-t - 0.045*(1-t-b);
                xl_0 = posX_;
                yl_0 = posY_ - 0.15;
                xl_1 = posX_ + 0.15*H/W;
                yl_1 = posY_;
                #TASImage* CMS_logo = new TASImage("CMSlogoBW.png");
                pad_logo = TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
                pad_logo.raw();
                pad_logo.cd();
                CMS_logo.Draw("X");
                pad_logo.Modified();
                pad.cd();
                
            else:
                latex.SetTextFont(cmsTextFont);
                latex.SetTextSize(cmsTextSize*t);
                latex.SetTextAlign(align_);
                latex.DrawLatex(posX_, posY_, cmsText);
                
                if (writeExtraText==True):
                    #posX_ =   l +  relPosX*(1-l-r);
                    #posY_ =   1-t+lumiTextOffset*t;
                    
                    # posX_= l +  relPosX*(1-l-r)
                    #posY_= 1-t+lumiTextOffset*t
                    latex.SetTextFont(extraTextFont)
                    latex.SetTextAlign(align_)
                    latex.SetTextSize(extraTextSize*t)
                    latex.DrawLatex(posX_+relExtraDX*cmsTextSize*t, posY_, extraText) 
                                    #posY_-relExtraDY*cmsTextSize*t, extraText)
                    #latex.DrawLatex(posX_, posY_, extraText)
                elif (writeExtraText):
                    if (iPosX==0):
                        posX_= l +  relPosX*(1-l-r)
                        posY_= 1-t+lumiTextOffset*t
                    latex.SetTextFont(extraTextFont);
                    latex.SetTextSize(extraTextSize*t);
                    latex.SetTextAlign(align_);
                    latex.DrawLatex(posX_, posY_, extraText);      
                    
        return;
