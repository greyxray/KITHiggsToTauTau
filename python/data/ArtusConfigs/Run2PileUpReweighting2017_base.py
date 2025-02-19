
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

def build_config(nickname, **kwargs):
  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))
  
  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50|150)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  year = datasetsHelper.base_dict[nickname]["year"]
  
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.settingsKappa"
    ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)
  
  # explicit configuration
  config["SkipEvents"] = 0
  config["EventCount"] = -1
  config["InputIsData"] = False
  BosonPdgIds = {
      "DY.?JetsToLL|EWKZ2Jets|Embedding(2016|MC)" : [
        23
      ],
      "^(GluGlu|GluGluTo|VBF|Wminus|Wplus|Z)(HToTauTau|H2JetsToTauTau)" : [
        25
      ],
      "W.?JetsToLN|EWKW" : [
        24
      ],
      "SUSY(BB|GluGlu|GluGluTo)(BB)?HToTauTau" : [
        25,
        35,
        36
        ]
  }
  config["BosonPdgIds"] = [0]
  for key, pdgids in BosonPdgIds.items():
    if re.search(key, nickname): config["BosonPdgIds"] = pdgids
  
  config["BosonStatuses"] = [62]
  config["TopPtReweightingStrategy"] = "Run1"
  if isData or isEmbedded:                config["PileupWeightFile"] = "not needed"
  elif year == 2016: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2016_271036-284044_13TeVMoriond17_23Sep2016ReReco_69p2mbMinBiasXS.root"
  elif year == 2017: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2017_294927-306462_13TeVFall17_31Mar2018ReReco_69p2mbMinBiasXS/%s.root"%nickname
  elif year == 2018: config["PileupWeightFile"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/pileup/Data_Pileup_2018_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18.root"
  else:
    print "PileupWeightFile not defined"
    exit(1)
  
  config["OutputPath"] = "output.root"
  
  config["Processors"] = []
  config["Processors"].append(                                    "producer:NicknameProducer")
  config["Processors"].extend((                                   "producer:CrossSectionWeightProducer",
                                                                  "producer:GeneratorWeightProducer",
                                                                  "producer:PUWeightProducer",
                                                                  "producer:NumberGeneratedEventsWeightProducer"))
  if isWjets or isDY:                config["Processors"].append( "producer:GenBosonFromGenParticlesProducer")
  if isDY or isEmbedded:             config["Processors"].append( "producer:GenDiLeptonDecayModeProducer")
  config["Processors"].extend((                                   "producer:GenParticleProducer",
                                                                  "producer:GenPartonCounterProducer"))
  if isWjets or isDY or isEmbedded:  config["Processors"].append("producer:GenBosonDiLeptonDecayModeProducer")
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")

  # pipelines - channels including systematic shifts
  config["Pipelines"] = jsonTools.JsonDict()
  config["Pipelines"] += importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2PileUpReweighting2017.pu").build_config(nickname)

  return config
