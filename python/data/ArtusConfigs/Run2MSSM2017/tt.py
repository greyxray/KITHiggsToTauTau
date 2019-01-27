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
  minimal_setup = True if "minimal_setup" in kwargs and kwargs["minimal_setup"] else False

  config = jsonTools.JsonDict()
  datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  # define frequently used conditions
  isEmbedded = datasetsHelper.isEmbedded(nickname)
  isData = datasetsHelper.isData(nickname) and (not isEmbedded)
  isTTbar = re.search("TT(To|_|Jets)", nickname)
  isDY = re.search("DY.?JetsToLLM(10to50|50)", nickname)
  isWjets = re.search("W.?JetsToLNu", nickname)
  isSignal = re.search("HToTauTau",nickname)
  isGluonFusion = re.search("GluGluHToTauTauM125", nickname)
  
  ## fill config:
  # includes
  includes = [
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsLooseElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsLooseMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsElectronID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsMuonID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsTauID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsJEC",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsSvfit",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsBTaggedJetID",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsTauES",
    "HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.settingsMinimalPlotlevelFilter_tt"
  ]
  for include_file in includes:
    analysis_config_module = importlib.import_module(include_file)
    config += analysis_config_module.build_config(nickname)

  # explicit configuration
  config["Channel"] = "TT"
  config["MinNTaus"] = 2
  if re.search("(Run201|Summer1|Fall1)", nickname): config["HltPaths"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
          "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v",
    ]
  elif re.search("Embedding201", nickname): config["HltPaths"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
          "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1"
    ]

  config["TauID"] = "TauIDRecommendation13TeV"
  config["TauUseOldDMs"] = True
  config["TauLowerPtCuts"] = ["25.0"]
  config["TauUpperAbsEtaCuts"] = ["2.1"]
  config["DiTauPairMinDeltaRCut"] = 0.5
  config["DeltaRTriggerMatchingTaus"] = 0.5
  config["DeltaRTriggerMatchingJets"] = 0.5
  config["DiTauPairIsTauIsoMVA"] = True
  config["DiTauPairLepton1LowerPtCuts"] = [
          "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v:40.0",
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
          "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:25.0",
  ]
  config["DiTauPairLepton2LowerPtCuts"] = [
          "HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v:40.0",
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:40.0",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:45.0",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:45.0",
          "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:25.0",
  ]
  #config["DiTauPairJet1LowerPtCuts"] = [
  #        "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:115.0"
  #]
  #config["DiTauPairJet2LowerPtCuts"] = [
  #        "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:40.0"
  #]
  #config["DiTauPairJetsLowerMjjCuts"] = [
  #        "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:650.0"
  #]
  # At the moment only the first filter given per path is checked.
  config["DiTauPairTrailingJetFilters"] = [
          "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:hltMatchedVBFTwoPFJets2CrossCleanedFromDoubleLooseChargedIsoPFTau20"
  ]
  config["CheckLepton1L1Match"] = [
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso"
  ]
  config["CheckLepton2L1Match"] = [
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso"
  ]
  config["CheckLepton1TriggerMatch"] = [
      "trg_singlemuon_24",
      "trg_singlemuon_27",
      "trg_singletau_leading",
      "trg_singleelectron_27",
      "trg_singleelectron_32",
      "trg_singleelectron_32_fallback",
      "trg_singleelectron_35",

      "trg_crossmuon_mu20tau27",
      "trg_crossele_ele24tau30",
      "trg_doubletau_20_vbf",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["CheckLepton2TriggerMatch"] = [
      "trg_singletau_trailing",

      "trg_crossmuon_mu20tau27",
      "trg_crossele_ele24tau30",
      "trg_doubletau_20_vbf",
      "trg_doubletau_35_tightiso_tightid",
      "trg_doubletau_40_mediso_tightid",
      "trg_doubletau_40_tightiso",
      "trg_muonelectron_mu12ele23",
      "trg_muonelectron_mu23ele12",
      "trg_muonelectron_mu8ele23",
  ]
  config["CheckJetsTriggerMatch"] = [
      "trg_doubletau_20_vbf"
  ]
  config["HLTBranchNames"] = [
      "trg_singlemuon_24:HLT_IsoMu24_v",
      "trg_singlemuon_27:HLT_IsoMu27_v",
      "trg_crossmuon_mu20tau27:HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v",
      "trg_singleelectron_27:HLT_Ele27_WPTight_Gsf_v",
      "trg_singleelectron_32:HLT_Ele32_WPTight_Gsf_v",
      "trg_singleelectron_32_fallback:HLT_Ele32_WPTight_Gsf_DoubleL1EG_v",
      "trg_singleelectron_35:HLT_Ele35_WPTight_Gsf_v",
      "trg_crossele_ele24tau30:HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v",
      "trg_doubletau_35_tightiso_tightid:HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_mediso_tightid:HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
      "trg_doubletau_40_tightiso:HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v",
      "trg_doubletau_20_vbf:HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v",
#      "trg_doubletau_20_vbf_jets:HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v",
      "trg_singletau_leading:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_singletau_trailing:HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v",
      "trg_muonelectron_mu12ele23:HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu23ele12:HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v",
      "trg_muonelectron_mu8ele23:HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v",
  ]
  config["TauTrigger2017InputOld"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017.root"
  config["TauTrigger2017Input"] = "$CMSSW_BASE/src/TauTriggerSFs2017/TauTriggerSFs2017/data/tauTriggerEfficiencies2017_New.root"
  config["TauTrigger2017WorkingPoints"] = [
       "vvloose",
       "vloose",
       "loose",
       "medium",
       "tight",
       "vtight",
       "vvtight",
  ]
  config["TauTrigger2017IDTypes"] = [
       "MVA",
  ]
  config["TauTrigger2017EfficiencyWeightNames"] = [
      "0:crossTriggerMCEfficiencyWeight",
      "0:crossTriggerDataEfficiencyWeight",
      "1:crossTriggerMCEfficiencyWeight",
      "1:crossTriggerDataEfficiencyWeight",
  ]
  config["EventWeight"] = "eventWeight"
  if isEmbedded:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_6.root"
    config["EmbeddedWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v17_6.root"
    config["EmbeddedWeightWorkspaceWeightNames"]=[
            "0:muonEffTrgWeight",
            "0:muonEffIDWeight",
            "1:muonEffIDWeight",
            "0:triggerWeight",
            "1:triggerWeight",
            ]
    config["EmbeddedWeightWorkspaceObjectNames"]=[
            "0:m_sel_trg_ratio",
            "0:m_sel_idEmb_ratio",
            "1:m_sel_idEmb_ratio",
            "0:tt_emb_PFTau35OR40_tight_kit_ratio",
            "1:tt_emb_PFTau35OR40_tight_kit_ratio",
            ]
    config["EmbeddedWeightWorkspaceObjectArguments"] = [
            "0:gt1_pt,gt1_eta,gt2_pt,gt2_eta",
            "0:gt_pt,gt_eta",
            "1:gt_pt,gt_eta",
            "0:t_pt",
            "1:t_pt",
            ]
  else:
    config["RooWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
    config["TauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
    config["TauTauTriggerWeightWorkspaceWeightNames"] = [
        "0:triggerWeight",
        "1:triggerWeight"
    ]
    config["TauTauTriggerWeightWorkspaceObjectNames"] = [
        "0:t_genuine_MediumIso_tt_ratio,t_fake_MediumIso_tt_ratio",
        "1:t_genuine_MediumIso_tt_ratio,t_fake_MediumIso_tt_ratio"
    ]
    config["TauTauTriggerWeightWorkspaceObjectArguments"] = [
        "0:t_pt,t_dm",
        "1:t_pt,t_dm"
    ]
    config["VBFTauTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
    config["SaveVBFTauTauTriggerWeightAsOptionalOnly"] = True
    config["VBFTauTauTriggerWeightWorkspaceWeightNames"] = [
            "0:VBFTriggerTauMCEfficiencyWeight_TightMVA",
            "0:VBFTriggerTauMCPUREfficiencyWeight_TightMVA",
            "0:VBFTriggerTauMCEfficiencyWeight_TightMVA_CorrFact",
            "0:VBFTriggerTauMCPUREfficiencyWeight_TightMVA_CorrFact",
            "0:VBFTriggerTauDataEfficiencyWeight_TightMVA",
            "1:VBFTriggerTauMCEfficiencyWeight_TightMVA",
            "1:VBFTriggerTauMCPUREfficiencyWeight_TightMVA",
            "1:VBFTriggerTauMCEfficiencyWeight_TightMVA_CorrFact",
            "1:VBFTriggerTauMCPUREfficiencyWeight_TightMVA_CorrFact",
            "1:VBFTriggerTauDataEfficiencyWeight_TightMVA",
            "0:VBFTriggerTauMCEfficiencyWeight_VLooseMVA",
            "0:VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA",
            "0:VBFTriggerTauMCEfficiencyWeight_VLooseMVA_CorrFact",
            "0:VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_CorrFact",
            "0:VBFTriggerTauDataEfficiencyWeight_VLooseMVA",
            "1:VBFTriggerTauMCEfficiencyWeight_VLooseMVA",
            "1:VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA",
            "1:VBFTriggerTauMCEfficiencyWeight_VLooseMVA_CorrFact",
            "1:VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_CorrFact",
            "1:VBFTriggerTauDataEfficiencyWeight_VLooseMVA",
            ]
    config["VBFTauTauTriggerWeightWorkspaceObjectNames"] = [
            "0:t_trgvbf_mva_tight_mc",
            "0:t_trgvbf_mva_tight_mcpur",
            "0:t_trgvbf_mva_tight_mc_corrFact",
            "0:t_trgvbf_mva_tight_mc_corrFact_pur",
            "0:t_trgvbf_mva_tight_data",
            "1:t_trgvbf_mva_tight_mc",
            "1:t_trgvbf_mva_tight_mcpur",
            "1:t_trgvbf_mva_tight_mc_corrFact",
            "1:t_trgvbf_mva_tight_mc_corrFact_pur",
            "1:t_trgvbf_mva_tight_data",
            "0:t_trgvbf_mva_vloose_mc",
            "0:t_trgvbf_mva_vloose_mcpur",
            "0:t_trgvbf_mva_vloose_mc_corrFact",
            "0:t_trgvbf_mva_vloose_mc_corrFact_pur",
            "0:t_trgvbf_mva_vloose_data",
            "1:t_trgvbf_mva_vloose_mc",
            "1:t_trgvbf_mva_vloose_mcpur",
            "1:t_trgvbf_mva_vloose_mc_corrFact",
            "1:t_trgvbf_mva_vloose_mc_corrFact_pur",
            "1:t_trgvbf_mva_vloose_data",
            ]
    config["VBFTauTauTriggerWeightWorkspaceObjectArguments"] = [
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "0:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            "1:t_pt",
            ]
    config["VBFJetTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
    config["SaveVBFJetTriggerWeightAsOptionalOnly"] = True
    config["VBFJetTriggerWeightWorkspaceWeightNames"] = [
            "0:VBFTriggerJetMCEfficiencyWeight_mjj",
            "0:VBFTriggerJetMCEfficiencyWeight_leadpt",
            "0:VBFTriggerJetMCEfficiencyWeight_trailpt",
            "0:VBFTriggerJetMCEfficiencyWeight_mjj_leadpt",
            "0:VBFTriggerJetMCEfficiencyWeight_mjj_trailpt",
            "0:VBFTriggerJetMCEfficiencyWeight_leadpt_trailpt",
            "0:VBFTriggerJetDataEfficiencyWeight_mjj",
            "0:VBFTriggerJetDataEfficiencyWeight_leadpt",
            "0:VBFTriggerJetDataEfficiencyWeight_trailpt",
            "0:VBFTriggerJetDataEfficiencyWeight_mjj_leadpt",
            "0:VBFTriggerJetDataEfficiencyWeight_mjj_trailpt",
            "0:VBFTriggerJetDataEfficiencyWeight_leadpt_trailpt",
            ]
    config["VBFJetTriggerWeightWorkspaceObjectNames"] = [
            "0:j_trgvbf_1d_mjj_mc",
            "0:j_trgvbf_1d_leadpt_mc",
            "0:j_trgvbf_1d_trailpt_mc",
            "0:j_trgvbf_2d_mjj_leadpt_mc",
            "0:j_trgvbf_2d_mjj_trailpt_mc",
            "0:j_trgvbf_2d_leadpt_trailpt_mc",
            "0:j_trgvbf_1d_mjj_data",
            "0:j_trgvbf_1d_leadpt_data",
            "0:j_trgvbf_1d_trailpt_data",
            "0:j_trgvbf_2d_mjj_leadpt_data",
            "0:j_trgvbf_2d_mjj_trailpt_data",
            "0:j_trgvbf_2d_leadpt_trailpt_data",
            ]
    config["VBFJetTriggerWeightWorkspaceObjectArguments"] = [
            "0:j_mjj",
            "0:j_pt1",
            "0:j_pt2",
            "0:j_mjj,j_pt1",
            "0:j_mjj,j_pt2",
            "0:j_pt1,j_pt2",
            "0:j_mjj",
            "0:j_pt1",
            "0:j_pt2",
            "0:j_mjj,j_pt1",
            "0:j_mjj,j_pt2",
            "0:j_pt1,j_pt2",
            ]
    config["SingleTauTriggerWeightWorkspace"] = "$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/scaleFactorWeights/htt_scalefactors_v16_5.root"
    config["SaveSingleTauTriggerWeightAsOptionalOnly"] = True
    config["SingleTauTriggerWeightWorkspaceWeightNames"] = [
            "0:SingleTauMCEfficiencyWeightJetFakes_TightMVA",
            "1:SingleTauMCEfficiencyWeightJetFakes_TightMVA",
            "0:SingleTauDataEfficiencyWeightJetFakes_TightMVA",
            "1:SingleTauDataEfficiencyWeightJetFakes_TightMVA",
            "0:SingleTauMCEfficiencyWeightElectronFakes_TightMVA",
            "1:SingleTauMCEfficiencyWeightElectronFakes_TightMVA",
            "0:SingleTauDataEfficiencyWeightElectronFakes_TightMVA",
            "1:SingleTauDataEfficiencyWeightElectronetFakes_TightMVA",
            "0:SingleTauMCEfficiencyWeightGenuineTau_TightMVA",
            "1:SingleTauMCEfficiencyWeightGenuineTau_TightMVA",
            "0:SingleTauMCEfficiencyWeightGenuineTauZprimeOrSUSYH_TightMVA",
            "1:SingleTauMCEfficiencyWeightGenuineTauZprimeOrSUSYH_TightMVA",
            ]
    config["SingleTauTriggerWeightWorkspaceObjectNames"] = [
            "0:t_trgsingletau_jetfakes_mc",
            "1:t_trgsingletau_jetfakes_mc",
            "0:t_trgsingletau_jetfakes_data",
            "1:t_trgsingletau_jetfakes_data",
            "0:t_trgsingletau_efakes_mc",
            "1:t_trgsingletau_efakes_mc",
            "0:t_trgsingletau_efakes_data",
            "1:t_trgsingletau_efakes_data",
            "0:t_trgsingletau_genuinetau_mc",
            "0:t_trgsingletau_genuinetau_mc",
            "1:t_trgsingletau_genuinetau_zprimesusyh_mc",
            "1:t_trgsingletau_genuinetau_zprimesusyh_mc",
            ]
    config["SingleTauTriggerWeightWorkspaceObjectArguments"] = [
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            "0:t_pt,t_dm",
            "1:t_pt,t_dm",
            ]

  config["FakeFaktorFiles"] = [
      "inclusive:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/medium/tt/inclusive/fakeFactors_20170628_medium.root",
      "nobtag:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/medium/tt/nobtag/fakeFactors_20170628_medium.root",
      "btag:$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/root/fakeFactorWeights/medium/tt/btag/fakeFactors_20170628_medium.root"
  ]

  config["TauTauRestFrameReco"] = "collinear_approximation"
  if isEmbedded:
    config["TauTriggerFilterNames"] = [
            "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoubleL2IsoTau26eta2p2",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
      ]
  else:
    config["TauTriggerFilterNames"] = [
            "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau35TrackPt1TightChargedIsolationAndTightOOSCPhotonsDz02Reg",
            "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v:hltDoublePFTau40TrackPt1MediumChargedIsolationAndTightOOSCPhotonsDz02Reg",
            "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v:hltDoublePFTau40TrackPt1TightChargedIsolationDz02Reg",
            "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:hltDoublePFTau20TrackPt1LooseChargedIsolationReg",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltPFTau180TrackPt50LooseAbsOrRelMediumHighPtRelaxedIsoIso",
            "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v:hltSelectedPFTau180MediumChargedIsolationL1HLTMatched"
    ]
    config["JetTriggerFilterNames"] = [
            "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:hltMatchedVBFTwoPFJets2CrossCleanedFromDoubleLooseChargedIsoPFTau20",
            "HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v:hltMatchedVBFOnePFJet2CrossCleanedFromDoubleLooseChargedIsoPFTau20",
    ]
  config["TauTriggerCheckL1Match"] = [
          "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg_v",
          "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg_v",
          "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg_v"
    ]

  config["InvalidateNonMatchingElectrons"] = False
  config["InvalidateNonMatchingMuons"] = False
  config["InvalidateNonMatchingTaus"] = False
  config["InvalidateNonMatchingJets"] = False
  config["DirectIso"] = True

  config["Quantities"] = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.syncQuantities").build_list(minimal_setup=minimal_setup)
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Includes.weightQuantities").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.lheWeights").build_list())
  config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.zptQuantities").build_list())
  #config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.fakeFactorWeightQuantities_tt").build_list())
  config["Quantities"].extend([
      "had_gen_match_pT_1",
      "had_gen_match_pT_2",
      "flagMETFilter",
      "pt_ttjj"
  ])
  if isEmbedded:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.Includes.embeddedDecayModeWeightQuantities").build_list())
    config["Quantities"].extend([
          "muonEffTrgWeight", "muonEffIDWeight_1","muonEffIDWeight_2", "doubleTauTrgWeight"
          ])
  elif not isData:
      # VBF and Single Tau trigger weights
      config["Quantities"].extend([
          "VBFTriggerTauMCEfficiencyWeight_TightMVA_1", "VBFTriggerTauMCEfficiencyWeight_TightMVA_2",
          "VBFTriggerTauMCPUREfficiencyWeight_TightMVA_1", "VBFTriggerTauMCPUREfficiencyWeight_TightMVA_2",
          "VBFTriggerTauMCEfficiencyWeight_TightMVA_CorrFact_1", "VBFTriggerTauMCEfficiencyWeight_TightMVA_CorrFact_2",
          "VBFTriggerTauMCPUREfficiencyWeight_TightMVA_CorrFact_1", "VBFTriggerTauMCPUREfficiencyWeight_TightMVA_CorrFact_2",
          "VBFTriggerTauDataEfficiencyWeight_TightMVA_1", "VBFTriggerTauDataEfficiencyWeight_TightMVA_2",
          "VBFTriggerTauMCEfficiencyWeight_VLooseMVA_1", "VBFTriggerTauMCEfficiencyWeight_VLooseMVA_2",
          "VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_1", "VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_2",
          "VBFTriggerTauMCEfficiencyWeight_VLooseMVA_CorrFact_1", "VBFTriggerTauMCEfficiencyWeight_VLooseMVA_CorrFact_2",
          "VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_CorrFact_1", "VBFTriggerTauMCPUREfficiencyWeight_VLooseMVA_CorrFact_2",
          "VBFTriggerTauDataEfficiencyWeight_VLooseMVA_1", "VBFTriggerTauDataEfficiencyWeight_VLooseMVA_2",
          "VBFTriggerJetMCEfficiencyWeight_mjj", "VBFTriggerJetMCEfficiencyWeight_leadpt", "VBFTriggerJetMCEfficiencyWeight_trailpt",
          "VBFTriggerJetMCEfficiencyWeight_mjj_leadpt", "VBFTriggerJetMCEfficiencyWeight_mjj_trailpt", "VBFTriggerJetMCEfficiencyWeight_leadpt_trailpt",
          "VBFTriggerJetDataEfficiencyWeight_mjj", "VBFTriggerJetDataEfficiencyWeight_leadpt", "VBFTriggerJetDataEfficiencyWeight_trailpt",
          "VBFTriggerJetDataEfficiencyWeight_mjj_leadpt", "VBFTriggerJetDataEfficiencyWeight_mjj_trailpt", "VBFTriggerJetDataEfficiencyWeight_leadpt_trailpt",
          "SingleTauMCEfficiencyWeightJetFakes_TightMVA_1", "SingleTauMCEfficiencyWeightJetFakes_TightMVA_2",
          "SingleTauDataEfficiencyWeightJetFakes_TightMVA_1", "SingleTauDataEfficiencyWeightJetFakes_TightMVA_2",
          "SingleTauMCEfficiencyWeightElectronFakes_TightMVA_1", "SingleTauMCEfficiencyWeightElectronFakes_TightMVA_2",
          "SingleTauDataEfficiencyWeightElectronFakes_TightMVA_1", "SingleTauDataEfficiencyWeightElectronetFakes_TightMVA_2",
          "SingleTauMCEfficiencyWeightGenuineTau_TightMVA_1", "SingleTauMCEfficiencyWeightGenuineTau_TightMVA_2",
          "SingleTauMCEfficiencyWeightGenuineTauZprimeOrSUSYH_TightMVA_1", "SingleTauMCEfficiencyWeightGenuineTauZprimeOrSUSYH_TightMVA_2",
      ])
  config["Quantities"].extend(["trg_doubletau_20_vbf", "trg_doubletau_20_vbf_jets", "trg_doubletau_20_vbf_vbfjets"])
  config["Quantities"].extend(["vbfmjj", "vbfjpt_1", "vbfjeta_1", "vbfjphi_1", "vbfjpt_2", "vbfjeta_2", "vbfjphi_2"])
  if re.search("HToTauTauM125", nickname):
    config["Quantities"].extend([
      "htxs_stage0cat",
      "htxs_stage1cat"
    ])
  if isGluonFusion:
    config["Quantities"].extend(importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2Analysis.Includes.ggHNNLOQuantities").build_list())

  config["OSChargeLeptons"] = True
  config["TopPtReweightingStrategy"] = "Run1"

  config["Processors"] = []
  #if not (isEmbedded):           config["Processors"].append( "producer:ElectronCorrectionsProducer")
  config["Processors"].extend((                               "producer:HttValidLooseElectronsProducer",
                                                              "producer:HttValidLooseMuonsProducer",
                                                              "producer:HltProducer",
                                                              "producer:MetSelector"))
  if not (isData): config["Processors"].append( "producer:TauCorrectionsProducer")
  if not isData:                 config["Processors"].append( "producer:HttValidGenTausProducer")
  config["Processors"].extend((                               "producer:ValidTausProducer",
                                                              "filter:ValidTausFilter",
                                                              "producer:TauTriggerMatchingProducer",
                                                              "filter:MinTausCountFilter",
                                                              "producer:ValidElectronsProducer",
                                                              "producer:ValidMuonsProducer",
                                                              #"producer:ValidTTPairCandidatesProducer",
                                                              "producer:NewValidTTPairCandidatesProducer",
                                                              "filter:ValidDiTauPairCandidatesFilter",
                                                              "producer:Run2DecayChannelProducer",
                                                              "producer:ValidTaggedJetsProducer",
                                                              "producer:JetTriggerMatchingProducer",
  #                                                            "producer:TaggedJetCorrectionsProducer",
                                                              ))
  if not (isData or isEmbedded): config["Processors"].append( "producer:GroupedJetUncertaintyShiftProducer")
  config["Processors"].append(                                "producer:ValidBTaggedJetsProducer")

  if btag_eff: config["ProcessorsBtagEff"] = copy.deepcp(config["Processors"])

  if not (isData or isEmbedded):  config["Processors"].append("producer:MetCorrector")
  config["Processors"].extend((                               "producer:SimpleEleTauFakeRateWeightProducer",
                                                              "producer:SimpleMuTauFakeRateWeightProducer"))
  #                                                            "producer:TauTauTriggerWeightProducer"))
  if isTTbar:                    config["Processors"].append( "producer:TopPtReweightingProducer")
  if isDY or isEmbedded:        config["Processors"].append( "producer:ZPtReweightProducer")
  config["Processors"].extend((                               "producer:TauTauRestFrameSelector",
                                                              "producer:DiLeptonQuantitiesProducer",
                                                              "producer:DiJetQuantitiesProducer",
                                                              "producer:VBFDiJetQuantitiesProducer",
                                                              "filter:MinimalPlotlevelFilter"))
  if isEmbedded:                 config["Processors"].append( "producer:EmbeddedWeightProducer")
  if isEmbedded:                 config["Processors"].append( "producer:TauDecayModeWeightProducer")
  if not isData:                 config["Processors"].append( "producer:TauTrigger2017EfficiencyProducer")
  if not (isEmbedded or isData): config["Processors"].extend(("producer:VBFTauTauTriggerWeightProducer",
                                                              "producer:VBFJetTriggerWeightProducer",
                                                              "producer:SingleTauTriggerWeightProducer",
                                                              ))
  config["Processors"].append(                                "producer:EventWeightProducer")
  if isGluonFusion:              config["Processors"].append( "producer:SMggHNNLOProducer")
  config["Processors"].append(                                "producer:SvfitProducer")

  config["AddGenMatchedTaus"] = True
  config["AddGenMatchedTauJets"] = True
  config["BranchGenMatchedTaus"] = True
  config["Consumers"] = ["KappaLambdaNtupleConsumer",
                         "cutflow_histogram"]

  if btag_eff:
     config["Processors"] = copy.deepcp(config["ProcessorsBtagEff"])

     btag_eff_unwanted = ["KappaLambdaNtupleConsumer", "CutFlowTreeConsumer", "KappaElectronsConsumer", "KappaTausConsumer", "KappaTaggedJetsConsumer", "RunTimeConsumer", "PrintEventsConsumer"]
     for unwanted in btag_eff_unwanted:
      if unwanted in config["Consumers"]: config["Consumers"].remove(unwanted)

     config["Consumers"].append("BTagEffConsumer")

  # pipelines - systematic shifts
  return ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.nominal").build_config(nickname)) # + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.tauESperDM_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.JECunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.regionalJECunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.METunc_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.METrecoil_shifts").build_config(nickname)) + \
         ACU.apply_uncertainty_shift_configs('tt', config, importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.btagging_shifts").build_config(nickname))

