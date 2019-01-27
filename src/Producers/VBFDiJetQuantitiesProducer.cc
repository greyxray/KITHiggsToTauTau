
#include <boost/regex.hpp>

#include "Artus/Consumer/interface/LambdaNtupleConsumer.h"
#include "Artus/Utility/interface/DefaultValues.h"

#include "HiggsAnalysis/KITHiggsToTauTau/interface/Producers/VBFDiJetQuantitiesProducer.h"


double VBFDiJetQuantitiesProducer::GetDiJetQuantity(product_type const& product,
                                                 dijet_extractor_lambda dijetQuantity)
{
	return ((static_cast<HttProduct const&>(product)).m_diJetSystemAvailable ? dijetQuantity((static_cast<HttProduct const&>(product)).m_vbfDiJetSystem) : DefaultValues::UndefinedDouble);
}

void VBFDiJetQuantitiesProducer::Init(setting_type const& settings)
{
	ProducerBase<HttTypes>::Init(settings);

	// add possible quantities for the lambda ntuples consumers
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetPt", [this](event_type const& event, product_type const& product) {
		return VBFDiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Pt(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetEta", [this](event_type const& event, product_type const& product) {
		return VBFDiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Eta(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetPhi", [this](event_type const& event, product_type const& product) {
		return VBFDiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.Phi(); });
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetMass", [this](event_type const& event, product_type const& product) {
		return VBFDiJetQuantitiesProducer::GetDiJetQuantity(product, [](RMDLV diJetSystem) -> double
	{
		return diJetSystem.mass(); });
	});
	
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetDeltaPhi", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ROOT::Math::VectorUtil::DeltaPhi(product.m_vbfDiJetPair[0]->p4, product.m_vbfDiJetPair[1]->p4) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetAbsDeltaEta", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? std::abs(product.m_vbfDiJetPair[0]->p4.Eta() - product.m_vbfDiJetPair[1]->p4.Eta()) :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfDiJetdiLepPhi", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? ((static_cast<HttProduct const&>(product)).m_vbfDiJetSystem + product.m_diLeptonSystem).Phi() :
		                                        DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfLeadJetPt", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Pt() : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfLeadJetEta", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Eta() : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfLeadJetPhi", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Phi() : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfTrailJetPt", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Pt() : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfTrailJetEta", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Eta() : DefaultValues::UndefinedFloat;
	});
	LambdaNtupleConsumer<HttTypes>::AddFloatQuantity("vbfTrailJetPhi", [this](event_type const& event, product_type const& product) {
		return product.m_diJetSystemAvailable ? product.m_vbfDiJetPair.at(0)->p4.Phi() : DefaultValues::UndefinedFloat;
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
            LambdaNtupleConsumer<HttTypes>::AddBoolQuantity(hltNames.first+"_vbfjets", [this, hltNames, jetsCheckTriggerMatchByHltName, jet1LowerPtCutsByHltName, jet2LowerPtCutsByHltName, jetsLowerMjjCutsByHltName, trailingJetFiltersByHltName](event_type const& event, product_type const& product)
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
                        //     LOG(DEBUG) << hlt.first;
                        //     LOG(DEBUG) << hlt.second["HLT_VBF_DoubleLooseChargedIsoPFTau20_Trk1_eta2p1_Reg_v"]["hltMatchedVBFOnePFJet2CrossCleanedFromDoubleLooseChargedIsoPFTau20"].at(0).p4.Pt();
                        // }
                        if (product.m_vbfDiJetPair.size() >= 2)
                        {
                            if ((product.m_jetTriggerMatch.find(static_cast<KJet*>(product.m_vbfDiJetPair.at(0))) != product.m_jetTriggerMatch.end())
                                    && (product.m_detailedTriggerMatchedJets.find(static_cast<KJet*>(product.m_vbfDiJetPair.at(1))) != product.m_detailedTriggerMatchedJets.end()))
                            {
                                    LOG(DEBUG) << "Found detailed trigger matched objects for both jets.";
                                    auto triggerJet1 = product.m_jetTriggerMatch.at(static_cast<KJet*>(product.m_vbfDiJetPair.at(0)));
                                    for (auto hlts: triggerJet1)
                                    {
                                        if (boost::regex_search(hlts.first, boost::regex(hltName, boost::regex::icase | boost::regex::extended)))
                                        {
                                            hltFiredJets = hlts.second;
                                        }
                                    }
                                    LOG(DEBUG) << "Found trigger match for the leading jet? " << hltFiredJets;
                                    auto triggerJet2 = product.m_detailedTriggerMatchedJets.at(static_cast<KJet*>(product.m_vbfDiJetPair.at(1)));
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
                                                    LOG(DEBUG) << "Found filter " << hltFilters.first << "for the trailing jet.";
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
                                                (static_cast<KJet*>(product.m_vbfDiJetPair.at(0))->p4.Pt() > *std::max_element(jet1LowerPtCutsByHltName.at(hltName).begin(), jet1LowerPtCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Jet 1 Pt: " << static_cast<KJet*>(product.m_vbfDiJetPair.at(0))->p4.Pt() << " threshold: " << *std::max_element(jet1LowerPtCutsByHltName.at(hltName).begin(), jet1LowerPtCutsByHltName.at(hltName).end());
                                    }
                                    if (jet2LowerPtCutsByHltName.find(hltName) != jet2LowerPtCutsByHltName.end())
                                    {
                                        hltFiredJets = hltFiredJets &&
                                                (static_cast<KJet*>(product.m_vbfDiJetPair.at(1))->p4.Pt() > *std::max_element(jet2LowerPtCutsByHltName.at(hltName).begin(), jet2LowerPtCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Jet 2 Pt: " << static_cast<KJet*>(product.m_vbfDiJetPair.at(1))->p4.Pt() << " threshold: " << *std::max_element(jet2LowerPtCutsByHltName.at(hltName).begin(), jet2LowerPtCutsByHltName.at(hltName).end());
                                    }
                                    if (jetsLowerMjjCutsByHltName.find(hltName) != jetsLowerMjjCutsByHltName.end())
                                    {
                                        hltFiredJets = hltFiredJets &&
                                                ((static_cast<KJet*>(product.m_vbfDiJetPair.at(0))->p4 + static_cast<KJet*>(product.m_vbfDiJetPair.at(1))->p4).mass() > *std::max_element(jetsLowerMjjCutsByHltName.at(hltName).begin(), jetsLowerMjjCutsByHltName.at(hltName).end()));
                                        LOG(DEBUG) << "Mjj: " << (static_cast<KJet*>(product.m_vbfDiJetPair.at(0))->p4 + static_cast<KJet*>(product.m_vbfDiJetPair.at(1))->p4).mass() << " threshold: " << *std::max_element(jetsLowerMjjCutsByHltName.at(hltName).begin(), jetsLowerMjjCutsByHltName.at(hltName).end());
                                    }
                                    LOG(DEBUG) << "jets pass also kinematic cuts? " << hltFiredJets;
                            }
                        }
                        LOG(DEBUG) << "hltFiredJets: " << hltFiredJets << "Lambda function for hltName " << hltName << ": " << (LambdaNtupleConsumer<HttTypes>::GetBoolQuantities()[hltNames.first](event, product));
                        jetsFiredTrigger = jetsFiredTrigger || (hltFiredJets && LambdaNtupleConsumer<HttTypes>::GetBoolQuantities()[hltNames.first]);
                        LOG(DEBUG) << "jetsFiredTrigger: " << jetsFiredTrigger;
                    }
                }
                return jetsFiredTrigger;
                });
        }
}

