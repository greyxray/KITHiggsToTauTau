#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

def build_list():
  quantities_list = [
    "nickname",
    "input",
    "run",
    "lumi",
    "event",
    "evt",
    "npv",
    "npu",
    "rho",
    #"mcweight",
    "puweight",
    "idweight_1",
    "idweight_2",
    "isoweight_1",
    "isoweight_2",
    #"effweight",
    "weight",
    #"embeddedWeight",
    "m_vis",
    "H_mass",
    "H_pt",
    "diLepMass",
    "diLepMassSmearUp",
    "diLepMassSmearDown",
    "diLepGenMass",
    "diLepMetMt",
    "pt_1",
    "phi_1",
    "eta_1",
    "m_1",
    "q_1",
    "iso_1",
    #"mva_1",
    "d0_1",
    "dZ_1",
    #"passid_1",
    #"passiso_1",
    "mt_1",
    "pt_2",
    "phi_2",
    "eta_2",
    "m_2",
    "q_2",
    "iso_2",
    "d0_2",
    "dZ_2",
    #"mva_2",
    #"passid_2",
    #"passiso_2",
    "mt_2",
    "met",
    "metphi",
    #"l1met",
    #"l1metphi",
    #"l1metcorr",
    #"calomet",
    #"calometphi",
    #"calometcorr",
    #"calometphicorr",
    "mvamet",
    "mvametphi",
    "pzetavis",
    "pzetamiss",
    "pZetaMissVis",
    "metcov00",
    "metcov01",
    "metcov10",
    "metcov11",
    "mvacov00",
    "mvacov01",
    "mvacov10",
    "mvacov11",
    "jpt_1",
    "jeta_1",
    "jphi_1",
    "jm_1",
    "jrawf_1",
    "jmva_1",
    "jpfid_1",
    "jpuid_1",
    "jcsv_1",
    "bpt_1",
    "beta_1",
    "bphi_1",
    "brawf_1",
    "bmva_1",
    "bpfid_1",
    "bpuid_1",
    "bcsv_1",
    "jpt_2",
    "jeta_2",
    "jphi_2",
    "jm_2",
    "jrawf_2",
    "jmva_2",
    "jpfid_2",
    "jpuid_2",
    "jcsv_2",
    "bpt_2",
    "beta_2",
    "bphi_2",
    "brawf_2",
    "bmva_2",
    "bpfid_2",
    "bpuid_2",
    "bcsv_2",
    "mjj",
    "jdeta",
    "njetingap",
    "njetingap20",
    "jdphi",
    "dijetpt",
    "dijetphi",
    "hdijetphi",
    "visjeteta",
    "ptvis",
    "nbtag",
    "njets",
    "njetspt20",
    "njetspt30",
    #"mva_gf",
    #"mva_vbf",
    "trigweight_1",
    "chargedIsoPtSum_1",
    "neutralIsoPtSum_1",
    "puCorrPtSum_1",
    "footprintCorrection_1",
    "photonPtSumOutsideSignalCone_1",
    "againstMuonLoose3_1", "againstMuonTight3_1",
    "againstElectronLooseMVA6_1", "againstElectronMediumMVA6_1", "againstElectronTightMVA6_1",
    "againstElectronVLooseMVA6_1", "againstElectronVTightMVA6_1",
    "byCombinedIsolationDeltaBetaCorrRaw3Hits_1",
    "byLooseCombinedIsolationDeltaBetaCorr3Hits_1", "byMediumCombinedIsolationDeltaBetaCorr3Hits_1",
    "byTightCombinedIsolationDeltaBetaCorr3Hits_1", "byIsolationMVArun2v1DBoldDMwLTraw_1", "byVLooseIsolationMVArun2v1DBoldDMwLT_1",
    "byLooseIsolationMVArun2v1DBoldDMwLT_1", "byMediumIsolationMVArun2v1DBoldDMwLT_1", "byTightIsolationMVArun2v1DBoldDMwLT_1",
    "byVTightIsolationMVArun2v1DBoldDMwLT_1", "byVVTightIsolationMVArun2v1DBoldDMwLT_1", "rerunDiscriminationByIsolationMVAOldDMrun2v1raw_1",
    "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_1", "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_1", "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_1",
    "rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_1", "rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_1", "rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_1",
    "decayModeFinding_1", "decayModeFindingNewDMs_1",
    "trigweight_2",
    "chargedIsoPtSum_2",
    "neutralIsoPtSum_2",
    "puCorrPtSum_2",
    "footprintCorrection_2",
    "photonPtSumOutsideSignalCone_2",
    "againstMuonLoose3_2", "againstMuonTight3_2",
    "againstElectronLooseMVA6_2", "againstElectronMediumMVA6_2", "againstElectronTightMVA6_2",
    "againstElectronVLooseMVA6_2", "againstElectronVTightMVA6_2",
    "byCombinedIsolationDeltaBetaCorrRaw3Hits_2",
    "byLooseCombinedIsolationDeltaBetaCorr3Hits_2", "byMediumCombinedIsolationDeltaBetaCorr3Hits_2",
    "byTightCombinedIsolationDeltaBetaCorr3Hits_2", "byIsolationMVArun2v1DBoldDMwLTraw_2", "byVLooseIsolationMVArun2v1DBoldDMwLT_2",
    "byLooseIsolationMVArun2v1DBoldDMwLT_2", "byMediumIsolationMVArun2v1DBoldDMwLT_2", "byTightIsolationMVArun2v1DBoldDMwLT_2",
    "byVTightIsolationMVArun2v1DBoldDMwLT_2", "byVVTightIsolationMVArun2v1DBoldDMwLT_2", "rerunDiscriminationByIsolationMVAOldDMrun2v1raw_2",
    "rerunDiscriminationByIsolationMVAOldDMrun2v1VLoose_2", "rerunDiscriminationByIsolationMVAOldDMrun2v1Loose_2", "rerunDiscriminationByIsolationMVAOldDMrun2v1Medium_2",
    "rerunDiscriminationByIsolationMVAOldDMrun2v1Tight_2", "rerunDiscriminationByIsolationMVAOldDMrun2v1VTight_2", "rerunDiscriminationByIsolationMVAOldDMrun2v1VVTight_2",
    "decayModeFinding_2", "decayModeFindingNewDMs_2",
    "isFake",
    "NUP",
    "id_m_loose_1",
    "id_m_medium_1",
    "id_m_tight_1",
    "id_m_highpt_1",
    "id_e_mva_nt_loose_1",
    "id_e_cut_veto_1",
    "id_e_cut_loose_1",
    "id_e_cut_medium_1",
    "id_e_cut_tight_1",
    "pt_tt",
    "dilepton_veto",
    "extraelec_veto",
    "extramuon_veto",
    "gen_match_1",
    "gen_match_2",
    "decayMode_1",
    "decayMode_2",
    "npartons",
    "genbosonmass",
    "leadingJetGenMatch",
    "trailingJetGenMatch"
  ]
  
  return quantities_list
