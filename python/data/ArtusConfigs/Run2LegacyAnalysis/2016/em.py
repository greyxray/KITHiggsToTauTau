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
  etau_fake_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "etau-fake-es" else False
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
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.settingsMinimalPlotlevelFilter_em"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname, **kwargs)
  
  # explicit configuration
  config["Channel"] = "EM"
  config["MinNElectrons"] = 1
  config["MinNMuons"] = 1

  ### HLT & Trigger Object configuration
  config["HltPaths"] = [
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"
  ]
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:24",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:24"
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:24",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:24"
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
  config["ElectronTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLElectronlegTrackIsoFilter"
  ]
  config["MuonTriggerFilterNames"] = [
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLDZFilter",
          "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v:hltMu23TrkIsoVVLEle12CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered23",
          "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v:hltMu8TrkIsoVVLEle23CaloIdLTrackIdLIsoVLMuonlegL3IsoFiltered8"
  ]

  ### Signal pair selection configuration
  config["ElectronScaleAndSmearUsed"] = True if not isEmbedded else False
  config["ElectronScaleAndSmearTag"] = "ecalTrkEnergyPostCorr"
  config["ElectronLowerPtCuts"] = ["13.0"]
  config["ElectronUpperAbsEtaCuts"] = ["2.5"]
  config["MuonLowerPtCuts"] = ["9.0"]
  config["MuonUpperAbsEtaCuts"] = ["2.4"]
  config["DiTauPairMinDeltaRCut"] = 0.3
  config["DeltaRTriggerMatchingMuons"] = 0.3
  config["DeltaRTriggerMatchingElectrons"] = 0.3
  config["DiTauPairIsTauIsoMVA"] = True
  config["TauTauRestFrameReco"] = "collinear_approximation"
  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True
  config["OSChargeLeptons"] = True
  config["AddGenMatchedParticles"] = True
  config["BranchGenMatchedElectrons"] = True
  config["BranchGenMatchedMuons"] = True

  ### Efficiencies & weights configuration
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_2.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_2.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
          "0:muonEffTrgWeight",
          "0:muonEffIDWeight",
          "1:muonEffIDWeight",

          "1:isoWeight", # TODO check if this isolation is the right one
          "1:idWeight",

          #"1:trigger_23_data_Weight",
          #"1:trigger_23_embed_Weight",
          #"1:trigger_8_data_Weight",
          #"1:trigger_8_embed_Weight",

          "0:isoWeight", # TODO check if this isolation is the right one
          "0:idWeight",
          "0:eleRecoWeight",

          #"0:trigger_23_data_Weight",
          #"0:trigger_23_embed_Weight",
          #"0:trigger_12_data_Weight",
          #"0:trigger_12_embed_Weight",
    ]
    config["EmbeddedWeightWorkspaceObjectNames"]=[
          "0:m_sel_trg_ratio",
          "0:m_sel_idEmb_ratio",
          "1:m_sel_idEmb_ratio",
          
          "1:m_iso_ratio",
          "1:m_id_ratio",
          
          #"1:m_trg23_binned_ic_data",
          #"1:m_trg23_binned_ic_embed",         
          #"1:m_trg8_binned_ic_data",
          #"1:m_trg8_binned_ic_embed",
          
          "0:e_iso_ratio",
          "0:e_id_ratio",
          "0:e_trk_ratio",

          #"0:e_trg23_binned_ic_data",
          #"0:e_trg23_binned_ic_embed",    
          #"0:e_trg12_binned_ic_data",
          #"0:e_trg12_binned_ic_embed",
    ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
          "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
          "0:gt_pt,gt_eta",
          "1:gt_pt,gt_eta",
          
          "1:m_pt,m_eta",
          "1:m_pt,m_eta",

          #"1:m_pt,m_eta,m_iso",
          #"1:m_pt,m_eta,m_iso",
          #"1:m_pt,m_eta,m_iso",
          #"1:m_pt,m_eta,m_iso",

          "0:e_pt,e_eta",
          "0:e_pt,e_eta",
          "0:e_pt,e_eta",

          #"0:e_pt,e_eta,e_iso",
          #"0:e_pt,e_eta,e_iso",
          #"0:e_pt,e_eta,e_iso",
          #"0:e_pt,e_eta,e_iso",
    ]
  else:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_2.root"
    config["RooWorkspaceWeightNames"] = [
        "1:isoWeight", # TODO check if this isolation is the right one
        "1:idWeight",

        #"1:trigger_23_data_Weight",
        #"1:trigger_23_mc_Weight",
        #"1:trigger_8_data_Weight",
        #"1:trigger_8_mc_Weight",

        "0:isoWeight", # TODO check if this isolation is the right one
        "0:idWeight",
        "0:eleRecoWeight",

        #"0:trigger_23_data_Weight",
        #"0:trigger_23_mc_Weight",
        #"0:trigger_12_data_Weight",
        #"0:trigger_12_mc_Weight",
    ]
    config["RooWorkspaceObjectNames"] = [
        "1:m_iso_ratio",
        "1:m_id_ratio",
        
        #"1:m_trg23_binned_ic_data",
        #"1:m_trg23_binned_ic_mc",         
        #"1:m_trg8_binned_ic_data",
        #"1:m_trg8_binned_ic_mc",
        
        "0:e_iso_ratio",
        "0:e_id_ratio",
        "0:e_trk_ratio",

        #"0:e_trg23_binned_ic_data",
        #"0:e_trg23_binned_ic_mc",    
        #"0:e_trg12_binned_ic_data",
        #"0:e_trg12_binned_ic_mc",
        
    ]
    config["RooWorkspaceObjectArguments"] = [
        "1:m_pt,m_eta",
        "1:m_pt,m_eta",

        #"1:m_pt,m_eta,m_iso",
        #"1:m_pt,m_eta,m_iso",
        #"1:m_pt,m_eta,m_iso",
        #"1:m_pt,m_eta,m_iso",

        "0:e_pt,e_eta",
        "0:e_pt,e_eta",
        "0:e_pt,e_eta",

        #"0:e_pt,e_eta,e_iso",
        #"0:e_pt,e_eta,e_iso",
        #"0:e_pt,e_eta,e_iso",
        #"0:e_pt,e_eta,e_iso",
    ]
  config["QCDFactorWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_legacy_v16_2.root"
  config["QCDFactorWorkspaceWeightNames"]=[
      "0:em_qcd_osss_binned_Weight",
      "0:em_qcd_extrap_up_Weight",
      "0:em_qcd_extrap_down_Weight",
      "0:em_qcd_osss_0jet_rateup_Weight",
      "0:em_qcd_osss_0jet_ratedown_Weight",
      "0:em_qcd_osss_0jet_shapeup_Weight",
      "0:em_qcd_osss_0jet_shapedown_Weight",
      "0:em_qcd_osss_1jet_rateup_Weight",
      "0:em_qcd_osss_1jet_ratedown_Weight",
      "0:em_qcd_osss_1jet_shapeup_Weight",
      "0:em_qcd_osss_1jet_shapedown_Weight",

      "0:em_qcd_extrap_uncert_Weight",
  ]
  config["QCDFactorWorkspaceObjectNames"] = [
      "0:em_qcd_osss_binned",
      "0:em_qcd_extrap_up",
      "0:em_qcd_extrap_down",
      "0:em_qcd_0jet_rateup",
      "0:em_qcd_0jet_ratedown",
      "0:em_qcd_0jet_shapeup",
      "0:em_qcd_0jet_shapedown",
      "0:em_qcd_1jet_rateup",
      "0:em_qcd_1jet_ratedown",
      "0:em_qcd_1jet_shapeup",
      "0:em_qcd_1jet_shapedown",

      "0:em_qcd_extrap_uncert",
  ]
  config["QCDFactorWorkspaceObjectArguments"] = [
      "0:e_pt,m_pt,dR,njets",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",
      "0:e_pt,m_pt,dR",

      "0:e_pt,m_pt",
  ]
  config["EventWeight"] = "eventWeight"
  config["TopPtReweightingStrategy"] = "Run1"

  ### Ntuple output quantities configuration
  config["Quantities"] =      importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.syncQuantities").build_list(isMC = (not isData) and (not isEmbedded), nickname = nickname)
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend([
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
      "nLooseElectrons",
      "nLooseMuons",
      "nDiTauPairCandidates",
      "nAllDiTauPairCandidates",
      "lep1ErrD0",
      "lep1ErrDz",
      "lep2ErrD0",
      "lep2ErrDz",
      "PVnDOF",
      #"PVchi2",
      #"drel0_1",
      #"drel0_2",
      #"drelZ_1",
      #"drelZ_2",
      "idWeight_1",
      "isoWeight_1",
      "idWeight_2",
      "isoWeight_2",
      "trackWeight_1",
      "trackWeight_2",
      "diLepMetMt",
      "pZetaVis",
      "pZetaMiss",
      "mt_tt",
      "flagMETFilter",
      "mt_tot"
  ])
  config["Quantities"].extend([
      "diLepMetMt",
      "pZetaMiss",
      "pZetaVis",
      "dr_tt",
      "diLepMetMass",
      "diLepMetPhi",
      "diLepMetEta",
      "diLepMetPt",
      "dphi_mumet",
      "dphi_emet",
      "mTdileptonMET",
      "mt_tt",
      "mTemu",
  #    "mt_sv",
      "mt_max",
      "mtmax",
      "dPhiLep1Met",
      "dPhiLep2Met",
      "dzeta"
  ])
  if isEmbedded:
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2",
          "trigger_23_data_Weight_2","trigger_23_embed_Weight_2","trigger_8_embed_Weight_2" ,"trigger_8_data_Weight_2",
          "trigger_23_data_Weight_1","trigger_23_embed_Weight_1","trigger_12_embed_Weight_1" ,"trigger_12_data_Weight_1",
          "looseIsoWeight_2","idisoWeight_1","idisoWeight_2"
           ])
  elif not isData:
    config["Quantities"].extend([
          "trigger_23_data_Weight_2","trigger_23_mc_Weight_2","trigger_8_mc_Weight_2" ,"trigger_8_data_Weight_2",
          "trigger_23_data_Weight_1","trigger_23_mc_Weight_1","trigger_12_mc_Weight_1" ,"trigger_12_data_Weight_1"
           ])
    config["Quantities"].extend([
    "trigger_12_Weight_1","trigger_23_Weight_1","trigger_8_Weight_2","trigger_23_Weight_2"
    ])
  config["Quantities"].extend([
      "em_qcd_osss_binned_Weight",
      "em_qcd_extrap_up_Weight",
      "em_qcd_extrap_down_Weight",
      "em_qcd_osss_0jet_rateup_Weight",
      "em_qcd_osss_0jet_ratedown_Weight",
      "em_qcd_osss_0jet_shapeup_Weight",
      "em_qcd_osss_0jet_shapedown_Weight",
      "em_qcd_osss_1jet_rateup_Weight",
      "em_qcd_osss_1jet_ratedown_Weight",
      "em_qcd_osss_1jet_shapeup_Weight",
      "em_qcd_osss_1jet_shapedown_Weight",
      "em_qcd_extrap_uncert_Weight"])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1p1cat",
      "htxs_stage1p1finecat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis.Includes.ggHNNLOQuantities").build_list())

  ### Processors & consumers configuration
  config["Processors"] = []
  config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetCollector",
                                                              "producer:ValidElectronsProducer",
                                                              "filter:ValidElectronsFilter",
                                                              "producer:ElectronTriggerMatchingProducer",
                                                              "filter:MinElectronsCountFilter",
                                                              "producer:ValidMuonsProducer",
                                                              "filter:ValidMuonsFilter",
                                                              "producer:MuonTriggerMatchingProducer",
                                                              "filter:MinMuonsCountFilter",
                                                              "producer:ValidTausProducer",
                                                              "producer:NewValidEMPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer"))
  if not (isData or isEmbedded): config["Processors"].append( "producer:TaggedJetCorrectionsProducer")
  config["Processors"].extend((                               "producer:ValidTaggedJetsProducer",
                                                              "producer:ValidBTaggedJetsProducer"))
  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcopy(config["Processors"])
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:MetCorrector",
                                                              "producer:PuppiMetCorrector",
                                                              "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY:                       config["Processors"].append( "producer:ZPtReweightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  if not isData and not isEmbedded:                 config["Processors"].append( "producer:RooWorkspaceWeightProducer")
  config["Processors"].append( "producer:QCDFactorProducer")
  config["Processors"].append(                                "filter:MinimalPlotlevelFilter")
  config["Processors"].append(
                                                              "producer:EventWeightProducer")
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

  # pipelines - systematic shifts
  needed_pipelines = ['nominal', 'eleES_shifts', 'regionalJECunc_shifts', 'METunc_shifts', 'METrecoil_shifts', 'btagging_shifts']
  if pipelines is None:
      raise Exception("pipelines is None in %s" % (__file__))
  elif 'auto' in pipelines:
      pipelines = needed_pipelines

  return_conf = jsonTools.JsonDict()
  for pipeline in pipelines:
      if pipeline not in needed_pipelines:
          log.warning("Warning: pipeline NOT in the list of needed pipelines. Still adding it.")
      log.info('Add pipeline: %s' %(pipeline))
      return_conf += ACU.apply_uncertainty_shift_configs('em', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2LegacyAnalysis." + pipeline).build_config(nickname, **kwargs))
  return return_conf
