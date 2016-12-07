from ROOT import TCanvas, TF1, TH1F, TFile, gSystem, gStyle, gROOT, TColor
import numpy as np

gROOT.SetBatch(True)



class Dmeson(object):
    
    #self.breitWFit

    def __init__(self):
        
        self.breitWFit=TF1()

        print('ROOT file opened')

        # Load ROOT file with the D0 mass distribution

        self.loadFile = TFile('hist.root')

    def __del__(self):

        print('Plot saved')

    def setstyle(self):

        # Delete previous PostScript plots and set Canvas options

        gSystem.Exec('rm -f '+'D0.pdf')
        gSystem.Exec('rm -f '+'Fit.pdf')
        gStyle.SetCanvasBorderMode(0)
        gStyle.SetCanvasColor(0)
        gStyle.SetStatBorderSize(1)
        gStyle.SetStatColor(0)



    def plotAndFit(self):

        # Plot 
        self.setstyle()

        # Get D0 histogram out of file 'loadFile'
        h1 = self.loadFile.Get('hist')
        h1.UseCurrentStyle()

        # Plot D0 mass distribution before fit
        c1 = TCanvas('c1', 'Canvas1', 0, 0, 700, 500)
        c1.Clear()
        h1.Draw()
        c1.Update()
        c1.SaveAs('D0.pdf')
           
         
        # Fit h1 with Breit-Wigner distribution

        breitW = TF1('breitW', BreitWig, 1.7, 2.0, 5)
        breitW.SetNpx(1000)
        
        fkt = TF1("fkt","gaus",1.8,1.95)
  

        # The value given in breitW.SetParameter(1, 1.8648) is the 
	# PDG value of the D0 mass

        breitW.SetParameter(0, 0.05) # Width
        breitW.SetParameter(1, 1.8648) # Mean Value
        breitW.SetParameter(2, 0.1) # Norm
        breitW.SetParameter(3, 1.75) # Bkg parameter 1
        breitW.SetParameter(4, 0.0) # Bkg parameter 2

        gStyle.SetStatH(0.4)

	# Choose fit options: Print fit probability,
	# chisquare/number of degress of freedom,
	# errors, name/value of parameters

        gStyle.SetOptFit(1111)

        h1.UseCurrentStyle()

	# Start fit with breitW	
        
        h1.Fit("breitW")
        self.breitWFit=breitW.Clone()
        #h1.Fit("fkt")        
        #mean = fkt.GetParameter(1)
        #error = fkt.GetParError(1)  
        #fkt.SetLineColor(3)
        #fkt.Draw("SAME")
        breitW.Draw("same")
        c1.Update()
        c1.SaveAs("Fit_gaus.pdf")
        
        print "width=",breitW.GetParameter(0),"  mean=",breitW.GetParameter(1)
        #print "sigma=",fkt.GetParameter(2),"  gauss_mean=",mean
        
        x_min=1.8
        x_max=1.95

#    def sigToBkgRatio(self, x_min, x_max):
        ges=self.breitWFit.Integral(x_min,x_max)
        bkg_fkt_1 = TF1("bkg_fkt_1", bkg1, 1.7, 2.0, 5)
        bkg_fkt_2 = TF1("bkg_fkt_2", bkg2, 1.7, 2.0, 5)
        bkg_fkt_3 = TF1("bkg_fkt_3", bkg3, 1.7, 2.0, 5)
        print par
        bkg_1=bkg_fkt_1.Integral(x_min,x_max)
        print bkg_1
        bkg_2=bkg_fkt_2.Integral(x_min,x_max)
        print bkg_2
        bkg_3=bkg_fkt_3.Integral(x_min,x_max)
        print bkg_3
        sbr1 = (ges-bkg_1)/bkg_1
        sbr2 = (ges-bkg_2)/bkg_2
        sbr3 = (ges-bkg_3)/bkg_3
        
        print "signal-to-background ratio between ",x_min, " and ",x_max," for linear background:\n (S/B)_lin= ",sbr1,"\n\n\n"
        print "signal-to-background ratio between ",x_min, " and ",x_max," for exponential background:\n (S/B)_exp= ",sbr2,"\n\n\n"
        print "signal-to-background ratio between ",x_min, " and ",x_max," for quadratic background:\n (S/B)_quad= ",sbr2,"\n\n\n"
      

def BreitWig(x, par):

    f = (par[0]/2.)*par[2]/((x[0] - par[1])*(x[0] - par[1]) + (par[0]/2.)*(par[0]/2.)) + bkg1(x, par)

    return f


def bkg1(x, par):

    # Simple background model with constant and linear term.

    return par[3] + par[4]*x[0]


def bkg2(x, par):

    # Simple background model with constant and exponential term.

    return par[3]*np.exp(par[4]*x[0])


def bkg3(x, par):

    # Simple background model with quadratic term.

    return (par[3] - x[0])*(par[3] - x[0])*par[4]


# Declaration of an object of the class Dmeson

hist=TFile("hist.root")
d = Dmeson()
d.plotAndFit()
#d.sigToBkgRatio(1.8,1.95)
