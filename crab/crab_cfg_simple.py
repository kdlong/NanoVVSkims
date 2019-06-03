from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import os

config = Configuration()
nano_dir = os.environ["CMSSW_BASE"] + "/src/PhysicsTools/NanoAODTools"
haddscript = "%s/scripts/haddnano.py" % nano_dir
keepdrop_file = "%s/python/postprocessing/analysis/NanoVVSkims/Dilepton/keep_and_drop.txt" % nano_dir
crab_script = '%s/crab/crab_script.sh' % nano_dir

#dataset = '/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/NANOAODSIM'
dataset = '/DoubleMuon/Run2016B-22Aug2018_ver2-v1/NANOAOD'

config.section_("General")
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = crab_script 
config.JobType.inputFiles = ['crab_script.py', haddscript, keepdrop_file] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.JobType.allowUndistributedCMSSW = True
config.section_("Data")
config.Data.inputDataset = dataset 

#config.Data.inputDBS = 'phys03'
(_, primaryDS, conditions, dataTier) = dataset.split('/')
isMC = "SIM" in dataTier
if not isMC:
    # Since a PD will have several eras, add conditions to name to differentiate
    #config.General.requestName = '_'.join([campaign_name, primaryDS, conditions])
    config.Data.lumiMask ='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    # Comment out in the (hopefully very rare) case where resubmit needs to 
    # be done manually
    #config.General.requestName = '_'.join([campaign_name, primaryDS, conditions, "resubmit"])
    #config.Data.lumiMask ='crab_%s/results/notFinishedLumis.json' % config.General.requestName 
    # config.Data.splitting = 'LumiBased'
    # config.Data.unitsPerJob = getUnitsPerJob(primaryDS)
config.General.requestName = "_".join(['NanoPostprocessing_Dilepton', primaryDS, 'v2'])
config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 10

config.Data.outLFNDirBase = '/store/user/%s/DileptonNanoSkims' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'NanoPostprocessing'
config.section_("Site")
config.Site.storageSite = "T2_US_Wisconsin"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'

