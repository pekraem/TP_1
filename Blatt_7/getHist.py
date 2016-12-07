from ROOT import TFile, TH1F, TH2F,  TTree, gROOT, TCanvas

#gROOT.SetBatch(False)

# FIXME Implement your code here. 


inputfile = TFile("1.5_Qcut_NTuple.root")
tree = inputfile.Get("variables")
branchlist = tree.GetListOfBranches()
hist = TH1F("hist","hist",100,0.7,2.3)

c = TCanvas("c","c",800, 600)
tree.Draw(branchlist[1].GetName()+">>hist")

hist.SaveAs("hist_full.root")

print hist
hist.Draw()

