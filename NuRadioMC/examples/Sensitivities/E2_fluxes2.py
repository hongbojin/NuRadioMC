import matplotlib.pyplot as plt
import numpy as np
from NuRadioReco.utilities import units
from NuRadioMC.utilities import fluxes
import os

energyBinsPerDecade = 2.
plotUnitsEnergy = units.GeV
plotUnitsFlux = units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1

# Unless you would like to work with the layout or the models/data from other experiments,
# you don't need to change anything below here
# --------------------------------------------------------------------
# Other planned experiments

# GRAND white paper,
# numerical values, Bustamante
GRAND_energy = np.array(([48192296.5, 67644231.1, 94947581.6, 133271428.0, 187063990.0, 262568931.0, 368550053.0, 517308507.0, 726110577.0, 1019191760.0, 1430569790.0, 2007992980.0, 2818482440.0, 3956111070.0, 5552922590.0, 7794257720.0, 10940266600.0, 15356104100.0, 21554313200.0, 30254315500.0, 42465913900.0,
                          59606499400.0, 83665567300.0, 117435636000.0, 164836371000.0, 231369543000.0, 324757606000.0, 455840043000.0, 639831498000.0, 898087721000.0, 1260584320000.0, 1769396010000.0, 2483580190000.0, 3486031680000.0, 4893104280000.0, 6868115880000.0, 9640304610000.0, 13531436400000.0, 18993151900000.0, 26659388600000.0]))

GRAND_energy *= units.GeV

GRAND_10k = np.array(([8.41513361e-08, 7.38147706e-08, 5.69225180e-08, 3.46647934e-08,
                       1.95651137e-08, 1.40651565e-08, 1.25782087e-08, 1.24621707e-08,
                       1.31123151e-08, 1.45812119e-08, 1.65528260e-08, 1.91930521e-08,
                       2.31554429e-08, 2.87477813e-08, 3.55164030e-08, 4.42563884e-08,
                       5.63965197e-08, 7.45183330e-08, 1.01159657e-07, 1.39040439e-07,
                       1.98526677e-07, 2.61742251e-07, 3.40870828e-07, 4.82745531e-07,
                       6.55876763e-07, 9.07706655e-07, 1.67125879e-06, 1.76142511e-05,
                       2.55022320e-04, 1.88371074e-03, 6.71431813e-03, 1.14286198e-02,
                       1.14294614e-02, 1.72447830e-02, 7.48579143e-02, 3.31883351e-01,
                       8.57786094e-01, 1.24824516e+00, 1.42294586e+00, 1.80135089e+00]))

GRAND_10k *= (units.GeV* units.cm**-2 * units.second**-1 * units.sr**-1)
#GRAND_10k /= 2 #halfdecade bins
GRAND_10k *= energyBinsPerDecade

GRAND_200k = np.array(([4.26219753e-09, 3.58147708e-09, 2.75670137e-09, 1.85254042e-09,
                        1.13825106e-09, 7.70141315e-10, 6.51758930e-10, 6.35878242e-10,
                        6.69261628e-10, 7.37439217e-10, 8.38784832e-10, 9.81688683e-10,
                        1.18493794e-09, 1.45699379e-09, 1.80867621e-09, 2.26948852e-09,
                        2.91952068e-09, 3.86790849e-09, 5.24530715e-09, 7.31211288e-09,
                        9.98848945e-09, 1.33523293e-08, 1.80893102e-08, 2.46582187e-08,
                        3.41054825e-08, 5.39140368e-08, 3.36553610e-07, 4.57179717e-06,
                        3.59391218e-05, 1.47550853e-04, 3.33777479e-04, 4.92873322e-04,
                        6.68381070e-04, 1.72553598e-03, 7.06643413e-03, 2.10754560e-02,
                        4.06319101e-02, 5.88162853e-02, 7.45423652e-02, 8.83700084e-02]))

GRAND_200k *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)

# RADAR proposed from https://arxiv.org/pdf/1710.02883.pdf

Radar = np.array(([
    (1.525e+01, 6.870e-09, 3.430e-07),
    (1.575e+01, 9.797e-10, 3.113e-08),
    (1.625e+01, 4.728e-09, 1.928e-07),
    (1.675e+01, 6.359e-09, 3.706e-07),
    (1.725e+01, 9.128e-09, 8.517e-07),
    (1.775e+01, 1.619e-08, 1.835e-06),
    (1.825e+01, 2.995e-08, 2.766e-06),
    (1.875e+01, 5.562e-08, 8.253e-06),
    (1.925e+01, 1.072e-07, 1.849e-05)]))

