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
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False
  pipelines = kwargs["pipelines"] if "pipelines" in kwargs else None
  minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("(W.?Jets|WG)ToLNu", nickname)
  isSignal = re.search("HToTauTau",nickname)
  isHWW = re.search("HToWW",nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)

  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsVetoMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_mt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)

  # explicit configuration
  config["Channel"] = "MT"
  config["MinNMuons"] = 1
  config["MinNTaus"] = 1

  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
          "HLT_IsoMu22",
          "HLT_IsoTkMu22",
          "HLT_IsoMu22_eta2p1",
          "HLT_IsoTkMu22_eta2p1",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1"
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_IsoMu22_v:23.0",
          "HLT_IsoTkMu22_v:23.0"
  ]
  config["CheckLepton1TriggerMatch"] = [
          "trg_singleelectron",
          "trg_singlemuon",

          "trg_mutaucross",
          "trg_doubletau",
          "trg_muonelectron_mu23ele12",
          "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
          "trg_mutaucross",
          "trg_doubletau",
          "trg_muonelectron_mu23ele12",
          "trg_muonelectron_mu8ele23",
  ]
  config["HLTBranchNames"] = [
          "trg_singleelectron:HLT_Ele25_eta2p1_WPTight_Gsf_v",
          "trg_singlemuon:HLT_IsoMu22_v",
          "trg_singlemuon:HLT_IsoTkMu22_v",
          "trg_singlemuon:HLT_IsoMu22_eta2p1_v",
          "trg_singlemuon:HLT_IsoTkMu22_eta2p1_v",
          "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v",
          "trg_mutaucross:HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v",
          "trg_doubletau:HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg_v",
          "trg_doubletau:HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg_v"
          "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
          "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v",
          "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
          "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v",
  ]
  config["MuonTriggerFilterNames"] = [
          "HLT_IsoMu22_v:hltL3crIsoL1sMu20L1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_v:hltL3fL1sMu20L1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu22_eta2p1_v:hltL3crIsoL1sSingleMu20erL1f0L2f10QL3f22QL3trkIsoFiltered0p09",
          "HLT_IsoTkMu22_eta2p1_v:hltL3fL1sMu20erL1f0Tkf22QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltL3crIsoL1sMu18erTauJet20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltL3crIsoL1sSingleMu18erIorSingleMu20erL1f0L2f10QL3f19QL3trkIsoFiltered0p09",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
  ]
  config["TauTriggerFilterNames"] = [
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltPFTau20TrackLooseIsoAgainstMuon",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_v:hltOverlapFilterIsoMu19LooseIsoPFTau20",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltPFTau20TrackLooseIsoAgainstMuon",
          "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1_v:hltOverlapFilterSingleIsoMu19LooseIsoPFTau20"
  ]
  
  ### Electron scale and smear corrections
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"

  ### Signal pair selection configuration
  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["MuonLowerPtCuts"] = ["20.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.1"]
  config["TauLowerPtCuts"] = ["30.0"]
  config["TauUpperAbsEtaCuts"] = ["2.3"]
  config["TriggerObjectLowerPtCut"] = -1.0
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedParticles"] = True
  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedMuons"] = True
  config["BranchGenMatchedTaus"] = True
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_1.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_1.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",
          
          #"1:MuTau_TauLeg_EmbeddedEfficiencyWeight",
          #"1:MuTau_TauLeg_DataEfficiencyWeight",
          
          "0:isoWeight",
          "0:idWeight",
          "0:singleTriggerMCEfficiencyWeightKIT",
          "0:singleTriggerDataEfficiencyWeightKIT",
          
          "0:crossTriggerMCEfficiencyWeight",
          "0:crossTriggerDataEfficiencyWeight"
          ]
    config["EmbeddedWeightWorkspaceObjectNames"]=[
          "0:m_sel_trg_ratio",
          "0:m_sel_idEmb_ratio",
          "1:m_sel_idEmb_ratio",
          
          #"1:t_TightIso_mt_emb",
          #"1:t_genuine_TightIso_mt_data,t_fake_TightIso_mt_data",
          
          "0:m_iso_ratio_emb",
          "0:m_id_ratio_emb",
          "0:m_trg_emb",
          "0:m_trg_data",
          
          "0:m_trgMu19leg_eta2p1_desy_mc", #temporary because not yet measured for embedded
          "0:m_trgMu19leg_eta2p1_desy_data"
          ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",
          
          #"1:t_pt,t_eta",
          #"1:t_pt,t_eta",

          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          "0:m_pt,m_eta",
          
          "0:m_pt,m_eta",
          "0:m_pt,m_eta"]
  else:
  ## Efficiencies & weights configuration
    config["SaveRooWorkspaceTriggerWeightAsOptionalOnly"] = "true"
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_1.root"
    config["RooWorkspaceWeightNames"]=[
        "0:crossTriggerMCEfficiencyWeight",
        "0:crossTriggerDataEfficiencyWeight",
        "0:singleTriggerMCEfficiencyWeightKIT",
        "0:singleTriggerDataEfficiencyWeightKIT",

        "0:isoWeight",
        "0:idWeight",
#        "0:trackWeight", # new recommendation for full run2 data/MC is to remove it (will result in SF = 1.0).
    ]
    config["RooWorkspaceObjectNames"] = [
        "0:m_trgMu19leg_eta2p1_desy_mc",
        "0:m_trgMu19leg_eta2p1_desy_data",
        "0:m_trg_mc",
        "0:m_trg_data",

        "0:m_iso_ratio",
        "0:m_id_ratio",
#        "0:m_trk_ratio",
    ]
    config["RooWorkspaceObjectArguments"] = [
        "0:m_pt,m_eta",
        "0:m_pt,m_eta",
        "0:m_pt,m_eta",
        "0:m_pt,m_eta",

        "0:m_pt,m_eta",
        "0:m_pt,m_eta",
#        "0:m_eta",
]

  config["TriggerEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_Run2016_Muon_Mu22OR_eta2p1_eff.root"]
  config["TriggerEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/triggerWeights/triggerEfficiency_MC_Muon_Mu22OR_eta2p1_eff.root"]
  config["IdentificationEfficiencyData"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_Run2016_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  config["IdentificationEfficiencyMc"] = ["0:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/identificationWeights/identificationEfficiency_MC_Muon_IdIso_IsoLt0p15_2016BtoH_eff.root"]
  config["IdentificationEfficiencyMode"] = "multiply_weights"
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["TriggerEfficiencyMode"] = "multiply_weights"
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(isMC = (not isData) and (not isEmbedded), nickname = nickname)
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "nVetoMuons",
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "triggerWeight_singleMu_1",
      "idIsoWeight_1",
      "triggerWeight_muTauCross_1",
     # "triggerWeight_muTauCross_2",
      "MuTau_TauLeg_EmbeddedEfficiencyWeight_2",
      "MuTau_TauLeg_DataEfficiencyWeight_2",
      "lep1ErrD0",
      "lep1ErrDz",
      "lep2ErrD0",
      "lep2ErrDz",
      "PVnDOF",
      #"PVchi2",
      #"drel0_1",
      #"drel0_2",
      #"drelZ_1",
      "trg_singlemuon"
      #"prefire_weight",
      #"prefire_weight_down",
      #"prefire_weight_2017",
      #"prefire_weight_2017_up",
      #"prefire_weight_2017_down"
  ])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())

  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
      "muonEffTrgWeight",
      "muonEffIDWeight_1",
      "muonEffIDWeight_2",
      # "crosstriggerWeight_1",
      # "crosstriggerWeight_2"
      ])  

  ### Processors & consumers configuration
  config["Processors"] =   []#                                  ["producer:MuonCorrectionsProducer"] if isEmbedded else []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MinMuonsCountFilter",
                                                              "producer:HttValidVetoMuonsProducer",
                                                              "producer:ValidElectronsProducer"))
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:NewValidMTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:DiVetoMuonVetoProducer"))
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  config["Processors"].extend((                               "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if not isEmbedded:             config["Processors"].extend(("producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  #if not isData and not isEmbedded:                 config["Processors"].append( "producer:MuTauTriggerWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")

  #if not isData:                 config["Processors"].append( "producer:TauTrigger2017EfficiencyProducer")
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  config["Processors"].append(                                "producer:SvfitProducer")
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  # Subanalyses settings
  if btag_eff:
     config["Processors"] = copy.deepcopy(config["ProcessorsBtagEff"])

     btag_eff_unwanted = ["KappaLambdaNtupleConsumer", "CutFlowTreeConsumer", "KappaElectronsConsumer", "KappaTausConsumer", "KappaTaggedJetsConsumer", "RunTimeConsumer", "PrintEventsConsumer"]
     for unwanted in btag_eff_unwanted:
      if unwanted in config["Consumers"]: config["Consumers"].remove(unwanted)

     config["Consumers"].append("BTagEffConsumer")

  if tau_es:
    # needed pipelines : nominal tauES_subanalysis tauMuFakeESperDM_shifts METunc_shifts METrecoil_shifts JECunc_shifts regionalJECunc_shifts btagging_shifts
    config["Quantities"].extend(["leadingTauEnergyAssymetry"])

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'tauESperDM_shifts', 'tauMuFakeESperDM_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts']
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('mt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf
