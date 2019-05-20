#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class DileptonAnalysis(Module):
    def __init__(self):
	    self.writeHistFile=True

    def beginJob(self,histFile=None,histDirName=None):
	    Module.beginJob(self,histFile,histDirName)

preselection="(nElectron + nMuon) > 1"
files=[" root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/2CE738F9-C212-E811-BD0E-EC0D9A8222CE.root"]
p=PostProcessor(".",files,cut=preselection,branchsel=None,modules=[DileptonAnalysis()],noOut=True,histFileName="histOut.root",histDirName="plots")
p.run()