Radar[:, 0] = 10**Radar[:, 0] * units.eV
Radar[:, 1] *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
Radar[:, 2] *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)

# --------------------------------------------------------------------
# Published data and limits

# IceCube
# log (E^2 * Phi [GeV cm^02 s^-1 sr^-1]) : log (E [Gev])
# Phys Rev D 98 062003 (2018)
# Numbers private correspondence Shigeru Yoshida
ice_cube_limit = np.array(([
    (6.199999125, -7.698484687),
    (6.299999496, -8.162876678),
    (6.400000617, -8.11395291),
    (6.500000321, -8.063634144),
    (6.599999814, -8.004841781),
    (6.699999798, -7.944960162),
    (6.799999763, -7.924197388),
    (6.899999872, -7.899315263),
    (7.299999496, -7.730561153),
    (7.699999798, -7.670680637),
    (8.100001583, -7.683379711),
    (8.500000321, -7.748746801),
    (8.899999872, -7.703060304),
    (9.299999496, -7.512907553),
    (9.699999798, -7.370926525),
    (10.10000158, -7.134626026),
    (10.50000032, -6.926516638),
    (10.89999987, -6.576523031)
]))

ice_cube_limit[:, 0] = 10**ice_cube_limit[:, 0] * units.GeV
ice_cube_limit[:, 1] = 10**ice_cube_limit[:, 1] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
ice_cube_limit[:, 1] *= energyBinsPerDecade

# Fig. 2 from PoS ICRC2017 (2018) 981
# IceCube preliminary
# E (GeV); E^2 dN/dE (GeV cm^-2 s-1 sr-1); yerror down; yerror up
ice_cube_hese = np.array(([

    (6.526e+04,  2.248e-08,  9.96e-9,  1.123e-8),
    (1.409e+05,  2.692e-08,  5.91e-9,  7.56e-9),
    (3.041e+05,  7.631e-09,  3.746e-9, 4.61e-9),
    (6.644e+05,  2.022e-09,  7.03e-10, 0.),
    (1.434e+06,  5.205e-09,  3.183e-9,  4.57e-9),
    (3.096e+06,  4.347e-09,  3.142e-9,  5.428e-9),
    (6.684e+06,  1.544e-09,  5.37e-10, 0.),
    (1.46e+07,  4.063e-09,   1.353e-9, 0.),
    (3.153e+07,  6.093e-09,  2.03e-9,  0.),
    (6.806e+07,  1.046e-08,  3.641e-9, 0.)
]))



