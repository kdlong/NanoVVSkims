# Modified from N. Smith, U. Wisconsin
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
import ConfigParser
import os
import re
import subprocess
import sys
import datetime
import glob
import hashlib

#Should go in the settings file
nano_dir = os.environ["CMSSW_BASE"] + "/src/PhysicsTools/NanoAODTools"
analysis_dir = '%s/python/postprocessing/analysis/NanoVVSkims' % nano_dir
haddscript = "%s/scripts/haddnano.py" % nano_dir
keepdrop_file = "%s/Dilepton/keep_and_drop.txt" % analysis_dir
crab_dir = '%s/crab' % nano_dir
crab_script = '%s/crab_script.py' % crab_dir

settingsFile = "%s/crab/CrabTemplates/local.txt" % analysis_dir
if not os.path.exists(settingsFile):
    print "Please copy local.template.txt to local.txt and edit as appropriate"
    exit()
localSettings = ConfigParser.ConfigParser()
localSettings.read(settingsFile)

os.chdir(analysis_dir)
gitDescription = subprocess.check_output(["git", "describe", "--always"]).strip()
gitStatus = subprocess.check_output(["git", "status", "--porcelain", "-uno"])
if gitStatus != "":
    print "\033[33mWARNING: git status is dirty!\033[0m"
    print gitStatus
    gitDescription += "*"
print "Git status is %s" % gitDescription
os.chdir(nano_dir)
# We have to hack our way around how crab parses command line arguments :<
dataset = 'dummy'
for arg in sys.argv:
    if 'Data.inputDataset=' in arg:
        dataset = arg.split('=')[1]
if dataset == 'dummy':
    raise Exception("Must pass dataset argument as Data.inputDataset=...")

(_, primaryDS, conditions, dataTier) = dataset.split('/')
if 'NANOAODSIM' in dataTier:
    isMC = 1
elif dataTier == 'NANOAODSIM' or "NANOAOD" in dataset:
    isMC = 0
else:
    raise Exception("Dataset malformed? Couldn't deduce isMC parameter")

def getUnitsPerJob(ds):
    if isMC == 0:
        # The difference is due to trigger rates
        if 'Double' in ds:
            return 75
        elif 'MuonEG' in ds:
            return 75
        elif 'Single' in ds:
            return 50
        else:
            return 75
    else:
        return 50

config = config()
config.Data.inputDataset = dataset
config.Data.outputDatasetTag = conditions
today = datetime.date.today().strftime("%d%b%Y")
campaign_name = localSettings.get("local", "campaign").replace("$DATE", today)
if isMC:
    config.General.requestName = '_'.join([campaign_name, primaryDS])
    # Check for extension dataset, force unique request name
    m = re.match(r".*(_ext[0-9]*)-", conditions)
    if m:
        config.General.requestName += m.groups()[0]
    config.Data.splitting = 'FileBased'
    config.Data.unitsPerJob = getUnitsPerJob(primaryDS)
else:
    # Since a PD will have several eras, add conditions to name to differentiate
    config.General.requestName = '_'.join([campaign_name, primaryDS, conditions])
    config.Data.lumiMask ='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
    # Comment out in the (hopefully very rare) case where resubmit needs to 
    # be done manually
    #config.General.requestName = '_'.join([campaign_name, primaryDS, conditions, "resubmit"])
    #config.Data.lumiMask ='crab_%s/results/notFinishedLumis.json' % config.General.requestName 
    
    config.Data.splitting = 'LumiBased'
    config.Data.unitsPerJob = getUnitsPerJob(primaryDS)

# Max requestName is 100 characters
if len(config.General.requestName) > 100:
    bits = 5
    h = hashlib.sha256(config.General.requestName).hexdigest()
    # Replace last 5 characters with hash in case of duplicates after truncation
    config.General.requestName = config.General.requestName[:(100-bits)] + h[:bits]

# Things that don't change with dataset
config.General.workArea = '.'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '%s/PSet.py' % crab_dir
config.JobType.numCores = 1
config.JobType.inputFiles = [crab_script, haddscript, keepdrop_file] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.scriptExe = crab_script 
config.JobType.sendPythonFolder	 = True
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDBS = 'global' if 'USER' not in dataset else 'phys03'
config.Data.useParent = False
config.Data.publication = False
outdir = localSettings.get("local", "outLFNDirBase").replace(
    "$USER", getUsernameFromSiteDB()).replace("$DATE", today)
config.Data.outLFNDirBase = outdir 
config.Data.ignoreLocality = False

config.Site.storageSite = localSettings.get("local", "storageSite")
