# Analysis class for the analysis types
# analysis types will extend this class

from matplotlib.pyplot import cla
from abc import ABC, abstractmethod
from molecule import molecule

class Analysis:
    lines = []
    molecules = []
    data_lines = ''

    def __init__(self) -> None:
        pass

    # does copilot
    def run_get_function(function):
        try:
            function()
        except Exception as e:
            # convert function to string
            print("Error in function: " + str(function) + "with logfile: ") # TODO
        pass

    # sometimes a file has a header or a footer that makes the lines
    # difficult to parse, use this to get only the lines
    @abstractmethod
    def get_data_lines(self):
        pass

    def get_data(self, logfiles):
        for logfile in logfiles:
            global current_mol
            current_mol = molecule()

            with open(logfile, 'r') as logfile:
                # Read all lines from the file
                global lines
                lines = logfile.readlines()
                dataLines = ''
                self.get_data_lines()


                # get the name of the file, could be in any directory so just get the last part of the path
                current_mol.name = logfile.name.split('/')[-1].split('.')[0]
                self.get_status()
                if current_mol.status == 'Error':
                    # if there was an error, skip the rest of the file
                    self.molecules.append(current_mol)
                    continue

                self.get_homo_lumo()
                self.get_NPROC()
                self.get_electronic_energy()
                self.get_dipole()
                self.get_basis_set()

                # add the molecule to the list of molecules
                self.molecules.append(current_mol)

        # print molecules
        for mol in self.molecules:
            # print all the data for each molecule
            print(mol.name, mol.status, mol.HOMO, mol.LUMO, mol.GAP, mol.NPROC, mol.electronic_energy, mol.dipole_xyz, mol.dipole, mol.basis_sets, mol.functional, mol.stoichiometry, sep=', ')

        return self.molecules
    

    @abstractmethod
    def get_electronic_energy(self):
        pass

    @abstractmethod
    def get_dipole(self):
        pass

    @abstractmethod
    def get_basis_set(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def get_electronic_energy(self):
        pass

    #             get_homo_lumo()
#             get_NPROC()
#             get_electronic_energy()
#             get_dipole()
#             get_basis_set()

    @abstractmethod
    def get_data_lines(self):
        pass

    @abstractmethod
    def get_status(self):
        pass

    @abstractmethod
    def get_homo_lumo(self):
        pass

    @abstractmethod
    def get_NPROC():
        pass