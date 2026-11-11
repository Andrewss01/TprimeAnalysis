#!/usr/bin/env python
import os, ROOT
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs

loadJMESystematicsCalculators() # https://cms-jerc.web.cern.ch/Recommendations/

cvmfsPOGpath = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/"
jerSmearingToolFile = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/JER-Smearing/2026-09-18/jer_smear.json.gz" # JERSmear v2 (min cut 0.01 on the smeared pt, as in CMSSW)

# ---- JES/JER uncertainty sources (MC), https://cms-jme-jerc.docs.cern.ch/recommendations/uncertainties/#treatment-alternatives ----
# eraTag = "2022", "2022EE", "2023", "2023BPix", "2024": also the suffix of the uncorrelated Regrouped sources in the json (e.g. Regrouped_Absolute_2024)
# JES Regrouped set: sources without era suffix correlated across years, with era suffix uncorrelated
JES_REGROUPED = [
    "Absolute",  "Absolute_{era}",
    "BBEC1",     "BBEC1_{era}",
    "EC2",       "EC2_{era}",
    "FlavorQCD",
    "HF",        "HF_{era}",
    "RelativeBal",
    "RelativeSample_{era}",
]
# JER split in 6 (|eta|,pt) regions (config.splitJER = True):
#   jer0: |eta|<1.93           jer1: 1.93<|eta|<2.5
#   jer2: 2.5<|eta|<3, pt<50   jer3: 2.5<|eta|<3, pt>50
#   jer4: 3<|eta|<5,   pt<50   jer5: 3<|eta|<5,   pt>50
JER_SPLIT = ["jer"+str(k) for k in range(6)]

def jes_sources(eraTag):
    """config.jesUncertainties: Total (kept, to use the unsplit JES in step 2) + 11 Regrouped"""
    return ["Total"] + ["Regrouped_" + s.format(era=eraTag) for s in JES_REGROUPED]

def top_scenarios(eraTag):
    """scenarios of the TopMixed/TopResolved pt, mass, score branches (MC), passed to nanoTopcand and nanoTopevaluate_MultiScore:
    nominal + jes<source>up/down (Total + 11 Regrouped) + jer up/down (unsplit, from the calculator with splitJER=False) + jer0...jer5 up/down
    = 1 + 2*12 + 2 + 2*6 = 39.
    The candidates use only jets/fatjets with |eta|<2.5 (tools.get_jet/get_fatjet): for them jer2...jer5 are identical to nominal (kept anyway)."""
    scenarios = ["nominal"]
    for source in jes_sources(eraTag):
        scenarios += ["jes"+source+"up", "jes"+source+"down"]
    for jer in ["jer"] + JER_SPLIT:
        scenarios += [jer+"up", jer+"down"]
    return scenarios

