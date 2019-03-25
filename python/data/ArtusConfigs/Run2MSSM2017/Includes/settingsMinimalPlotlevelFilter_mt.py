#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import re
import json
import copy
import Artus.Utility.jsonTools as jsonTools
#import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz
import importlib
#import os

def build_config(nickname, **kwargs):
  tau_es = True if "sub_analysis" in kwargs and kwargs["sub_analysis"] == "tau-es" else False
  tau_es_method = kwargs["tau_es_method"] if "tau_es_method" in kwargs else 'classical'  # classical, gamma

  config = jsonTools.JsonDict()
  #datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

  config["PlotlevelFilterExpressionQuantities"] = [
    "flagMETFilter",
    "againstElectronVLooseMVA6_2",
    "extraelec_veto",
    "againstMuonTight3_2",
    "byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2",
  ]
  config["PlotlevelFilterExpression"] = "(flagMETFilter > 0.5)*(extraelec_veto < 0.5)*(againstMuonTight3_2 > 0.5)*(againstElectronVLooseMVA6_2 > 0.5)*(byVLooseIsolationMVArun2017v2DBoldDMwLT2017_2 > 0.5)"

  # as for the TES version of 2016
  if not tau_es:
    config["PlotlevelFilterExpressionQuantities"].append('nDiMuonVetoPairsOS')
    config["PlotlevelFilterExpression"] += '*(nDiMuonVetoPairsOS < 0.5)'

    config["PlotlevelFilterExpressionQuantities"].append("extramuon_veto")
    config["PlotlevelFilterExpression"] += '*(extramuon_veto < 0.5)'
  else:
    # version consistent with Izaak for 2017
    config["PlotlevelFilterExpressionQuantities"].append('nDiMuonVetoPairsOS')
    config["PlotlevelFilterExpression"] += '*(nDiMuonVetoPairsOS < 0.5)'

    # version for 2018 reprocessing
    config["PlotlevelFilterExpressionQuantities"].append("extramuon_veto")
    config["PlotlevelFilterExpression"] += '*(extramuon_veto < 0.5)'

    if tau_es_method == 'gamma':
      config["PlotlevelFilterExpressionQuantities"].append("decayMode_2")
      config["PlotlevelFilterExpression"] += '*(decayMode_2 > 0)*(decayMode_2 < 2)'  # selecting only DM1
    elif tau_es_method == 'gamma_shapes':
      pass  # the variation is postponed to shapes-production step

  return config
