import argparse

import numpy as np
import h5py

import scqubits as scq

E_C = 11
ECm = 50.0
E_L1 = 3.52
E_L2 = 3.52
E_La = 0.271
E_Lb = 0.266
E_J = 4.246
E_Ja = 5.837
E_Jb = 4.930
E_Ca = 0.892
E_Cb = 0.8655

flux_c, flux_s = 0.2662, 0.01768

FTC_grounded = scq.FluxoniumTunableCouplerGrounded(EJa=E_Ja, EJb=E_Jb, EC_twoqubit=np.inf,
                                               ECq1=E_Ca, ECq2=E_Cb, ELa=E_La, ELb=E_Lb,
                                               flux_a=0.5, flux_b=0.5, flux_c=0.30,
                                               fluxonium_cutoff=110, fluxonium_truncated_dim=7,
                                               ECc=E_C, ECm=ECm, EL1=E_L1, EL2=E_L2, EJC=E_J,
                                               fluxonium_minus_truncated_dim=7, h_o_truncated_dim=7)


def run_ftc_zz(flux_a, flux_b, flux_c, highest_exc_q=2, highest_exc_m=3, highest_exc_p=3):
    FTC_grounded.flux_c = flux_c
    (E00, E00_4, E_00_2) = FTC_grounded.fourth_order_energy_shift(
        0, 0, flux_a=flux_a, flux_b=flux_b, highest_exc_q=highest_exc_q, highest_exc_m=highest_exc_m,
        highest_exc_p=highest_exc_p, num_cpus=8)
    (E01, E01_4, E_01_2) = FTC_grounded.fourth_order_energy_shift(
        0, 1, flux_a=flux_a, flux_b=flux_b, highest_exc_q=highest_exc_q, highest_exc_m=highest_exc_m,
        highest_exc_p=highest_exc_p, num_cpus=8)
    (E10, E10_4, E_10_2) = FTC_grounded.fourth_order_energy_shift(
        1, 0, flux_a=flux_a, flux_b=flux_b, highest_exc_q=highest_exc_q, highest_exc_m=highest_exc_m,
        highest_exc_p=highest_exc_p, num_cpus=8)
    (E11, E11_4, E_11_2) = FTC_grounded.fourth_order_energy_shift(
        1, 1, flux_a=flux_a, flux_b=flux_b, highest_exc_q=highest_exc_q, highest_exc_m=highest_exc_m,
        highest_exc_p=highest_exc_p, num_cpus=8)
    return E11 - E10 - E01 + E00

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ftc zz")
    parser.add_argument(
        "--dev_amount", default="0.0", type=str, help="gamma deviation in GHz"
    )
    parser.add_argument("--idx", default=0, type=int, help="index that is unraveled")
    parser.add_argument(
        "--num_pts", default=5, type=int, help="number of points in gamma_dev_list"
    )
    parser.add_argument("--num_cpus", default=8, type=int, help="num cpus")
    args = parser.parse_args()
    run_gamma_dev(
        float(args.dev_amount), args.idx, args.num_pts, num_cpus=args.num_cpus
    )
