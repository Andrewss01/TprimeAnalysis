import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import tensorflow as tf
from itertools import combinations, chain
import os


###### UTILITIES ######
def fill_mass(mass_dnn, idx_top, j0, j1, j2, fj, scenario):
    if fj == None:#3j0fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        j2_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup) 
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        top_p4 = j0_p4+j1_p4+j2_p4
        mass_dnn[idx_top, 0] = top_p4.M()
        mass_dnn[idx_top, 1] = top_p4.M()
        mass_dnn[idx_top, 2] = top_p4.Pt()

    elif j2 == None:#2j1fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
        top_p4 = j0_p4+j1_p4
        mass_dnn[idx_top, 0] = top_p4.M()
        top                  = top2j1fj(fj, j0, j1, scenario)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    else: #3j1fj
        j0_p4 = ROOT.TLorentzVector()
        j1_p4 = ROOT.TLorentzVector()
        j2_p4 = ROOT.TLorentzVector()
        if scenario == "nominal":
            j0_p4.SetPtEtaPhiM(j0.pt_nominal, j0.eta, j0.phi, j0.mass_nominal)
            j1_p4.SetPtEtaPhiM(j1.pt_nominal, j1.eta, j1.phi, j1.mass_nominal)
            j2_p4.SetPtEtaPhiM(j2.pt_nominal, j2.eta, j2.phi, j2.mass_nominal)
        elif scenario == "jesTotalup":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotalup, j0.eta, j0.phi, j0.mass_jesTotalup)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotalup, j1.eta, j1.phi, j1.mass_jesTotalup)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotalup, j2.eta, j2.phi, j2.mass_jesTotalup) 
        elif scenario == "jesTotaldown":
            j0_p4.SetPtEtaPhiM(j0.pt_jesTotaldown, j0.eta, j0.phi, j0.mass_jesTotaldown)
            j1_p4.SetPtEtaPhiM(j1.pt_jesTotaldown, j1.eta, j1.phi, j1.mass_jesTotaldown)
            j2_p4.SetPtEtaPhiM(j2.pt_jesTotaldown, j2.eta, j2.phi, j2.mass_jesTotaldown)
        elif scenario == "jerup":
            j0_p4.SetPtEtaPhiM(j0.pt_jerup, j0.eta, j0.phi, j0.mass_jerup)
            j1_p4.SetPtEtaPhiM(j1.pt_jerup, j1.eta, j1.phi, j1.mass_jerup)
            j2_p4.SetPtEtaPhiM(j2.pt_jerup, j2.eta, j2.phi, j2.mass_jerup)
        elif scenario == "jerdown":
            j0_p4.SetPtEtaPhiM(j0.pt_jerdown, j0.eta, j0.phi, j0.mass_jerdown)
            j1_p4.SetPtEtaPhiM(j1.pt_jerdown, j1.eta, j1.phi, j1.mass_jerdown)
            j2_p4.SetPtEtaPhiM(j2.pt_jerdown, j2.eta, j2.phi, j2.mass_jerdown)
        top_p4 = j0_p4+j1_p4+j2_p4
        mass_dnn[idx_top, 0] = top_p4.M()
        top                  = top3j1fj(fj, j0, j1, j2, scenario)
        mass_dnn[idx_top, 1] = top.M()
        mass_dnn[idx_top, 2] = top.Pt()
    return mass_dnn

