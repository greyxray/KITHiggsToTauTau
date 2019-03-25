#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.jsonTools as jsonTools
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)
import Kappa.Skimming.datasetsHelperTwopz as datasetsHelperTwopz

import re
import os
import importlib


def fshift_dict(shift=None, dm=None):
    if shift is None or dm is None:
        print "fshift_dict received wrong parameters"
        exit(1)
    config = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.nominal").build_config(nickname="pass")["nominal"]
    config[dm] = 1 + shift / 100.
    return config


def fshift_dict(shifts=None):
    if not isinstance(shifts, dict):
        print "fshift_dict received wrong parameters"
        exit(1)
    config = importlib.import_module("HiggsAnalysis.KITHiggsToTauTau.data.ArtusConfigs.Run2MSSM2017.nominal").build_config(nickname="pass")["nominal"]
    for variable, shift in shifts.iteritems():
        config[variable] = 1 + shift / 100.
    return config


def build_config(nickname, **kwargs):
    """Produce shifts for e->tau FR ES measurements"""
    # TODO : now it is 1 shift. Need to implement 2 shifts.
    log.debug("Produce shifts for tau ES measurements")
    tau_es_method = kwargs["tau_es_method"] if "tau_es_method" in kwargs else 'classical'  # classical, gamma
    tau_es_group = kwargs["tau_es_group"] if "tau_es_group" in kwargs else None
    tau_es_charged = kwargs["tau_es_charged"] if "tau_es_charged" in kwargs else None
    tau_es_neutral = kwargs["tau_es_neutral"] if "tau_es_neutral" in kwargs else None

    root_str = lambda x: str(x).replace("-", "neg").replace(".", "p")

    config = jsonTools.JsonDict()
    datasetsHelper = datasetsHelperTwopz.datasetsHelperTwopz(os.path.expandvars("$CMSSW_BASE/src/Kappa/Skimming/data/datasets.json"))

    # define frequently used conditions
    isEmbedded = datasetsHelper.isEmbedded(nickname)
    isDY = re.search("DY.?JetsToLLM", nickname)
    isEWKZ2Jets = re.search("EWKZ2Jets", nickname)

    if tau_es_method is 'classical':
        tau_es_shifts_groups = [
            [-6 + i * 0.2 for i in range(0, 10)],
            [-4 + i * 0.2 for i in range(0, 10)],
            [-2 + i * 0.2 for i in range(0, 10)],
            [0.2 + i * 0.2 for i in range(0, 10)],
            [2.2 + i * 0.2 for i in range(0, 10)],
            [4.2 + i * 0.2 for i in range(0, 10)],
            [0],
            [-4, -2, 2, 4],
        ]
        if isinstance(tau_es_group, int) and abs(tau_es_group) < len(tau_es_shifts_groups):
            tau_es_shifts = tau_es_shifts_groups[tau_es_group]
            print "TES:", tau_es_shifts
        else:
            print "TES shifts not properly specified -> skipping. tau_es_shifts_groups :", tau_es_shifts_groups
            return

        # Pipelines for producing shapes for calculating the TauElectronFakeEnergyCorrection*
        if isDY or isEWKZ2Jets or isEmbedded:

            for es in tau_es_shifts:
                config["tauTauEsInclusiveShift_" + root_str(es)] = fshift_dict(es, "TauEnergyCorrectionShift")
                config["tauTauEsOneProngShift_" + root_str(es)] = fshift_dict(es, "TauEnergyCorrectionOneProngShift")
                config["tauTauEsOneProngPiZerosShift_" + root_str(es)] = fshift_dict(es, "TauEnergyCorrectionOneProngPiZerosShift")
                config["tauTauEsThreeProngShift_" + root_str(es)] = fshift_dict(es, "TauEnergyCorrectionThreeProngShift")

    elif tau_es_method == 'gamma':
        # expect: +0.2% ES for neutral and -1% for charged -> will vary neural component only between +-2% -> 21 option
        # therefore : tau_es_group in [0; 83] = [0; (21-1) * len(tau_es_shifts_charged_groups) + (len(tau_es_shifts_charged_groups) - 1) ]

        # Pipelines for producing shapes for calculating the TauElectronFakeEnergyCorrection*
        if isDY or isEWKZ2Jets or isEmbedded:
            for c in tau_es_charged:
                for n in tau_es_neutral:
                    print 'charged:', c, 'neutral:', n
                    config["tauTauEsOneProngPiZerosShift_ch" + root_str(c) + "_nt" + root_str(n)] = fshift_dict(
                        {
                            "TauEnergyCorrectionOneProngPiZerosCHShift": c,
                            "TauEnergyCorrectionOneProngPiZerosNTShift": n,
                        }
                    )

                    # if n == 0:
                    #     config["tauTauEsOneProngShift_ch" + root_str(c) + "_nt" + root_str(n)] = fshift_dict(
                    #         {
                    #             "TauEnergyCorrectionOneProngCHShift": c,
                    #             "TauEnergyCorrectionOneProngNTShift": n,
                    #         }
                    #     )
                    #     config["tauTauEsThreeProngShift_ch" + root_str(c) + "_nt" + root_str(n)] = fshift_dict(
                    #         {
                    #             "TauEnergyCorrectionThreeProngCHShift": c,
                    #             "TauEnergyCorrectionThreeProngNTShift": n,
                    #         }
                    #     )
    elif tau_es_method == 'gamma_shapes':
        pass  # the variation is postponed to shapes-production step

    return config
