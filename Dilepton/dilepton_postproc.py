#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from dileptonModule import *

testfile = os.environ["CMSSW_BASE"] + "/src/Analysis/VVAnalysis/test/9D8BBBB2-187D-CE49-9CAE-009ADB180509.root"

p=PostProcessor(".",[testfile],"(nElectron+nMuon)>2","keep_and_drop.txt",[dileptonModuleConstr()],provenance=True)
p.run()
