# molecule class
# has each of these data points: Name,status, time, NPROC, HOMO, LUMO, GAP,Electronic energy, Dipole xyz, Dipole,basis sets, functional,stoichiometry,spin multiplicity, S2, total charge, Mulliken, NBO
from analysis_types import analysis_type

class Molecule:
    name = ""
    status = ""
    upload_date = ""
    upload_time = ""
    uploader = ""
    analysis_type = None # will be obj
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
    identifier = ""

    def __init__(self) -> None:
        pass

    def __init__(self, uploader, analysis_type) -> None:
        self.uploader = uploader
        self.analysis_type = analysis_type

    def __init__(self, uploader, analysis_type, file_path) -> None:
        self.uploader = uploader
        self.analysis_type = analysis_type
        self.get_data(file_path)

    # runs proper get_data given analysis type
    def get_data(self, file_path):
        if hasattr(self.analysis_type, 'get_data'):
            self.analysis_type.get_data(self, file_path) # adds info to mol
        else:
            if (self.analysis_type == None):
                raise AttributeError(f"Molecule {self.name} does not have an analysis type, somehow.")
            else:
                raise AttributeError(f"In molecule {self.name}, {self.analysis_type} does not have a get_data method")
