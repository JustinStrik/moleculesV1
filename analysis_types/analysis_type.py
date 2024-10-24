# Analysis class for the analysis types
# analysis types will extend this class

from matplotlib.pyplot import cla
from abc import ABC, abstractmethod

class Analysis_Type:

    name = ""  # abstract variable for the name of the analysis type
    # abstract variable
    @abstractmethod
    def get_suffix():
        pass

    def __init__(self) -> None:
        pass

    # sometimes a file has a header or a footer that makes the lines
    # difficult to parse, use this to get only the lines

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