versiontag = {
    "2018"      :   "2018_UL",
    "2022"      :   "Run3-22CDSep23-Summer22-NanoAODv12/2026-06-05",
    "2022EE"    :   "Run3-22EFGSep23-Summer22EE-NanoAODv12/2026-06-05",
    "2023"      :   "Run3-23CSep23-Summer23-NanoAODv12/2026-07-15",
    "2023BPix"  :   "Run3-23DSep23-Summer23BPix-NanoAODv12/2026-07-15",
    "2024"      :   "Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2026-07-16",
}
jestag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V4_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V4_MC',
            '2023'      : 'Summer23Prompt23_V4_MC',
            '2023BPix'  : 'Summer23BPixPrompt23_V4_MC',
            '2024'      : 'Summer24Prompt24_V5_MC',
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_V5_MC',
            '2022'      : 'Summer22_22Sep2023_V4_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_V4_MC',
            '2023'      : 'Summer23Prompt23_V4_MC',
            '2023BPix'  : 'Summer23BPixPrompt23_V4_MC',
            '2024'      : 'Summer24Prompt24_V5_MC',
        }
    },
    "DATA":{
        'AK8PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_V4_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2023_C1'       : 'Summer23Prompt23_V4_DATA',
            '2023_C2'       : 'Summer23Prompt23_V4_DATA',
            '2023_C3'       : 'Summer23Prompt23_V4_DATA',
            '2023_C4'       : 'Summer23Prompt23_V4_DATA',
            '2023BPix_D'    : 'Summer23BPixPrompt23_V4_DATA',
            '2024_C'          : 'Summer24Prompt24_V5_DATA',
            '2024_D'          : 'Summer24Prompt24_V5_DATA',
            '2024_E'          : 'Summer24Prompt24_V5_DATA',
            '2024_F'          : 'Summer24Prompt24_V5_DATA',
            '2024_G'          : 'Summer24Prompt24_V5_DATA',
            '2024_H'          : 'Summer24Prompt24_V5_DATA',
            '2024_I'          : 'Summer24Prompt24_V5_DATA',
        },
        'AK4PFPuppi':{
            '2018'          : 'Summer19UL18_V5_DATA',
            '2022'          : 'Summer22_22Sep2023_V4_DATA',
            '2022EE_E'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2022EE_F'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2022EE_G'      : 'Summer22EE_22Sep2023_V4_DATA',
            '2023_C1'       : 'Summer23Prompt23_V4_DATA',
            '2023_C2'       : 'Summer23Prompt23_V4_DATA',
            '2023_C3'       : 'Summer23Prompt23_V4_DATA',
            '2023_C4'       : 'Summer23Prompt23_V4_DATA',
            '2023BPix_D'    : 'Summer23BPixPrompt23_V4_DATA',
            '2024_C'        : 'Summer24Prompt24_V5_DATA',
            '2024_D'        : 'Summer24Prompt24_V5_DATA',
            '2024_E'        : 'Summer24Prompt24_V5_DATA',
            '2024_F'        : 'Summer24Prompt24_V5_DATA',
            '2024_G'        : 'Summer24Prompt24_V5_DATA',
            '2024_H'        : 'Summer24Prompt24_V5_DATA',
            '2024_I'        : 'Summer24Prompt24_V5_DATA',
        }
    }
}
jertag = {
    "MC":{
        'AK8PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV2_MC', 
            '2022EE'    : 'Summer22EE_22Sep2023_JRV2_MC',
            '2023'      : 'Summer23Prompt23_RunCv1234_JRV3_MC', 
            '2023BPix'  : 'Summer23BPixPrompt23_RunD_JRV3_MC',
            '2024'      : 'Summer24Prompt24_JRV2_MC',
        },
        'AK4PFPuppi':{
            '2018'      : 'Summer19UL18_JRV2_MC',
            '2022'      : 'Summer22_22Sep2023_JRV2_MC',
            '2022EE'    : 'Summer22EE_22Sep2023_JRV2_MC',
            '2023'      : 'Summer23Prompt23_RunCv1234_JRV3_MC', 
            '2023BPix'  : 'Summer23BPixPrompt23_RunD_JRV3_MC',
            '2024'      : 'Summer24Prompt24_JRV2_MC',
        }
    }
}
def configcreate(isMC=True, year=2022, EE=False, runPeriod="C", jetType="AK4PFPuppi", forMET=False, doJer=True, splitJER=True, isT1SmearedMET=False):
    # splitJER=True : JER split in jer0...jer5 (no jerup/jerdown, CMSJMECalculators gives either the split or the unsplit JER)
    # splitJER=False: unsplit jerup/jerdown -> in step 1 a second calculator with splitJER=False writes only jerup/jerdown
    # isT1SmearedMET (only forMET, MC with doJer): True  -> Type-1 MET from the smeared jets (nominal smeared, real JER up/down variations)
    #                                              False -> nominal from unsmeared jets, all JER variations = smeared nominal (up == down)
    print("isMC, year, EE, runPeriod, jetType, forMET, doJer, splitJER, isT1SmearedMET:", isMC, year, EE, runPeriod, jetType, forMET, doJer, splitJER, isT1SmearedMET)
    if forMET:
        configCls = calcConfigs.METVariations
    elif "AK4" in jetType:
        configCls = calcConfigs.JetVariations
    elif "AK8" in jetType:
        configCls = calcConfigs.FatJetVariations
    else:
        print("Unsupported configurationType")

    year_ = str(year)
    if year == 2022:
        if EE: year_ += "EE"
    elif year == 2023:
        if EE: year_ += "BPix"
    eraTag = year_ # era key without run period: suffix of the uncorrelated Regrouped JES sources (e.g. Regrouped_Absolute_2024)

    tagver = versiontag[year_]
    print("tagver: ", tagver)
    if runPeriod != ".": 
        if ("2022EE" in year_) or ("2023" in year_) or ("2024" in year_):
            year_ += "_"+runPeriod
            print("year_ with runPeriod: ", year_)
    if (forMET or "AK4" in jetType):
        jsonFile = cvmfsPOGpath + tagver + "/jet_jerc.json.gz"
    else:
        jsonFile = cvmfsPOGpath + tagver + "/fatJet_jerc.json.gz"

    print("year, RunTag, jetType: ", year_, tagver, jetType)
    print("JES :", jestag["MC" if isMC else "DATA"][jetType][year_])

    config          = configCls(jsonFile, jetType)
    config.jecTag   = jestag["MC" if isMC else "DATA"][jetType][year_]
    config.jecLevel = "L1L2L3Res"
    if isMC:
        if year_ == "2018":
            config.jesUncertainties = ["Total", "AbsoluteMPFBias", "AbsoluteScale", "AbsoluteStat", "Fragmentation", "PileUpDataMC", "PileUpPtRef", "RelativeFSR", "RelativeStatFSR", "SinglePionECAL", "SinglePionHCAL", "TimePtEta"]
        else:
            config.jesUncertainties = jes_sources(eraTag) # Total + 11 Regrouped
    print("JES uncertainties:", config.jesUncertainties)
    if doJer and isMC:
        print("JER :", jertag["MC" if isMC else "DATA"][jetType][year_])
        config.jerTag               = jertag["MC"][jetType][year_]
        config.splitJER             = splitJER and (year_ != "2018") # jer0 ... jer5 (6 |eta|,pt regions)
        config.jsonFileSmearingTool = jerSmearingToolFile
        config.smearingToolName     = "JERSmear"
        if forMET:
            config.isT1SmearedMET   = isT1SmearedMET # jet smearing propagated to the Type-1 MET

    if "AK8" in jetType:
        config.jsonFileSubjet       = cvmfsPOGpath + tagver + "/jet_jerc.json.gz"
        config.jetAlgoSubjet        = "AK4PFPuppi" if year_ !="2018" else "AK4PFchs"
        config.jecTagSubjet         = jestag["MC" if isMC else "DATA"]["AK4PFPuppi" if year_ !="2018" else "AK4PFchs"][year_]
        config.jecLevelSubjet       = "L1L2L3Res"
        config.jsonFileSmearingTool = jerSmearingToolFile
        config.smearingToolName     = "JERSmear"
    if "AK4" in jetType:
        calc = config.create() # ROOT.JetVariationsCalculator(config.create())
    elif forMET:
        calc = config.create() # ROOT.Type1METVariationsCalculator(config.create())
    elif "AK8" in jetType:
        calc = config.create() # ROOT.FatJetVariationsCalculator(config.create()) 
    # return config.create()
    return calc