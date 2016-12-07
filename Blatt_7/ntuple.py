from basf2 import *
from modularAnalysis import *

# Implement your code here.

#access rootfile
inputMdst("/scratch/TP1/gen_mc_data.root")

#create particle lists for Kaons and Pions
fillParticleList("K-","Kid>0.1")
fillParticleList("pi+","piid>0.1")
reconstructDecay("D0 -> K- pi+","M<4.0")

#apply cut on momentum
#applyCuts("D0","p<2.5")

#reconstruct D*+ -> D0 pi+
reconstructDecay("D*+ -> D0 pi+","M<6.0")

#check MCTruth
matchMCTruth("D*+")
cutAndCopyList("D*+:sig","D*+","isSignal == 1")

#apply cuts on D*+:sig
#applyCuts("D*+:sig","Q<0.02")
#applyCuts("D*+:sig","1.7<daughter(0,M)<2.05")
applyCuts("D*+","0.005<Q<0.007")

#saving variables as rootfile
#variablesToNTuple("D*+" , ["M","formula(M - daughter(0, M))","Q"],filename="1.3_D*+_sig_NTuple.root")
variablesToNTuple("D*+" , ["daughter(0, M)", "M","formula(M - daughter(0, M))","Q"], filename="1.5_Qcut_NTuple.root")


process(analysis_main)

#saving variables as rootfile
#variablesToNTuple("D0", ["M","p"])

#process(analysis_main)


print(statistics)