def fill_fj(year, fj_dnn, fj, idx_top, scenario):
    if year==2018: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.deepTagMD_TvsQCD
        fj_dnn[idx_top, 3]  = fj.deepTagMD_WvsQCD
        fj_dnn[idx_top, 4]  = fj.deepTag_QCD
        fj_dnn[idx_top, 5]  = fj.deepTag_QCDothers
        fj_dnn[idx_top, 6]  = fj.deepTag_TvsQCD
        fj_dnn[idx_top, 7]  = fj.deepTag_WvsQCD
        fj_dnn[idx_top, 8]  = fj.eta
        fj_dnn[idx_top, 10] = fj.phi
        if scenario == "nominal":
            fj_dnn[idx_top, 9]  = fj.mass_nominal
            fj_dnn[idx_top, 11] = fj.pt_nominal
        elif scenario == "jesTotalup":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotalup
            fj_dnn[idx_top, 11] = fj.pt_jesTotalup
        elif scenario == "jesTotaldown":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotaldown
            fj_dnn[idx_top, 11] = fj.pt_jesTotaldown
        elif scenario == "jerup":
            fj_dnn[idx_top, 9]  = fj.mass_jerup
            fj_dnn[idx_top, 11] = fj.pt_jerup
        elif scenario == "jerdown":
            fj_dnn[idx_top, 9]  = fj.mass_jerdown
            fj_dnn[idx_top, 11] = fj.pt_jerdown

    elif year in [2022,2023]: 
        fj_dnn[idx_top, 0]  = fj.area
        fj_dnn[idx_top, 1]  = fj.btagDeepB
        fj_dnn[idx_top, 2]  = fj.particleNetWithMass_TvsQCD
        fj_dnn[idx_top, 3]  = fj.particleNetWithMass_WvsQCD
        fj_dnn[idx_top, 4]  = fj.particleNet_QCD
        fj_dnn[idx_top, 5] = fj.particleNetWithMass_QCD 
        fj_dnn[idx_top, 6] = fj.particleNet_XbbVsQCD
        fj_dnn[idx_top, 7] = fj.particleNet_XqqVsQCD
        fj_dnn[idx_top, 8]  = fj.eta
        fj_dnn[idx_top, 10]  = fj.phi
        if scenario == "nominal":
            fj_dnn[idx_top, 9]  = fj.mass_nominal
            fj_dnn[idx_top, 11] = fj.pt_nominal
        elif scenario == "jesTotalup":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotalup
            fj_dnn[idx_top, 11] = fj.pt_jesTotalup
        elif scenario == "jesTotaldown":
            fj_dnn[idx_top, 9]  = fj.mass_jesTotaldown
            fj_dnn[idx_top, 11] = fj.pt_jesTotaldown
        elif scenario == "jerup":
            fj_dnn[idx_top, 9]  = fj.mass_jerup
            fj_dnn[idx_top, 11] = fj.pt_jerup
        elif scenario == "jerdown":
            fj_dnn[idx_top, 9]  = fj.mass_jerdown
            fj_dnn[idx_top, 11] = fj.pt_jerdown
    return fj_dnn

