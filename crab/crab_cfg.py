from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import os

config = Configuration()
nano_dir = os.environ["CMSSW_BASE"] + "/src/PhysicsTools/NanoAODTools"
haddscript = "%s/scripts/haddnano.py" % nano_dir
keepdrop_file = "%s/python/postprocessing/analysis/NanoVVSkims/Dilepton/keep_and_drop.txt" % nano_dir
crab_script = '%s/crab/crab_script.sh' % nano_dir

config.section_("General")
config.General.requestName = 'NanoPostprocessing_DYDileptonTest'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = crab_script 
config.JobType.inputFiles = ['crab_script_dilepton.py', haddscript, keepdrop_file] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 2
config.Data.totalUnits = 10

config.Data.outLFNDirBase = '/store/user/%s/DileptonNanoSkims' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoPostprocessing'
config.section_("Site")
config.Site.storageSite = "T2_US_WISCONSIN"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

