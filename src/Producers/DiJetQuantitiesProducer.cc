
#include <boost/regex.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/DiJetQuantitiesProducer.h"


double DiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diJetSystemAvailable ? dijetQuantity((static_cast<HttProduct const&>(product)).m_diJetSystem) : DefaultValues::UndefinedDouble);
}

void DiJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetPt", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetEta", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetPhi", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetMass", [this](event_type const& event, product_type const& product) {
		return DiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetDeltaPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_validJets[0]->p4, product.m_validJets[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetAbsDeltaEta", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_validJets[0]->p4.Eta() - product.m_validJets[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("diJetdiLepPhi", [](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? (product.m_diJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddBoolQuantity("centralJet30Exists", [](event_type const& event, product_type const& product) {
		return (product.m_nCentralJets30 > 0 ? true : false);
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nCentralJets20", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets20;
	});
	LambdaNtupleConsumer<HttTypes>::AddIntQuantity("nCentralJets30", [](event_type const& event, product_type const& product) {
		return product.m_nCentralJets30;
	});
        std::vector<std::string> jetsCheckTriggerMatchByHltName = settings.GetCheckJetsTriggerMatch();
        m_jet1LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
                Utility::ParseVectorToMap(settings.GetDiTauPairJet1LowerPtCuts()), m_jet1LowerPtCutsByHltName
        );
        m_jet2LowerPtCutsByIndex = Utility::ParseMapTypes<size_t, float>(
                Utility::ParseVectorToMap(settings.GetDiTauPairJet2LowerPtCuts()), m_jet2LowerPtCutsByHltName
        );
        m_jetsLowerMjjCutsByIndex = Utility::ParseMapTypes<size_t, float>(
                Utility::ParseVectorToMap(settings.GetDiTauPairJetsLowerMjjCuts()), m_jetsLowerMjjCutsByHltName
        );
        m_trailingJetFiltersByIndex = Utility::ParseMapTypes<size_t, std::string>(
                Utility::ParseVectorToMap(settings.GetDiTauPairTrailingJetFilters()), m_trailingJetFiltersByHltName
        );

        m_hltFiredBranchNames = Utility::ParseVectorToMap(settings.GetHLTBranchNames());
        for (auto hltNames: m_hltFiredBranchNames)
        {
            std::map<std::string, std::vector<float>> jet1LowerPtCutsByHltName = m_jet1LowerPtCutsByHltName;
            std::map<std::string, std::vector<float>> jet2LowerPtCutsByHltName = m_jet2LowerPtCutsByHltName;
            std::map<std::string, std::vector<float>> jetsLowerMjjCutsByHltName = m_jetsLowerMjjCutsByHltName;
            std::map<std::string, std::vector<std::string>> trailingJetFiltersByHltName = m_trailingJetFiltersByHltName;
            LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(hltNames.first+"_jets", [hltNames, jetsCheckTriggerMatchByHltName, jet1LowerPtCutsByHltName, jet2LowerPtCutsByHltName, jetsLowerMjjCutsByHltName, trailingJetFiltersByHltName](event_type const& event, product_type const& product)
            {
                bool jetsFiredTrigger = false;
                LOG(DEBUG) << "Checking trigger match for " << hltNames.first << std::endl << "checkJets: " << (std::find(jetsCheckTriggerMatchByHltName.begin(), jetsCheckTriggerMatchByHltName.end(), hltNames.first) != jetsCheckTriggerMatchByHltName.end());
                if (std::find(jetsCheckTriggerMatchByHltName.begin(), jetsCheckTriggerMatchByHltName.end(), hltNames.first) != jetsCheckTriggerMatchByHltName.end())
                {
                    for (auto hltName: hltNames.second)
                    {
                        bool hltFiredJets = false;
                        LOG(DEBUG) << "Checking trigger object matching for jets";
                        // for (auto hlt : product.m_detailedTriggerMatchedJets)
                        // {
                        //     LOG(WARNING) << hlt.first;
                        //     LOG(WARNING) << hlt.second["HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v"]["hltMatchedVBFOnePFJet2CrossCleanedFromDoubleLooseChargedIsoPFTau20"].at(0).p4.Pt();
                        // }
                        if (product.m_validJets.size() >= 2)
                        {
                            LOG(DEBUG) << "Jet 1 detailed trigger matched: " << (product.m_jetTriggerMatch.find(static_cast<KJet*>(product.m_validJets.at(0))) != product.m_jetTriggerMatch.end());
                            LOG(DEBUG) << "Jet 2 detailed trigger matched: " << (product.m_detailedTriggerMatchedJets.find(static_cast<KJet*>(product.m_validJets.at(1))) != product.m_detailedTriggerMatchedJets.end());
                            if ((product.m_jetTriggerMatch.find(static_cast<KJet*>(product.m_validJets.at(0))) != product.m_jetTriggerMatch.end())
                                    && (product.m_detailedTriggerMatchedJets.find(static_cast<KJet*>(product.m_validJets.at(1))) != product.m_detailedTriggerMatchedJets.end()))
                            {
                                    LOG(DEBUG) << "Found detailed trigger matched objects for both jets.";
                                    auto triggerJet1 = product.m_jetTriggerMatch.at(static_cast<KJet*>(product.m_validJets.at(0)));
                                    for (auto hlts: triggerJet1)
                                    {
                                        if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                        {
                                            hltFiredJets = hlts.second;
                                        }
                                    }
                                    LOG(DEBUG) << "Found trigger match for the leading jet? " << hltFiredJets;
                                    auto triggerJet2 = product.m_detailedTriggerMatchedJets.at(static_cast<KJet*>(product.m_validJets.at(1)));
                                    for (auto hlts: triggerJet2)
                                    {
                                        if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                        {
                                            LOG(DEBUG) << "Found HLT path name " << hlts.first << " for the trailing jet.";
                                            for (auto hltFilters : hlts.second)
                                            {
                                                LOG(DEBUG) << "Looking for filter " << trailingJetFiltersByHltName.at(hltName).at(0);
                                                if (boost::regex_search(hltFilters.first, boost::regex(trailingJetFiltersByHltName.at(hltName).at(0), boost::regex::icase | boost::regex::extended)))
                                                {
                                                    LOG(DEBUG) << "Found filter " << hltFilters.first << " for the trailing jet.";
                                                    hltFiredJets = hltFiredJets && (hltFilters.second.size() > 0);
                                                }
                                            }
                                        }
                                    }
                                    LOG(DEBUG) << "Found trigger for both jets? " << hltFiredJets;
                                    // passing kinematic cuts for trigger
                                    if (jet1LowerPtCutsByHltName.find(hltName) != jet1LowerPtCutsByHltName.end())
                                    {
                                        hltFiredJets = hltFiredJets &&
                                                (static_cast<KJet*>(product.m_validJets.at(0))->p4.Pt() > *std::max_element(jet1LowerPtCutsByHltName.at(hltName).begin(), jet1LowerPtCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Jet 1 Pt: " << static_cast<KJet*>(product.m_validJets.at(0))->p4.Pt() << " threshold: " << *std::max_element(jet1LowerPtCutsByHltName.at(hltName).begin(), jet1LowerPtCutsByHltName.at(hltName).end());
                                    }
                                    if (jet2LowerPtCutsByHltName.find(hltName) != jet2LowerPtCutsByHltName.end())
                                    {
                                        hltFiredJets = hltFiredJets &&
                                                (static_cast<KJet*>(product.m_validJets.at(1))->p4.Pt() > *std::max_element(jet2LowerPtCutsByHltName.at(hltName).begin(), jet2LowerPtCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Jet 2 Pt: " << static_cast<KJet*>(product.m_validJets.at(1))->p4.Pt() << " threshold: " << *std::max_element(jet2LowerPtCutsByHltName.at(hltName).begin(), jet2LowerPtCutsByHltName.at(hltName).end());
                                    }
                                    if (jetsLowerMjjCutsByHltName.find(hltName) != jetsLowerMjjCutsByHltName.end())
                                    {
                                        hltFiredJets = hltFiredJets &&
                                                ((static_cast<KJet*>(product.m_validJets.at(0))->p4 + static_cast<KJet*>(product.m_validJets.at(1))->p4).M() > *std::max_element(jetsLowerMjjCutsByHltName.at(hltName).begin(), jetsLowerMjjCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Mjj: " << (static_cast<KJet*>(product.m_validJets.at(0))->p4 + static_cast<KJet*>(product.m_validJets.at(1))->p4).M() << " threshold: " << *std::max_element(jetsLowerMjjCutsByHltName.at(hltName).begin(), jetsLowerMjjCutsByHltName.at(hltName).end());
                                    }
                                    LOG(DEBUG) << "jets pass also kinematic cuts? " << hltFiredJets;
                            }
                        }
                        LOG(DEBUG) << "hltFiredJets: " << hltFiredJets << std::endl << "Lambda function for hltName " << hltName << ": " << (LambdaNtupleConsumer<HttTypes>::GetBoolQuantities()[hltNames.first](event, product));
                        jetsFiredTrigger = jetsFiredTrigger || (hltFiredJets && LambdaNtupleConsumer<HttTypes>::GetBoolQuantities()[hltNames.first]);
                        LOG(DEBUG) << "jetsFiredTrigger: " << jetsFiredTrigger;
                    }
                }
                return jetsFiredTrigger;
                });
        }
}

void DiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	// central jet veto
	product.m_nCentralJets30 = 0;
	if (KappaProduct::GetNJetsAbovePtThreshold(product.m_validJets, 30.0) >= 2)
	{
		float minJetEta = std::min(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		float maxJetEta = std::max(product.m_validJets[0]->p4.Eta(), product.m_validJets[1]->p4.Eta());
		for (std::vector<KBasicJet*>::const_iterator jet = product.m_validJets.begin();
		     jet != product.m_validJets.end(); ++jet)
		{
			// skip first two jets
			if ((*jet) == product.m_validJets[0]) continue;
			if ((*jet) == product.m_validJets[1]) continue;

			if ((minJetEta < (*jet)->p4.Eta()) && ((*jet)->p4.Eta() < maxJetEta))
			{
				if ((*jet)->p4.Pt() > 20.0)
					product.m_nCentralJets20++;

				if ((*jet)->p4.Pt() > 30.0)
					product.m_nCentralJets30++;
			}
		}
	}

	if (product.m_validJets.size() >= 2)
	{
		product.m_diJetSystem = (product.m_validJets[0]->p4 + product.m_validJets[1]->p4);
		product.m_diJetSystemAvailable = true;
	}
	else
	{
		product.m_diJetSystemAvailable = false;
	}
}