ice_cube_hese[:, 0] = ice_cube_hese[:, 0] * units.GeV
ice_cube_hese[:, 1] = ice_cube_hese[:, 1] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
ice_cube_hese[:, 1] *= 3
ice_cube_hese[:, 2] = ice_cube_hese[:, 2] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
ice_cube_hese[:, 2] *=  3
ice_cube_hese[:, 3] = ice_cube_hese[:, 3] * (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
ice_cube_hese[:, 3] *= 3

# Ice cube


def ice_cube_nu_fit(energy, slope=-2.13, offset=0.9):
    flux = 3 * offset * (energy / (100 * units.TeV))**slope * 1e-18 * \
        (units.GeV**-1 * units.cm**-2 * units.second**-1 * units.sr**-1)
    return flux


def get_ice_cube_mu_range():
    energy = np.arange(1e5, 5e6, 1e5) * units.GeV
    upper = np.maximum(ice_cube_nu_fit(energy, offset=0.9, slope=-2.), ice_cube_nu_fit(energy, offset=1.2, slope=-2.13))
    upper *= energy**2
    lower = np.minimum(ice_cube_nu_fit(energy, offset=0.9, slope=-2.26),
                       ice_cube_nu_fit(energy, offset=0.63, slope=-2.13))
    lower *= energy**2
    return energy, upper, lower


def get_ice_cube_hese_range():
    energy = np.arange(1e5, 5e6, 1e5) * units.GeV
    upper = np.maximum(ice_cube_nu_fit(energy, offset=2.46, slope=-2.63),
                       ice_cube_nu_fit(energy, offset=2.76, slope=-2.92))
    upper *= energy**2
    lower = np.minimum(ice_cube_nu_fit(energy, offset=2.46, slope=-3.25),
                       ice_cube_nu_fit(energy, offset=2.16, slope=-2.92))
    lower *= energy**2
    return energy, upper, lower


# ANITA I - III
# Phys. Rev. D 98, 022001 (2018)
anita_limit = np.array(([
    (9.94e17,	3.79e-14 * 9.94e17 / 1e9),
    (2.37e18,	2.15e-15 * 2.37e18 / 1e9),
    (5.19e18,	2.33e-16 * 5.19e18 / 1e9),
    (1.10e19,	3.64e-17 * 1.10e19 / 1e9),
    (3.55e19,	4.45e-18 * 3.55e19 / 1e9),
    (1.11e20,	9.22e-19 * 1.11e20 / 1e9),
    (4.18e20,	2.97e-19 * 4.18e20 / 1e9),
    (9.70e20,	1.62e-19 * 9.70e20 / 1e9)
]))

anita_limit[:, 0] *= units.eV
anita_limit[:, 1] *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
anita_limit[:, 1] /= 2
anita_limit[:, 1] *= energyBinsPerDecade


# Auger neutrino limit
# Auger 9 years, all flavour (x3)
auger_limit = np.array(([
    (16.7523809524, 4.462265901e-07),
    (17.2523809524, 1.103901153e-07),
    (17.7523809524, 6.487559078e-08),
    (18.2380952381, 7.739545498e-08),
    (18.7523809524, 1.387743075e-07),
    (19.2571428571, 3.083827665e-07),
    (19.7523809524, 7.467202523e-07),
    (20.2476190476, 1.998499395e-06)
]))
auger_limit[:, 0] = 10 ** auger_limit[:, 0] * units.eV
auger_limit[:, 1] *= (units.GeV * units.cm**-2 * units.second**-1 * units.sr**-1)
auger_limit[:, 1] /= 2  # half-decade binning
auger_limit[:, 1] *= energyBinsPerDecade

# get 10% proton flux
def get_proton_10(energy):
    vanVliet_reas = np.loadtxt(os.path.join(os.path.dirname(__file__), "ReasonableNeutrinos1.txt"))
    E = vanVliet_reas[0, :] * plotUnitsEnergy
    f = vanVliet_reas[1, :] * plotUnitsFlux / E**2
    from scipy.interpolate import interp1d
    getE = interp1d(E, f)
    return getE(energy)
    


def get_E2_limit_figure(show_ice_cube_EHE_limit=True,
                        show_ice_cube_HESE=True,
                        show_ice_cube_mu=True,
                        show_anita_I_III_limit=True,
                        show_auger_limit=True,
                        show_neutrino_best_fit=True,
                        show_neutrino_best_case=True,
                        show_neutrino_worst_case=True,
                        show_grand_10k=True,
                        show_grand_200k=True,
                        show_radar=False):

    # Limit E2 Plot
    # ---------------------------------------------------------------------------
    fig, ax = plt.subplots(1, 1, figsize=(7, 8))

    # Neutrino Models

    Heinze_band = np.loadtxt(os.path.join(os.path.dirname(__file__), "talys_neu_bands.out"))
    best_fit, = ax.plot(Heinze_band[:, 0], Heinze_band[:, 1] * Heinze_band[:, 0]**2, c='k',
                        label=r'Best fit UHECR ($\pm$ 3$\sigma$), Heinze et al.', linestyle='-.')

    Heinze_evo = np.loadtxt(os.path.join(os.path.dirname(__file__), "talys_neu_evolutions.out"))
    ax.fill_between(Heinze_evo[:, 0], Heinze_evo[:, 5] * Heinze_evo[:, 0] **
                    2, Heinze_evo[:, 6] * Heinze_evo[:, 0]**2, color='0.8')

    vanVliet_max_1 = np.loadtxt(os.path.join(os.path.dirname(__file__), "MaxNeutrinos1.txt"))
    vanVliet_max_2 = np.loadtxt(os.path.join(os.path.dirname(__file__), "MaxNeutrinos2.txt"))
    vanVliet_reas = np.loadtxt(os.path.join(os.path.dirname(__file__), "ReasonableNeutrinos1.txt"))

    vanVliet_max = np.maximum(vanVliet_max_1[1, :], vanVliet_max_2[1, :])

    prot10, = ax.plot(vanVliet_reas[0, :], vanVliet_reas[1, :],
                      label=r'10% protons in UHECRs, van Vliet et al.', linestyle=':', color='darkmagenta')

    prot = ax.fill_between(vanVliet_max_1[0,:],vanVliet_max,vanVliet_reas[1,:]/10,color='thistle',alpha=0.5,label=r'not excluded from UHECRs')

    first_legend = plt.legend(handles=[best_fit, prot, prot10], loc=4)

    plt.gca().add_artist(first_legend)
    #-----------------------------------------------------------------------

    if show_grand_10k:
        ax.plot(GRAND_energy / plotUnitsEnergy, GRAND_10k / plotUnitsFlux, linestyle="--", color='saddlebrown')
        ax.annotate('GRAND 10k',
                    xy=(0.3e10, 1.1e-7 /2 * energyBinsPerDecade), xycoords='data',
                    horizontalalignment='left', color='saddlebrown', rotation=50)

    if show_grand_200k:
        ax.plot(GRAND_energy / plotUnitsEnergy, GRAND_200k / plotUnitsFlux, linestyle="--", color='saddlebrown')
        ax.annotate('GRAND 200k',
                    xy=(1e10, 6e-9 /2 * energyBinsPerDecade), xycoords='data',
                    horizontalalignment='left', color='saddlebrown', rotation=50)
    if show_radar:
        ax.fill_between(Radar[:, 0] / plotUnitsEnergy, Radar[:, 1] / plotUnitsFlux,
                        Radar[:, 2] / plotUnitsFlux, facecolor='None', hatch='x', edgecolor='0.8')
        ax.annotate('Radar',
                    xy=(1e9, 4.5e-8), xycoords='data',
                    horizontalalignment='left', color='0.7', rotation=45)

    if show_ice_cube_EHE_limit:
        ax.plot(ice_cube_limit[:, 0] / plotUnitsEnergy, ice_cube_limit[:, 1] / plotUnitsFlux, color='dodgerblue')
        ax.annotate('IceCube',
                    xy=(3e5, 1e-7), xycoords='data',
                    horizontalalignment='left', verticalalignment='center', color='dodgerblue', rotation=0)

    if show_ice_cube_HESE:
        # data points
        uplimit = np.copy(ice_cube_hese[:, 3])
        uplimit[np.where(ice_cube_hese[:, 3] == 0)] = 1
        uplimit[np.where(ice_cube_hese[:, 3] != 0.)] = 0

        ax.errorbar(ice_cube_hese[:, 0] / plotUnitsEnergy, ice_cube_hese[:, 1] / plotUnitsFlux, yerr=ice_cube_hese[:,2:].T / plotUnitsFlux,
                    uplims=uplimit, color='dodgerblue', marker='o', ecolor='dodgerblue', linestyle='None')

        # hese fit
        ice_cube_hese_range = get_ice_cube_hese_range()
        ax.fill_between(ice_cube_hese_range[0] / plotUnitsEnergy, ice_cube_hese_range[1] / plotUnitsFlux,
                        ice_cube_hese_range[2] / plotUnitsFlux, hatch='//', edgecolor='dodgerblue', facecolor='azure')
        plt.plot(ice_cube_hese_range[0] / plotUnitsEnergy, ice_cube_nu_fit(ice_cube_hese_range[0],
                                                                           offset=2.46, slope=-2.92) * ice_cube_hese_range[0]**2 / plotUnitsFlux, color='dodgerblue')

    if show_ice_cube_mu:
        # mu fit
        ice_cube_mu_range = get_ice_cube_mu_range()
        ax.fill_between(ice_cube_mu_range[0] / plotUnitsEnergy, ice_cube_mu_range[1] / plotUnitsFlux,
                        ice_cube_mu_range[2] / plotUnitsFlux, hatch='\\', edgecolor='dodgerblue', facecolor='azure')
        plt.plot(ice_cube_mu_range[0] / plotUnitsEnergy,
                 ice_cube_nu_fit(ice_cube_mu_range[0], offset=0.9, slope=-2.13) * ice_cube_mu_range[0]**2 / plotUnitsFlux,
                 color='dodgerblue')

    if show_anita_I_III_limit:
        ax.plot(anita_limit[:, 0] / plotUnitsEnergy, anita_limit[:, 1] / plotUnitsFlux, color='darkorange')
        ax.annotate('ANITA I - III',
                    xy=(5e9, 0.5e-6 /2 * energyBinsPerDecade), xycoords='data',
                    horizontalalignment='right', color='darkorange')

    if show_auger_limit:
        ax.plot(auger_limit[:, 0] / plotUnitsEnergy, auger_limit[:, 1] / plotUnitsFlux, color='forestgreen')
        ax.annotate('Auger',
                    xy=(1.2e8, 2.1e-7 /2 * energyBinsPerDecade), xycoords='data',
                    horizontalalignment='left', color='forestgreen', rotation=0)

    ax.set_yscale('log')
    ax.set_xscale('log')

    ax.set_xlabel(r'Neutrino Energy [GeV]')
    ax.set_ylabel(r'$E^2\Phi$ [GeV cm$^{-2}$ s$^{-1}$ sr$^{-1}$]')

    ax.set_ylim(1e-11, 2e-6)
    ax.set_xlim(1e5, 1e11)

    plt.tight_layout()
    return fig, ax


def add_limit(ax, limit_labels, E, Veff, n_stations, label, livetime=3*units.year, fmt='-', color='C0'):
    E = np.array(E)
    Veff = np.array(Veff)
    limit = fluxes.get_limit_e2_flux(energy = E,
                                     veff = Veff,
                                     livetime = livetime,
                                     signalEff = n_stations,
                                     energyBinsPerDecade=energyBinsPerDecade,
                                     upperLimOnEvents=2.44,
                                     nuCrsScn='ctw')

    _plt, = ax.plot(E/plotUnitsEnergy,limit/ plotUnitsFlux, fmt, color=color,
                    label="{2}: {0} stations, {1} years".format(n_stations,int(livetime/units.year),label),
                    linewidth=3)
    limit_labels.append(_plt)
    return limit_labels

def add_limit_band(ax, limit_labels, E, Veff1, Veff2, n_stations, label, livetime=3*units.year, color='C0'):
    E = np.array(E)
    Veff1 = np.array(Veff1)
    Veff2 = np.array(Veff2)
    limit1 = fluxes.get_limit_e2_flux(energy = E,
                                     veff = Veff1,
                                     livetime = livetime,
                                     signalEff = n_stations,
                                     energyBinsPerDecade=energyBinsPerDecade,
                                     upperLimOnEvents=2.44,
                                     nuCrsScn='ctw')
    limit2 = fluxes.get_limit_e2_flux(energy = E,
                                      veff = Veff2,
                                     livetime = livetime,
                                     signalEff = n_stations,
                                     energyBinsPerDecade=energyBinsPerDecade,
                                     upperLimOnEvents=2.44,
                                     nuCrsScn='ctw')

    ax.fill_between(E/plotUnitsEnergy,limit1/ plotUnitsFlux,limit2/ plotUnitsFlux,
                            color=color, alpha=0.5, 
                            label="{2}: {0} stations, {1} years".format(n_stations,int(livetime/units.year),label))
#     limit_labels.append(_plt)
    return limit_labels

if __name__=="__main__":
    strawman_veff_pa = np.array(( [1.00000000e+16, 3.16227766e+16, 1.00000000e+17, 3.16227766e+17, 1.00000000e+18, 3.16227766e+18, 1.00000000e+19, 3.16227766e+19],
                              [1.82805666e+07, 1.34497197e+08, 6.32044851e+08, 2.20387046e+09, 4.86050340e+09, 8.18585201e+09, 1.25636305e+10, 1.83360237e+10])).T

    strawman_veff_pa[:,0] *= units.eV
    strawman_veff_pa[:,1] *= units.m**3 * units.sr
    
    strawman_pa_label = 'Strawman + PA@15m@2s'
    fig, ax = get_E2_limit_figure()
    labels =[]
    labels = add_limit(ax, labels, strawman_veff_pa[:,0],strawman_veff_pa[:,1], 270, strawman_pa_label)
    plt.legend(handles=labels, loc=2)
    plt.show()