def fill_jets(year, jets_dnn, j0, j1, j2, sumjet, fj_phi, fj_eta, idx_top, scenario): 
    if year==2018:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagDeepB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagDeepB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if scenario == "nominal":
            jets_dnn[idx_top, 0, 3] = j0.mass_nominal
            jets_dnn[idx_top, 0, 5] = j0.pt_nominal
            jets_dnn[idx_top, 1, 3] = j1.mass_nominal
            jets_dnn[idx_top, 1, 5] = j1.pt_nominal
        elif scenario == "jesTotalup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotalup
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotalup
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotalup
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotalup
        elif scenario == "jesTotaldown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotaldown
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotaldown
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotaldown
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotaldown
        elif scenario == "jerup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerup
            jets_dnn[idx_top, 0, 5] = j0.pt_jerup
            jets_dnn[idx_top, 1, 3] = j1.mass_jerup
            jets_dnn[idx_top, 1, 5] = j1.pt_jerup
        elif scenario == "jerdown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerdown
            jets_dnn[idx_top, 0, 5] = j0.pt_jerdown
            jets_dnn[idx_top, 1, 3] = j1.mass_jerdown
            jets_dnn[idx_top, 1, 5] = j1.pt_jerdown
                        
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagDeepB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
            if scenario == "nominal":
                jets_dnn[idx_top, 2, 3] = j2.mass_nominal
                jets_dnn[idx_top, 2, 5] = j2.pt_nominal
            elif scenario == "jesTotalup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotalup
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotalup
            elif scenario == "jesTotaldown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotaldown
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotaldown
            elif scenario == "jerup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerup
                jets_dnn[idx_top, 2, 5] = j2.pt_jerup
            elif scenario == "jerdown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerdown
                jets_dnn[idx_top, 2, 5] = j2.pt_jerdown

    elif year in [2022,2023]:
        jets_dnn[idx_top, 0, 0] = j0.area
        jets_dnn[idx_top, 0, 1] = j0.btagDeepFlavB
        jets_dnn[idx_top, 0, 2] = deltaEta(j0.eta, sumjet.Eta())#j0.#delta eta 3jets-jet
        jets_dnn[idx_top, 0, 4] = deltaPhi(j0.phi, sumjet.Phi())#j0.#delta phi 3jets-jet
        jets_dnn[idx_top, 0, 6] = deltaPhi(j0.phi, fj_phi)#j0.#deltaphi fj-jet
        jets_dnn[idx_top, 0, 7] = deltaEta(j0.eta, fj_eta)#j0.#deltaeta fj-jet

        jets_dnn[idx_top, 1, 0] = j1.area
        jets_dnn[idx_top, 1, 1] = j1.btagDeepFlavB
        jets_dnn[idx_top, 1, 2] = deltaEta(j1.eta, sumjet.Eta())
        jets_dnn[idx_top, 1, 4] = deltaPhi(j1.phi, sumjet.Phi())
        jets_dnn[idx_top, 1, 6] = deltaPhi(j1.phi, fj_phi)
        jets_dnn[idx_top, 1, 7] = deltaEta(j1.eta, fj_eta)
        if scenario == "nominal":
            jets_dnn[idx_top, 0, 3] = j0.mass_nominal
            jets_dnn[idx_top, 0, 5] = j0.pt_nominal
            jets_dnn[idx_top, 1, 3] = j1.mass_nominal
            jets_dnn[idx_top, 1, 5] = j1.pt_nominal
        elif scenario == "jesTotalup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotalup
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotalup
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotalup
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotalup
        elif scenario == "jesTotaldown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jesTotaldown
            jets_dnn[idx_top, 0, 5] = j0.pt_jesTotaldown
            jets_dnn[idx_top, 1, 3] = j1.mass_jesTotaldown
            jets_dnn[idx_top, 1, 5] = j1.pt_jesTotaldown
        elif scenario == "jerup":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerup
            jets_dnn[idx_top, 0, 5] = j0.pt_jerup
            jets_dnn[idx_top, 1, 3] = j1.mass_jerup
            jets_dnn[idx_top, 1, 5] = j1.pt_jerup
        elif scenario == "jerdown":
            jets_dnn[idx_top, 0, 3] = j0.mass_jerdown
            jets_dnn[idx_top, 0, 5] = j0.pt_jerdown
            jets_dnn[idx_top, 1, 3] = j1.mass_jerdown
            jets_dnn[idx_top, 1, 5] = j1.pt_jerdown
                        
        if hasattr(j2,"pt"):
            jets_dnn[idx_top, 2, 0] = j2.area
            jets_dnn[idx_top, 2, 1] = j2.btagDeepFlavB
            jets_dnn[idx_top, 2, 2] = deltaEta(j2.eta, sumjet.Eta())#j2.#delta eta fj-jet
            jets_dnn[idx_top, 2, 4] = deltaPhi(j2.phi, sumjet.Phi())#j2.#delta phi fatjet-jet
            jets_dnn[idx_top, 2, 6] = deltaPhi(j2.phi, fj_phi)
            jets_dnn[idx_top, 2, 7] = deltaEta(j2.eta, fj_eta)
            if scenario == "nominal":
                jets_dnn[idx_top, 2, 3] = j2.mass_nominal
                jets_dnn[idx_top, 2, 5] = j2.pt_nominal
            elif scenario == "jesTotalup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotalup
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotalup
            elif scenario == "jesTotaldown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jesTotaldown
                jets_dnn[idx_top, 2, 5] = j2.pt_jesTotaldown
            elif scenario == "jerup":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerup
                jets_dnn[idx_top, 2, 5] = j2.pt_jerup
            elif scenario == "jerdown":
                jets_dnn[idx_top, 2, 3] = j2.mass_jerdown
                jets_dnn[idx_top, 2, 5] = j2.pt_jerdown
    return jets_dnn

