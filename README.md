# NanoVVSkims
VV-specific skims of NanoAOD using NanoAOD-tools

Inspriation from the NanoAOD tools example and the VHbb analysis: https://github.com/vhbb/vhbb-nano

```shell
cmsrel CMSSW_10_4_0
cd CMSSW_10_4_0/src
cmsenv

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/kdlong/vhbb-nano.git PhysicsTools/NanoAODTools/python/postprocessing/analysis/NanoVVSkims
scram b
```
