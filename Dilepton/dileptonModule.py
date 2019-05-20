import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class DileptonProducer(Module):
    def __init__(self, electronSelection, muonSelection):
        self.electronSel = electronSelection
        self.muonSel = muonSelection
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("nLooseMuon",  "I");
        self.out.branch("nLooseElec",  "I");
        self.out.branch("nTightMuon",  "I");
        self.out.branch("nTightElec",  "I");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")

        looseMuons = []
        tightMuons = []
        for muon in filter(self.muonSel, muons):
            if muon.looseId and muon.pfRelIso03_all < 0.4:
                looseMuons.append(muon)
            else:
                continue
            if muon.tightId and muon.pfRelIso03_all < 0.15:
                tightMuons.append(muon)

        looseElectrons = []
        tightElectrons = []
        for electron in filter(electronSel, eletrons):
            if electron.cutBased == 1:
                looseElectrons.append(electron)
            else:
                continue
            if electron.cutBased == 4:
                tightElectrons.append(electron)

        self.out.fillBranch("nLooseMuon",len(looseMuons))
        self.out.fillBranch("nLooseElec",len(looseElectrons))
        self.out.fillBranch("nTightMuon",len(tightMuons))
        self.out.fillBranch("nTightElec",len(tightElectrons))

        return (len(looseMuons) + len(looseElectrons)) > 1


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

dileptonModuleConstr = lambda : dileptonProducer(electronSelection= lambda l : l.pt > 10, muonSelection= lambda l : l.pt > 10) 
 