def boost_PFC(pt_top,eta_top,phi_top,M_top,pt_PFC,eta_PFC,phi_PFC,M_PFC):
    pt_old = pt_PFC
    eta_old = eta_PFC
    phi_old = phi_PFC
    mass_old = M_PFC
    
    particle_old = ROOT.TLorentzVector()
    particle_old.SetPtEtaPhiM(pt_old, eta_old, phi_old, mass_old)

    pt_new_frame = pt_top
    eta_new_frame = eta_top
    phi_new_frame = phi_top
    mass_new_frame = M_top

    new_frame = ROOT.TLorentzVector()
    new_frame.SetPtEtaPhiM(pt_new_frame, eta_new_frame, phi_new_frame, mass_new_frame)

    boost_vector = new_frame.BoostVector()


    particle_old.Boost(-boost_vector.X(), -boost_vector.Y(), -boost_vector.Z())  


    pt_new = particle_old.Pt()
    eta_new = particle_old.Eta()
    phi_new = particle_old.Phi()
    mass_new = particle_old.M()

    return pt_new, eta_new, phi_new, mass_new


def fill_PFCs(n_PFCs, PFCs_dnn, PFCs, idx_top, pt_top, eta_top, phi_top, M_top): 
    for i,particle in enumerate(PFCs):
        if i<n_PFCs: #minore e non minore e uguale perchè parte da 0
            pt_boost, eta_boost, phi_boost, mass_boost = boost_PFC(pt_top, eta_top, phi_top, M_top, particle.pt ,particle.eta, particle.phi, particle.mass)
            PFCs_dnn[idx_top, i, 0] = pt_boost
            PFCs_dnn[idx_top, i, 1] = eta_boost
            PFCs_dnn[idx_top, i, 2] = phi_boost
            PFCs_dnn[idx_top, i, 3] = mass_boost
            PFCs_dnn[idx_top, i, 4] = particle.d0
            PFCs_dnn[idx_top, i, 5] = particle.dz
            PFCs_dnn[idx_top, i, 6] = particle.JetDeltaR
            PFCs_dnn[idx_top, i, 7] = particle.FatJetDeltaR
            PFCs_dnn[idx_top, i, 8] = particle.charge
            PFCs_dnn[idx_top, i, 9] = particle.pdgId
            PFCs_dnn[idx_top, i, 10] = particle.pvAssocQuality  
            PFCs_dnn[idx_top, i, 11] = particle.IsInJet
            PFCs_dnn[idx_top, i, 12] = particle.IsInFatJet
    return PFCs_dnn
    
def fill_SVs(n_SVs, SVs_dnn, SVs, idx_top, pt_top, eta_top, phi_top, M_top):
    for i, particle in enumerate(SVs):
        if i < n_SVs:
            pt_boost, eta_boost, phi_boost, mass_boost = boost_PFC(pt_top, eta_top, phi_top, M_top, particle.pt, particle.eta, particle.phi, particle.mass)
            SVs_dnn[idx_top, i, 0]   = pt_boost
            SVs_dnn[idx_top, i, 1]  = eta_boost
            SVs_dnn[idx_top, i, 2]  = phi_boost
            SVs_dnn[idx_top, i, 3]  = mass_boost
            SVs_dnn[idx_top, i, 4]  = particle.dxy
            SVs_dnn[idx_top, i, 5]  = particle.dxySig
            SVs_dnn[idx_top, i, 6]  = particle.JetDeltaR
            SVs_dnn[idx_top, i, 7]  = particle.FatJetDeltaR
            SVs_dnn[idx_top, i, 8]  = particle.charge 
            SVs_dnn[idx_top, i, 9]  = particle.dlen
            SVs_dnn[idx_top, i, 10] = particle.dlenSig
            SVs_dnn[idx_top, i, 11] = particle.ntracks
    return SVs_dnn


# path_to_model = "/afs/cern.ch/user/a/apuglia/TprimeAnalysis/NanoAODTools/python/postprocessing/final_trainings/"
# model_Mixed = 'training_pfsv_cnn_Mixed_01_09_2025/model_01_09_2025.h5'
# model_Resolved = 'training_resolved_31_08_2025/model_31_08_2025.h5'

# models                  = {}
# models['mixed'] = tf.keras.models.load_model(path_to_model + model_Mixed)
# models['resolved'] = tf.keras.models.load_model(path_to_model + model_Resolved)



