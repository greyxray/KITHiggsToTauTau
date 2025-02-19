#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
import os

import HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.ArtusConfigUtility as ACU

def build_config(nickname, **kwargs):
  btag_eff = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "btag-eff" else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSignal = re.search("HToTauTau",nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.ee_settingsElectronID",
    #"HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.settingsJetID"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "EE"
  config["MinNLooseElectrons"] = 2
  config["MinNElectrons"] = 2
  config["Year"] = 2017
  # HltPaths_comment: The first path must be the single lepton trigger. A corresponding Pt cut is implemented in the Run2DecayChannelProducer..
  if re.search("(Run201|Embedding201|Summer1|Fall1)", nickname): config["HltPaths"] = [
      "HLT_Ele27_WPTight_Gsf",
      "HLT_Ele32_WPTight_Gsf",
      "HLT_Ele35_WPTight_Gsf"
  ]
  # Electron Requirements

  config["ElectronLowerPtCuts"] = ["10.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.4"]
  config["DiTauPairMinDeltaRCut"] = 0.5
    
  config["ElectronTriggerFilterNames"] = [
  "HLT_Ele27_WPTight_Gsf_v:hltEle27WPTightGsfTrackIsoFilter",
  "HLT_Ele32_WPTight_Gsf_DoubleL1EG_v:hltEle32L1DoubleEGWPTightGsfTrackIsoFilter",
  "HLT_Ele32_WPTight_Gsf_v:hltEle32WPTightGsfTrackIsoFilter",
  "HLT_Ele35_WPTight_Gsf_v:hltEle35noerWPTightGsfTrackIsoFilter",
    ]

  config["HLTBranchNames"] = [
      "trg_t_Ele27:HLT_Ele27_WPTight_Gsf_v",
      "trg_p_Ele27:HLT_Ele27_WPTight_Gsf_v",
      "trg_t_Ele32:HLT_Ele32_WPTight_Gsf_v",
      "trg_p_Ele32:HLT_Ele32_WPTight_Gsf_v",
      "trg_t_Ele32_fb:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_p_Ele32_fb:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_t_Ele35:HLT_Ele35_WPTight_Gsf_v",
      "trg_p_Ele35:HLT_Ele35_WPTight_Gsf_v",
  ]

  config["CheckTagTriggerMatch"] = [
      "trg_t_Ele27",
      "trg_t_Ele32",
      "trg_t_Ele35",
      "trg_t_Ele32_fb",
  ]
  config["CheckProbeTriggerMatch"] = [
      "trg_p_Ele27",
      "trg_p_Ele32",
      "trg_p_Ele35",
      "trg_p_Ele32_fb",
  ]

  
  config["TagAdditionalCriteria"] = [
    "pt:26.0",
    "eta:2.1",
    "dxy:0.045",
    "dz:0.2",
    "iso_sum:0.1"]

  config["TagElectronIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp90"
  config["TagElectronSecondIDName"] = "egmGsfElectronIDs:mvaEleID-Fall17-noIso-V2-wp80"
  config["TagElectronSecondIDIsoName"] = "egmGsfElectronIDs:mvaEleID-Fall17-iso-V2-wp80"
  config["TagElectronCutIDSanity"] = "egmGsfElectronIDs:cutBasedElectronID-Fall17-94X-V2-medium"
  #config["OldElectronIDName"] = "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values" if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else "electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values"
  # config["ElectronMvaIDCutEB1"] = 0.967083 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.940962684155
  # config["ElectronMvaIDCutEB2"] = 0.929117 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.899208843708
  # config["ElectronMvaIDCutEE"] = 0.726311 if re.search("(Run2015|Fall15MiniAODv2|Spring16)", nickname) else 0.758484721184
  # config["ProbeAdditionalCriteria"] = [
  #   "pt:10"]

  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = True
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["EventWeight"] = "eventWeight"

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.TagAndProbe.Includes.TagAndProbeQuantitiesEE").build_list(2017)

  config["Processors"] =   [#"producer:HltProducer",
                            "producer:ValidElectronsProducer",
                            "filter:ValidElectronsFilter",
                            "producer:ElectronTriggerMatchingProducer",
                            "filter:MinElectronsCountFilter",
                            "producer:NewEETagAndProbePairCandidatesProducer",
                            "filter:ValidDiTauPairCandidatesFilter"]
                            #"producer:TaggedJetCorrectionsProducer",
                            #"producer:ValidTaggedJetsProducer"]

  config["Consumers"] = [#"KappaLambdaNtupleConsumer",
                         "NewEETagAndProbePairConsumer",
                         "cutflow_histogram"]

  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('ee_singleelectron', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.syst_shifts_nom").build_config(nickname))


