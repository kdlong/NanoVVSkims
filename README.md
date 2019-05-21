# NanoVVSkims
VV-specific skims of NanoAOD using NanoAOD-tools

Inspriation from the NanoAOD tools example and the VHbb analysis: https://github.com/vhbb/vhbb-nano

```shell
cmsrel CMSSW_10_2_14
cd CMSSW_10_2_14/src
cmsenv

git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
git clone https://github.com/kdlong/NanoVVSkims.git PhysicsTools/NanoAODTools/python/postprocessing/analysis/NanoVVSkims
scram b
```
