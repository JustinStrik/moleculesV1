# File name: Fe_CCNN_opt; 2. software name and version: ORCA 5.0.3; 3 total energy: -49837.34177 eV; 4. band gap: find the last showed ORBITAL ENERGIES, and in there, find the E(ev) of HOMO=0.0145eV (find it by check first zero value in OCC column) LUMO=-6.6352eV(it is number before LUMO), gap=HOMO-LUMO;  5. Charge: Find metal’s charge, in here is Fe. You can have a metal list to do this.  (1) MULLIKEN ATOMIC CHARGES: 0.541632 (2) LOEWDIN ATOMIC CHARGES: 0.212568. 


class molecule:
    def __init__(self):
        self.file_name = None
        self.software_name = None
        self.software_version = None
        self.total_energy = None
        self.band_gap = None
        self.homo = None
        self.lumo = None
        self.charge = None
        self.mulliken_atomic_charges = None
        self.loewdin_atomic_charges = None
        
current_mol = []

def get_file_name():
    pass

def get_orca_data(outfiles):
    # get all files that end with .log in the database directory
    # make sure the logfile name is the same as the path to the file
    # logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]

    # loop over all log files
    for outfile in outfiles:

        global current_mol
        current_mol = molecule()

        with open(outfile, 'r') as outfile:
            # Read all lines from the file
            global lines
            lines = outfile.readlines()

    
            
        
