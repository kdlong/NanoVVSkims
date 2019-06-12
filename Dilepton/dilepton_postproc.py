#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from dileptonModule import *

#testfile = os.environ["CMSSW_BASE"] + "/src/Analysis/VVAnalysis/test/9D8BBBB2-187D-CE49-9CAE-009ADB180509.root"
#testfile = "/afs/hep.wisc.edu/cms/kdlong/WZAnalysis/CMSSW_10_4_0_patch1/src/Analysis/VVAnalysis/test/9D8BBBB2-187D-CE49-9CAE-009ADB180509.root"
testfile = "/data/kelong/NanoAODSkims/Unskimmed/44FD6740-8FBD-754E-84D7-3FE57537AEA9.root"

p=PostProcessor(".",[testfile],"(nElectron>1 || nMuon > 1)","keep_and_drop.txt",[dileptonModuleConstr()],provenance=True)
p.run()