void VBFDiJetQuantitiesProducer::Produce(event_type const& event, product_type& product,
	                                  setting_type const& settings) const
{
	if (product.m_validJets.size() >= 2)
	{
                // Loop over the valid jets to find the pair with the highest dijet mass
                double mjj = 0.;
                unsigned int i1 = 0;
                unsigned int i2 = 0;
                for (unsigned int i = 0; i < product.m_validJets.size()-1; i++)
                {
                    const KJet* jet1 = static_cast<KJet*>(product.m_validJets.at(i));
                    for (unsigned int j = i+1; j < product.m_validJets.size(); j++)
                    {
                        const KJet* jet2 = static_cast<KJet*>(product.m_validJets.at(j));
                        const double mjj_temp = (jet1->p4 + jet2->p4).mass();
                        if (mjj_temp > mjj)
                        {
                            mjj = mjj_temp;
                            i1 = i;
                            i2 = j;
                        }
                    }
                } 
                LOG(DEBUG) << "Highest dijet-mass is " << mjj;
                LOG(DEBUG) << "Found for the jets with index " << i1 << " and " << i2;
		product.m_vbfDiJetSystem = (product.m_validJets[i1]->p4 + product.m_validJets[i2]->p4);
                product.m_vbfDiJetPair.push_back(static_cast<KJet*>(product.m_validJets.at(i1)));
                product.m_vbfDiJetPair.push_back(static_cast<KJet*>(product.m_validJets.at(i2)));
	}
}
