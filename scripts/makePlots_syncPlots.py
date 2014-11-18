#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import argparse
import os

import HiggsAnalysis.KITHiggsToTauTau.plotting.higgsplot as higgsplot


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Make sync plots.",
	                                 parents=[logger.loggingParser])

	parser.add_argument("--input-1", help="Input files 1.", required=True)
	parser.add_argument("--input-2", help="Input files 2.", required=True)
	
	parser.add_argument("--folder-1", help="Input folders 1.", required=True)
	parser.add_argument("--folder-2", help="Input folders 2.", required=True)
	
	parser.add_argument("--label-1", default="1", help="Label 1 [Default: %(default)s].")
	parser.add_argument("--label-2", default="2", help="Label 2 [Default: %(default)s].")
	
	parser.add_argument("--channel", help="Channel", required=True)
	parser.add_argument("--quantities", nargs="*",
	                    default=["inclusive", "eventsoverlap",
	                             "pt_1", "eta_1", "phi_1", "m_1", "iso_1",
	                             "pt_2", "eta_2", "phi_2", "m_2", "iso_2",
	                             "mvis", "pt_sv", "eta_sv", "phi_sv", "m_sv",
	                             "met", "metphi", "metcov00", "metcov01", "metcov10", "metcov11",
	                             "mvamet", "mvametphi", "mvacov00", "mvacov01", "mvacov10", "mvacov11",
	                             "jpt_1", "jeta_1", "jphi_1",
	                             "jpt_2", "jeta_2", "jphi_2",
	                             "njets", "mjj", "jdeta",
	                             "trigweight_1", "trigweight_2", "puweight",
	                             "npv", "npu", "rho"],
	                    help="Quantities. [Default: %(default)s]")
	parser.add_argument("-a", "--args", default="",
	                    help="Additional Arguments for HarryPlotter.")
	
	args = vars(parser.parse_args())
	logger.initLogger(args)
	
	failed_plots = []
	for quantity in args["quantities"]:
		json_exists = True
		json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_%s.json" % (args["channel"], quantity))
		if not os.path.exists(json_config):
			json_exists = False
			json_config = os.path.expandvars("$CMSSW_BASE/src/HiggsAnalysis/KITHiggsToTauTau/data/plots/configs/sync_exercise/%s_default.json" % args["channel"])
		
		plot_args = "--json-defaults %s -i %s %s --folders %s %s %s -f png --plot-modules PlotRootHtt %s %s" % (json_config, args["input_1"], args["input_2"], args["folder_1"], args["folder_2"], ("" if json_exists else ("-x %s" % quantity)), ("" if quantity != "eventsoverlap" else ("--analysis-modules EventSelectionOverlap")), args["args"])
		plot_args = os.path.expandvars(plot_args)
		
		log.info("\nhiggsplot.py %s" % plot_args)
		
		try:
			higgsplot.higgs_plot(plot_args)
		except Exception:
			failed_plots.append(plot_args)
	
	if len(plot_args) > 0:
		log.error("Failed plots:\n\thiggsplot.py %s" % "\n\thiggsplot.py ".join(plot_args))

