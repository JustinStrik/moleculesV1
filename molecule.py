# molecule class
# has each of these data points: Name,status, time, NPROC, HOMO, LUMO, GAP,Electronic energy, Dipole xyz, Dipole,basis sets, functional,stoichiometry,spin multiplicity, S2, total charge, Mulliken, NBO

from analysis_types import analysis_type


class molecule:
    name = ""
    status = ""
    upload_date = ""
    upload_time = ""
    uploader = ""
    analysis_type = ""
    cpu_time = ""
    elapsed_time = ""
    NPROC: float = 0
    HOMO: float = 0
    LUMO: float = 0
    GAP: float = 0
    electronic_energy: float = 0
    dipole_xyz = ""
    opt_xyz = []
    dipole = 0
    basis_sets = ""
    functional = ""
    stoichiometry = ""
    spin_multiplicity: int = 0
    S2 = 0
    total_charge = 0
    # Mulliken = ""
    NBO = ""