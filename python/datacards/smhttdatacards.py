# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import HiggsAnalysis.KITHiggsToTauTau.plotting.configs.categories as Categories
import HiggsAnalysis.KITHiggsToTauTau.datacards.datacards as datacards
import CombineHarvester.CombineTools.ch as ch

class SMHttDatacards(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], useRateParam=False, year="", cb=None):
		super(SMHttDatacards, self).__init__(cb)

		if cb is None:
			signal_processes = ["ggH", "qqH", "WH", "ZH"]
			
			background_processes_mt = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_et = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_tt = ["ZTT", "ZL", "ZJ", "TTT", "TTJJ", "VVT", "VVJ", "W", "QCD"]
			background_processes_em = ["ZTT", "ZLL", "TT", "VV", "HWW_gg", "HWW_qq", "W", "QCD"]
			background_processes_mm = ["ZLL", "TT", "VV", "W"]
			
			all_mc_bkgs = ["ZTT", "ZL", "ZJ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "W", "HWW_gg", "HWW_qq"]
			all_mc_bkgs_no_W = ["ZTT", "ZL", "ZJ", "TT", "TTT", "TTJJ", "VV", "VVT", "VVJ", "HWW_gg", "HWW_qq"]

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=Categories.CategoriesDict().getCategories(["mt"])["mt"],
					bkg_processes=background_processes_mt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency2016_syst_args)
				self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["mt"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.muon_efficiency_syst_args)
				self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.muon_efficiency_syst_args)
				self.cb.cp().channel(["mt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency_syst_args)
				self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_efficiency_syst_args)

			# Tau ES
			self.cb.cp().channel(["mt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["mt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# mu->tau fake ES
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_ZLShape_mt_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, "CMS_ZLShape_mt_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))

			# mu->tau fake rate
			if year == "2016":
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(["mt_ZeroJet2D", "mt_Boosted2D", "mt_Vbf2D"]).AddSyst(self.cb, "CMS_mFakeTau_1prong_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["mt"]).process(["ZL"]).bin(["mt_ZeroJet2D", "mt_Boosted2D", "mt_Vbf2D"]).AddSyst(self.cb, "CMS_mFakeTau_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["mt"]).process(["ZL"]).AddSyst(self.cb, *self.muFakeTau_syst_args)
			
			# ttbar shape
			self.cb.cp().channel(["mt"]).process(["TTT", "TTJJ"]).AddSyst(self.cb, *self.ttj_syst_args)
			
			# dy shape
			self.cb.cp().channel(["mt"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.dy_shape_syst_args)
			
			# decay mode reweighting
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["mt"]).process(["ZTT"]).bin(["mt_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_3prong_13TeV", "shape", ch.SystMap()(1.0))
			
			if useRateParam:
				for category in Categories.CategoriesDict().getCategories(["mt"], False)["mt"]:
					self.cb.cp().channel(["mt"]).bin(["mt_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=Categories.CategoriesDict().getCategories(["et"])["et"],
					bkg_processes=background_processes_et,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency2016_syst_args)
				self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["et"]).process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.electron_efficiency_syst_args)
				self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.electron_efficiency_syst_args)
				self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency_syst_args)
				self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_efficiency_syst_args)

			# Tau ES
			self.cb.cp().channel(["et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["et"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# e->tau fake ES
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_ZLShape_et_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, "CMS_ZLShape_et_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))

			# e->tau fake rate
			if year == "2016":
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(["et_ZeroJet2D", "et_Boosted2D", "et_Vbf2D"]).AddSyst(self.cb, "CMS_eFakeTau_1prong_13TeV", "shape", ch.SystMap()(1.0))
				self.cb.cp().channel(["et"]).process(["ZL"]).bin(["et_ZeroJet2D", "et_Boosted2D", "et_Vbf2D"]).AddSyst(self.cb, "CMS_eFakeTau_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["et"]).process(["ZL"]).AddSyst(self.cb, *self.eFakeTau_tight_syst_args)
			
			# ttbar shape
			self.cb.cp().channel(["et"]).process(["TTT", "TTJJ"]).AddSyst(self.cb, *self.ttj_syst_args)
			
			# dy shape
			self.cb.cp().channel(["et"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.dy_shape_syst_args)
			
			# decay mode reweighting
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_1prong1pizero_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et"]).process(["ZTT"]).bin(["et_ZeroJet2D"]).AddSyst(self.cb, "CMS_tauDMReco_3prong_13TeV", "shape", ch.SystMap()(1.0))
			
			if useRateParam:
				for category in Categories.CategoriesDict().getCategories(["et"], False)["et"]:
					self.cb.cp().channel(["et"]).bin(["et_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=Categories.CategoriesDict().getCategories(["em"])["em"],
					bkg_processes=background_processes_em,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["em"]).process(all_mc_bkgs).AddSyst(self.cb, *self.trigger_efficiency2016_em_syst_args)
				self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.trigger_efficiency2016_em_syst_args)
				self.cb.cp().channel(["em"]).process(all_mc_bkgs).AddSyst(self.cb, *self.electron_efficiency2016_syst_args)
				self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.electron_efficiency2016_syst_args)

				self.cb.cp().channel(["em"]).process(all_mc_bkgs).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["em"]).process(all_mc_bkgs).AddSyst(self.cb, *self.electron_efficiency_syst_args)
				self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.electron_efficiency_syst_args)

				self.cb.cp().channel(["em"]).process(all_mc_bkgs).AddSyst(self.cb, *self.muon_efficiency_syst_args)
				self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.muon_efficiency_syst_args)

			# B-Tag
			if year == "2016":
				# the bins for zero jet, boosted and vbf are defined in datacardconfigs.py
				self.cb.cp().channel(["em"]).process(["TT"]).bin(["em_ZeroJet2D", "em_Boosted2D", "em_Vbf2D"]).AddSyst(self.cb, *self.btag_efficiency2016_syst_args)
				self.cb.cp().channel(["em"]).process(["VV"]).bin(["em_Boosted2D", "em_Vbf2D"]).AddSyst(self.cb, *self.btag_mistag2016_syst_args)
			
			# electron ES
			self.cb.cp().channel(["em"]).process(all_mc_bkgs+["QCD"]).AddSyst(self.cb, *self.ele_es_syst_args)
			self.cb.cp().channel(["em"]).signals().AddSyst(self.cb, *self.ele_es_syst_args)
			
			# ttbar shape
			self.cb.cp().channel(["em"]).process(["TT"]).AddSyst(self.cb, *self.ttj_syst_args)
			
			# dy shape
			self.cb.cp().channel(["em"]).process(["ZTT", "ZLL"]).AddSyst(self.cb, *self.dy_shape_syst_args)
			
			if useRateParam:
				for category in Categories.CategoriesDict().getCategories(["em"], False)["em"]:
					self.cb.cp().channel(["em"]).bin(["em_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=Categories.CategoriesDict().getCategories(["tt"])["tt"],
					bkg_processes=background_processes_tt,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# efficiencies
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["tt"]).process(all_mc_bkgs).AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.trigger_efficiency2016_syst_args)
				self.cb.cp().channel(["tt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency2016_tt_syst_args)
				self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficiency2016_tt_syst_args)
			else:
				self.cb.cp().channel(["tt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency_syst_args)
				self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficiency_syst_args)

			# Tau ES
			self.cb.cp().channel(["tt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_es_syst_args)
			self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_es_syst_args)

			# ttbar shape
			self.cb.cp().channel(["tt"]).process(["TTT", "TTJJ"]).AddSyst(self.cb, *self.ttj_syst_args)
			
			# dy shape
			self.cb.cp().channel(["tt"]).process(["ZTT", "ZL", "ZJ"]).AddSyst(self.cb, *self.dy_shape_syst_args)
			
			if useRateParam:
				for category in Categories.CategoriesDict().getCategories(["tt"], False)["tt"]:
					self.cb.cp().channel(["tt"]).bin(["tt_"+category]).process(["ZTT"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))
			
			# ======================================================================
			# MM channel
			self.add_processes(
					channel="mm",
					categories=Categories.CategoriesDict().getCategories(["mm"])["mm"],
					bkg_processes=background_processes_mm,
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)
			
			# efficiencies
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["mm"]).process(all_mc_bkgs).AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
				self.cb.cp().channel(["mm"]).signals().AddSyst(self.cb, *self.muon_efficiency2016_syst_args)
			else:
				self.cb.cp().channel(["mm"]).process(all_mc_bkgs).AddSyst(self.cb, *self.muon_efficiency_syst_args)
				self.cb.cp().channel(["mm"]).signals().AddSyst(self.cb, *self.muon_efficiency_syst_args)
			
			if useRateParam:
				for category in Categories.CategoriesDict().getCategories(["mm"], False)["mm"]:
					self.cb.cp().channel(["mm"]).bin(["mm_"+category]).process(["ZLL"]).AddSyst(self.cb, "n_zll_"+category+"_norm", "rateParam", ch.SystMap()(1.0))

			# ======================================================================
			# All channels

			# lumi
			# (hopefully) temporary fix
			# TODO: update processes once MM and TT fits are implemented
			if year == "2016":
				self.cb.cp().signals().AddSyst(self.cb, *self.lumi2016_syst_args)
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.lumi2016_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm"]).AddSyst(self.cb, *self.lumi2016_syst_args) # automatically in other channels determined
			else:
				self.cb.cp().signals().AddSyst(self.cb, *self.lumi_syst_args)
				self.cb.cp().process(all_mc_bkgs_no_W).AddSyst(self.cb, *self.lumi_syst_args)
				self.cb.cp().process(["W"]).channel(["em", "tt", "mm"]).AddSyst(self.cb, *self.lumi_syst_args) # automatically in other channels determined

			# jets
			self.cb.cp().process(all_mc_bkgs+["QCD"]).AddSyst(self.cb, *self.jec_syst_args)
			self.cb.cp().signals().AddSyst(self.cb, *self.jec_syst_args)
			
			# fakes
			if year == "2016":
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "TTJJ", "VVJ"]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
				# TODO: add control regions for W+jets once implemented
				self.cb.cp().channel(["et", "mt", "tt"]).process(["W"]).bin([channel+"_"+category for channel in ["et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_htt_jetToTauFake_13TeV", "shape", ch.SystMap()(1.0))
			else:
				self.cb.cp().channel(["et", "mt", "tt"]).process(["ZJ", "W", "TTJJ", "VVJ"]).AddSyst(self.cb, *self.jetFakeTau_syst_args)
			
			# MET
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["em", "et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt", "tt", "em"]).signals().bin([channel+"_"+category for channel in ["em", "et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_clustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt", "tt", "em"]).process(all_mc_bkgs).bin([channel+"_"+category for channel in ["em", "et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().channel(["et", "mt", "tt", "em"]).signals().bin([channel+"_"+category for channel in ["em", "et", "mt", "tt"] for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "CMS_scale_met_unclustered_13TeV", "shape", ch.SystMap()(1.0))

			# cross section
			self.cb.cp().process(["ZTT", "ZL", "ZJ", "ZLL"]).AddSyst(self.cb, *self.ztt_cross_section_syst_args)
			self.cb.cp().process(["TTT", "TTJJ"]).channel(["mt", "et", "tt"]).AddSyst(self.cb, *self.ttj_cross_section_syst_args) # automatically in other channels determined
			if year == "2016":
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *self.vv_cross_section2016_syst_args)
			else:
				self.cb.cp().process(["VV", "VVT", "VVJ"]).AddSyst(self.cb, *self.vv_cross_section_syst_args)
			self.cb.cp().process(["W"]).channel(["em"]).AddSyst(self.cb, "CMS_htt_jetFakeLep_13TeV", "lnN", ch.SystMap()(1.20)) # automatically in other channels determined
			self.cb.cp().process(["W"]).channel(["tt", "mm"]).AddSyst(self.cb, *self.wj_cross_section_syst_args)
			
			# QCD normalization from https://github.com/cms-analysis/CombineHarvester/blob/SM2016-dev/HTTSM2016/src/HttSystematics_SMRun2.cc#L1393-L1415
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_em_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Boosted2D"]).AddSyst(self.cb, "CMS_htt_QCD_boosted_em_13TeV", "lnN", ch.SystMap()(1.10))
			self.cb.cp().channel(["em"]).process(["QCD"]).bin(["em_Vbf2D"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_em_13TeV", "lnN", ch.SystMap()(1.20))
			
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_ZeroJet2D"]).AddSyst(self.cb, "CMS_htt_QCD_0jet_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Boosted2D"]).AddSyst(self.cb, "CMS_htt_QCD_boosted_tt_13TeV", "lnN", ch.SystMap()(1.027))
			self.cb.cp().channel(["tt"]).process(["QCD"]).bin(["tt_Vbf2D"]).AddSyst(self.cb, "CMS_htt_QCD_VBF_tt_13TeV", "lnN", ch.SystMap()(1.15))
			
			self.cb.cp().channel(["mt"]).process(["QCD"]).bin(["mt_"+category for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_mt_13TeV", "lnN", ch.SystMap()(1.20))
			self.cb.cp().channel(["et"]).process(["QCD"]).bin(["et_"+category for category in ["ZeroJet2D", "Boosted2D", "Vbf2D"]]).AddSyst(self.cb, "QCD_Extrap_Iso_nonIso_et_13TeV", "lnN", ch.SystMap()(1.20))

			# tau efficiency
			# (hopefully) temporary fix
			if year == "2016":
				self.cb.cp().channel(["mt", "et"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency2016_corr_syst_args)
				self.cb.cp().channel(["tt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency2016_tt_corr_syst_args)
				self.cb.cp().channel(["mt", "et"]).signals().AddSyst(self.cb, *self.tau_efficiency2016_corr_syst_args)
				self.cb.cp().channel(["tt"]).signals().AddSyst(self.cb, *self.tau_efficiency2016_tt_corr_syst_args)
			else:
				self.cb.cp().channel(["mt", "et", "tt"]).process(["ZTT", "TTT", "VVT"]).AddSyst(self.cb, *self.tau_efficiency_corr_syst_args)
				self.cb.cp().channel(["mt", "et", "tt"]).signals().AddSyst(self.cb, *self.tau_efficiency_corr_syst_args)
			
			# ======================================================================
			# Theory uncertainties
			# TODO: implement shape uncertainty in systematics_run2.py
			#self.cb.cp().channel(["mt", "et", "tt", "em"]).process(["qqH"]).AddSyst(self.cb, "CMS_scale_gg_13TeV", "shape", ch.SystMap()(1.0))
			self.cb.cp().process(["qqH"]).AddSyst(self.cb, *self.htt_qcd_scale_qqh_syst_args)
			self.cb.cp().process(["ggH", "qqH"]).AddSyst(self.cb, *self.htt_pdf_scale_smhtt_syst_args)
			self.cb.cp().process(["ggH", "qqH"]).AddSyst(self.cb, *self.htt_ueps_smhtt_syst_args)
			
			# Uncertainty on BR of HTT @ 125 GeV
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_THU", "lnN", ch.SystMap()(1.017))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().signals().AddSyst(self.cb, "BR_htt_PU_alphas", "lnN", ch.SystMap()(1.0062))
			
			# Uncertainty on BR of HWW @ 125 GeV
			self.cb.cp().process(["HWW_gg", "HWW_qq"]).AddSyst(self.cb, "BR_hww_THU", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["HWW_gg", "HWW_qq"]).AddSyst(self.cb, "BR_hww_PU_mq", "lnN", ch.SystMap()(1.0099))
			self.cb.cp().process(["HWW_gg", "HWW_qq"]).AddSyst(self.cb, "BR_hww_PU_alphas", "lnN", ch.SystMap()(1.0066))
			
			self.cb.cp().process(["ggH", "HWW_gg"]).AddSyst(self.cb, "QCDScale_ggH", "lnN", ch.SystMap()(1.039))
			self.cb.cp().process(["qqH", "HWW_qq"]).AddSyst(self.cb, "QCDScale_qqH", "lnN", ch.SystMap()(1.004))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.007))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "QCDScale_VH", "lnN", ch.SystMap()(1.038))
			
			self.cb.cp().process(["ggH", "HWW_gg"]).AddSyst(self.cb, "pdf_Higgs_gg", "lnN", ch.SystMap()(1.032))
			self.cb.cp().process(["qqH", "HWW_qq"]).AddSyst(self.cb, "pdf_Higgs_qq", "lnN", ch.SystMap()(1.021))
			self.cb.cp().process(["WH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.019))
			self.cb.cp().process(["ZH"]).AddSyst(self.cb, "pdf_Higgs_VH", "lnN", ch.SystMap()(1.016))
			
			# ======================================================================

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()


# simplified version just for the purpose of datacard synchronization (no systematics)
class SMHttDatacardsForSync(datacards.Datacards):
	def __init__(self, higgs_masses=["125"], cb=None):
		super(SMHttDatacardsForSync, self).__init__(cb)

		if cb is None:
			signal_processes = []

			# ======================================================================
			# MT channel
			self.add_processes(
					channel="mt",
					categories=["mt_"+category for category in ["inclusivemt40"]],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# ET channel
			self.add_processes(
					channel="et",
					categories=["et_"+category for category in ["inclusivemt40"]],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# EM channel
			self.add_processes(
					channel="em",
					categories=["em_"+category for category in []],
					bkg_processes=["ZTT", "ZLL", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			# ======================================================================
			# TT channel
			self.add_processes(
					channel="tt",
					categories=["tt_"+category for category in []],
					bkg_processes=["ZTT", "ZL", "ZJ", "TT", "VV", "W", "QCD"],
					sig_processes=signal_processes,
					analysis=["htt"],
					era=["13TeV"],
					mass=higgs_masses
			)

			if log.isEnabledFor(logging.DEBUG):
				self.cb.PrintAll()