class nanoTopevaluate_MultiScore(Module):
    def __init__(self, modelMix_path, modelRes_path, isMC=1, year=2022):
        self.modelMix_path = modelMix_path
        self.modelRes_path = modelRes_path
        self.modelMix      = tf.keras.models.load_model(modelMix_path)
        self.modelRes      = tf.keras.models.load_model(modelRes_path)
        self.isMC = isMC
        self.year = year
        if isMC : self.scenarios = ["nominal", "jesTotalup", "jesTotaldown", "jerup", "jerdown"]
        else: self.scenarios = ["nominal"]
        pass
 

    def beginJob(self):
        pass


    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        "Branch scores to tree"
        # self.out.branch("TopMixed_score2", "F", lenVar="nTopMixed")
        # self.out.branch(f"TopMixed_TopScore", "F", lenVar="nTopMixed")
        # Low Pt
        # self.out.branch("TopResolved_TopScore", "F", lenVar="nTopResolved")
        for scenario in self.scenarios:
            self.out.branch("TopMixed_QCDScore_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopMixed_TTScore_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopMixed_FTScore_"+scenario, "F", lenVar="nTopMixed")
            self.out.branch("TopResolved_QCDScore_"+scenario, "F", lenVar="nTopResolved")
            self.out.branch("TopResolved_TTScore_"+scenario, "F", lenVar="nTopResolved")
            self.out.branch("TopResolved_FTScore_"+scenario, "F", lenVar="nTopResolved")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass


    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        jets     = Collection(event,"Jet")
        njets    = len(jets)
        fatjets  = Collection(event,"FatJet")
        nfatjets = len(fatjets)

        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets             = len(goodjets)
        ngoodfatjets          = len(goodfatjets)
        
        tophighpt             = Collection(event, "TopMixed")
        toplowpt              = Collection(event, "TopResolved")
        
        PFCands      = Collection(event,"PFCands")
        SV_vertexes  = Collection(event, "SV")

        Indexes_pfc  = Collection(event, "IndexesPFC")
        Indexes_sv   = Collection(event, "IndexesSV") 
      
        n_SVs, n_PFCs = 3,20
        # loop su High Pt candidates per valutare lo score con i modelli corrispondenti
        if self.year == 2018:
            fj_dnn      = {s: np.zeros((int(len(tophighpt)), 12)) for s in self.scenarios}
        elif self.year in [2022,2023]:
            fj_dnn      = {s: np.zeros((int(len(tophighpt)), 12)) for s in self.scenarios}
        jets_dnn    = {s: np.zeros((int(len(tophighpt)), 3, 8)) for s in self.scenarios}
        mass_dnn    = {s: np.zeros((len(tophighpt), 3)) for s in self.scenarios}
        PFC_dnn     = np.zeros((len(tophighpt), n_PFCs, 13))
        SVs_dnn     = np.zeros((len(tophighpt), n_SVs , 12))
        for i, top in enumerate(tophighpt):
            if top.idxJet2==-1:
                j0, j1      = goodjets[top.idxJet0],goodjets[top.idxJet1]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4()+j1.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn = jets_dnn[s], j0=j0, j1=j1, j2=0, sumjet = sumjet,  fj_phi= fj.phi, fj_eta=fj.eta, idx_top=i, scenario = s)
                    fj_dnn[s]      = fill_fj(self.year, fj_dnn[s], fj, i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =None, fj = fj, scenario = s)
            elif top.idxFatJet==-1:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = ROOT.TLorentzVector()
                fj.SetPtEtaPhiM(0,0,0,0)
                sumjet      = j0.p4()+j1.p4()+j2.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None, scenario = s)
            else:
                j0, j1, j2  = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
                fj          = goodfatjets[top.idxFatJet]
                sumjet      = j0.p4() + j1.p4() +j2.p4()
                for s in self.scenarios:
                    jets_dnn[s]    = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.phi, fj.eta, i, scenario = s)
                    fj_dnn[s]      = fill_fj(self.year, fj_dnn[s], fj, i, scenario = s)
                    mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =j2, fj = fj, scenario = s)


            PFCs=[]
            pfc_indexes=[]
            sv_indexes = []
            SVs = []

            for idx in Indexes_pfc:    
                #print(idx.idxPFC)
                pfc_indexes.append(idx.idxPFC)
            
            for idx in Indexes_sv:
                sv_indexes.append(idx.idxSV)

            # print('pfc indexes: ', pfc_indexes)
            
            start_index_pfc = pfc_indexes.index(-(i+1))
            end_index_pfc = pfc_indexes.index(-(i+2))
            # print(start_index_pfc, end_index_pfc)
            idx_pfc_to_append = pfc_indexes[start_index_pfc+1:end_index_pfc]

            start_index_sv = sv_indexes.index(-(i + 1))
            end_index_sv   = sv_indexes.index(-(i + 2))
            idx_sv_to_append = sv_indexes[start_index_sv+1 : end_index_sv]
            # print(sv_indexes)
            # print(start_index_sv, end_index_sv)
            for particle in PFCands: #ciclo sulle particles
                if particle.Idx in idx_pfc_to_append:
                    PFCs.append(particle)
            
            for vertex in SV_vertexes:
                if vertex.Idx in idx_sv_to_append:
                    SVs.append(vertex)
            # print(SVs)
            fill_PFCs(n_PFCs= n_PFCs, PFCs_dnn= PFC_dnn, PFCs= PFCs, idx_top= i, pt_top= top.pt, eta_top= top.eta, phi_top= top.phi, M_top= top.mass)

            fill_SVs(n_SVs= n_SVs, SVs_dnn= SVs_dnn, SVs= SVs, idx_top= i, pt_top= top.pt, eta_top= top.eta, phi_top= top.phi, M_top= top.mass)

       
        ####### SCORES ####### 
        scores = []
        if len(tophighpt)!=0:
            # Concatenate jets_dnn[s] along the first axis
            jets_dnn_concatenated = np.concatenate(list(jets_dnn.values()), axis=0)
            fj_dnn_concatenated = np.concatenate(list(fj_dnn.values()), axis=0)
            mass_dnn_concatenated = np.concatenate(list(mass_dnn.values()), axis=0)

            # scores_ = model({"fatjet": fj_dnn_concatenated, "jet": jets_dnn_concatenated, "top": mass_dnn_concatenated}).numpy().flatten().tolist()
            scores_ = self.modelMix({"fatjet": fj_dnn_concatenated, "jet": jets_dnn_concatenated, "top": mass_dnn_concatenated}).numpy().flatten().tolist()
            scores = {}
            for i, s in enumerate(self.scenarios):
                scores[s] = scores_[0 + i*len(tophighpt): len(tophighpt)+i*len(tophighpt)]
            print('scores for : ', s, ' are: ', scores[s])
        else:
            # top_score2  = []
            scores = {s : [] for s in self.scenarios}

        # Branch the scores calculated #
        # self.out.fillBranch("TopHighPt_score2", top_score2)
        for s in self.scenarios:
            prob_false_tt = (scores[s][:,0]).flatten().tolist()
            prob_true_tt  = (scores[s][:,1]).flatten().tolist()
            prob_qcd      = (scores[s][:,2]).flatten().tolist()
            print('prob_false_tt is:' , prob_false_tt)
            print('prob true tt is: ', prob_true_tt)
            print('prob qcd is: ', prob_qcd)
            self.out.fillBranch(f"TopMixed_QCDScore"+s, prob_qcd)
            self.out.fillBranch(f"TopMixed_TTScore" +s, prob_true_tt)
            self.out.fillBranch(f"TopMixed_FTScore" +s, prob_false_tt)
            

        # loop su Low Pt candidates per valutare lo score con i modelli corrispondenti
        
        jets_dnn = {s: np.zeros((int(len(toplowpt)), 3, 8)) for s in self.scenarios}  
        mass_dnn = {s: np.zeros((len(toplowpt), 3)) for s in self.scenarios}
        PFC_dnn  = np.zeros((len(tophighpt), n_PFCs, 13))
        SVs_dnn  = np.zeros((len(tophighpt), n_SVs, 12))
        for i, top in enumerate(toplowpt):

            j0, j1, j2 = goodjets[top.idxJet0],goodjets[top.idxJet1],goodjets[top.idxJet2]
            fj = ROOT.TLorentzVector()
            fj.SetPtEtaPhiM(0,0,0,0)
            sumjet = j0.p4()+j1.p4()+j2.p4()
            for s in self.scenarios:
                jets_dnn[s] = fill_jets(self.year, jets_dnn[s], j0, j1, j2, sumjet, fj.Phi(), fj.Eta(), i, scenario = s)
                mass_dnn[s]    = fill_mass(mass_dnn=mass_dnn[s], idx_top=i, j0=j0, j1=j1, j2 =j2, fj = None, scenario = s)

            PFCs=[]
            pfc_indexes=[]
            sv_indexes = []
            SVs = []

            for idx in Indexes_pfc:    
                #print(idx.idxPFC)
                pfc_indexes.append(idx.idxPFC)
            
            for idx in Indexes_sv:
                sv_indexes.append(idx.idxSV)

            # print('pfc indexes: ', pfc_indexes)
            
            start_index_pfc = pfc_indexes.index(-(i+1))
            end_index_pfc = pfc_indexes.index(-(i+2))
            # print(start_index_pfc, end_index_pfc)
            idx_pfc_to_append = pfc_indexes[start_index_pfc+1:end_index_pfc]

            start_index_sv = sv_indexes.index(-(i + 1))
            end_index_sv   = sv_indexes.index(-(i + 2))
            idx_sv_to_append = sv_indexes[start_index_sv+1 : end_index_sv]
            # print(sv_indexes)
            # print(start_index_sv, end_index_sv)
            for particle in PFCands: #ciclo sulle particles
                if particle.Idx in idx_pfc_to_append:
                    PFCs.append(particle)
            
            for vertex in SV_vertexes:
                if vertex.Idx in idx_sv_to_append:
                    SVs.append(vertex)
            # print(SVs)
            fill_PFCs(n_PFCs= n_PFCs, PFCs_dnn= PFC_dnn, PFCs= PFCs, idx_top= i, pt_top= top.pt, eta_top= top.eta, phi_top= top.phi, M_top= top.mass)

            fill_SVs(n_SVs= n_SVs, SVs_dnn= SVs_dnn, SVs= SVs, idx_top= i, pt_top= top.pt, eta_top= top.eta, phi_top= top.phi, M_top= top.mass)

        
        
        
        if len(toplowpt)!=0:
            
            jets_dnn_concatenated = np.concatenate(list(jets_dnn.values()), axis=0)
            mass_dnn_concatenated = np.concatenate(list(mass_dnn.values()), axis=0)
            scores_res_ = self.modelRes({"jet":jets_dnn_concatenated, "top":mass_dnn_concatenated, "pfc": PFC_dnn, "sv":SVs_dnn}).numpy()
            scores_res = {}

            for i, s in enumerate(self.scenarios):
                scores_res[s] = scores_res_[0 + i*len(toplowpt): len(toplowpt) + i*len(toplowpt)]
            print("scores resolved for scenario: ", s, 'are: ', scores_res[s])

                # top_score_DNN[s] = top_score_DNN_[0 + i*len(toplowpt): len(toplowpt)+i*len(toplowpt)]
        else:
            scores_res = {s: [] for s in self.scenarios}
            # top_score_DNN = {s: [] for s in self.scenarios}

        for s in self.scenarios:
            prob_false_tt = (scores_res[s][:,0]).flatten().tolist()
            prob_true_tt  = (scores_res[s][:,1]).flatten().tolist()
            prob_qcd      = (scores_res[s][:,2]).flatten().tolist()
            print('prob_false_tt is:' , prob_false_tt)
            print('prob true tt is: ', prob_true_tt)
            print('prob qcd is: ', prob_qcd)
            self.out.fillBranch(f"TopResolved_QCDScore"+s, prob_qcd)
            self.out.fillBranch(f"TopResolved_TTScore" +s, prob_true_tt)
            self.out.fillBranch(f"TopResolved_FTScore" +s, prob_false_tt)
            
            # self.out.fillBranch("TopResolved_TopScore_"+s, top_score_DNN[s])
        return True
