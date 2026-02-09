# Presety kalibracyjne (heurystyki): dryf / reforma / rozpad.
# Wszystkie wartości w [0,1] (poza n_* i krokami).
# Możesz je dalej stroić bez zmiany kodu.

PRESETS = {
    "dryf": dict(
        I_work=0.75,
        A_affect=0.55,
        R_power=0.80,
        C_conflict=0.85,
        G_regen=0.75,
        # wagi / dynamika
        alpha=0.25, beta=0.12, kappa=0.20,
        gamma=0.25, delta=0.12, eta=0.22,
        mu=0.25, nu=0.10,
        rho=0.10, sigma=0.22, tau=0.12,
        # progi
        TH_reform=0.72,
        TH_exit=0.35,
        e_min=0.18,
        s_min=0.18,
    ),
    "reforma": dict(
        I_work=0.45,
        A_affect=0.40,
        R_power=0.25,
        C_conflict=0.40,
        G_regen=0.20,
        alpha=0.20, beta=0.10, kappa=0.16,
        gamma=0.18, delta=0.10, eta=0.16,
        mu=0.14, nu=0.28,
        rho=0.08, sigma=0.12, tau=0.10,
        TH_reform=0.60,
        TH_exit=0.40,
        e_min=0.20,
        s_min=0.20,
    ),
    "rozpad": dict(
        I_work=0.85,
        A_affect=0.65,
        R_power=0.65,
        C_conflict=0.60,
        G_regen=0.90,
        alpha=0.30, beta=0.16, kappa=0.26,
        gamma=0.25, delta=0.14, eta=0.25,
        mu=0.22, nu=0.06,
        rho=0.04, sigma=0.10, tau=0.18,
        TH_reform=0.75,
        TH_exit=0.25,
        e_min=0.28,
        s_min=0.28,
    ),
}
