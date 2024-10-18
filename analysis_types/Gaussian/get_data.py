# gets data from log files done with Gaussian
import os

from requests import get
from analysis_types.analysis_type import Analysis_Type
from molecule import molecule
from analysis import Analysis

# global logfile
logfile = ''
molecules = []
suffix = '.log'
# there is a data_lines string
# this contains the lines with the main data we are concerned with
# reduces the number of times we have to loop over the file

# class Gaussian is from  Analysis
class Gaussian(Analysis_Type):
    
    def get_suffix():
        return suffix
    
    get_suffix = '.log'

    def get_homo_lumo(): 
        linefound = False

        # Search for the last line containing "Alpha occ. eigenvalues"
        for line in reversed(lines):
            if linefound:
                # return to two lines before the line containing "Alpha occ. eigenvalues"
                line = lines[lines.index(line) + 2]
                values = line.split()[4:]
                # values[0] to float, not string
                current_mol.LUMO = float(values[0])
                # absolute value of the difference between homo and lumo
                # only to 5 decimal places of abs(current_mol.HOMO - current_mol.LUMO)
                current_mol.GAP = abs(current_mol.HOMO - current_mol.LUMO).__round__(5)
                break

            if 'Alpha  occ. eigenvalues --' in line:
                # Split the line into a list of values
                values = line.split()

                current_mol.HOMO = float(values[len(values) - 1]) # last value in the list
                linefound = True


    def get_dipole():
        current_mol.dipole_xyz = data_lines.split('RMSD=')[1].split('\\')[0]
        # convert to float RMSD=6.613e-05\\
        current_mol.dipole_xyz = float(current_mol.dipole_xyz.split('e')[0]) * 10**float(current_mol.dipole_xyz.split('e')[1])

        current_mol.dipole = data_lines.split('RMSF=')[1].split('\\')[0]
        current_mol.dipole = float(current_mol.dipole.split('e')[0]) * 10**float(current_mol.dipole.split('e')[1])



    # get whether or not there was an error, read only the bottom 100 lines of the file searching for 'Error termination'
    def get_status():
        for line in lines:
            if 'Error termination' in line:
                status = 'Error'
                break
            else:
                status = 'No Error'
        current_mol.status = status

    # line looks like  %NProcShared=16
    def get_NPROC():
        for line in lines:
            if '%NProcShared=' in line:
                current_mol.NPROC = float(line.split('=')[1])
                break

    def get_electronic_energy():
        # HF=-2623.6082922\
        current_mol.electronic_energy = float(data_lines.split('HF=')[1].split('\\')[0]).__round__(5)

    # first value is basis set, second is functional
    def get_basis_set():
        # no 'e' (exponent) should be in the basis set
        current_mol.basis_sets = float(data_lines.split('Dipole=')[1].split(',')[0])
        current_mol.functional = float(data_lines.split('Dipole=')[1].split(',')[1])
        current_mol.stoichiometry = float(data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0]) # cut off before //

    def get_data_lines():
        # data lines start with '1\1\ and end with @, so read all lines between those two
        # and add it to one string
        global data_lines
        data_lines = ''
        dataStart = False
        for line in lines:
            if '1\\1\\' in line or dataStart:
                dataStart = True
                data_lines += line
                if '@' in line:
                    # remove all the \n from the string
                    data_lines = data_lines.replace('\n', '')
                    data_lines = data_lines.replace(' ', '')
                    break    

    def get_data(logfiles):
        # get all files that end with .log in the database directory
        # make sure the logfile name is the same as the path to the file
        # logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]

        # loop over all log files
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
                get_status()
                if current_mol.status == 'Error':
                    # if there was an error, skip the rest of the file
                    molecules.append(current_mol)
                    continue

                get_homo_lumo()
                get_NPROC()
                get_electronic_energy()
                get_dipole()
                get_basis_set()

                # add the molecule to the list of molecules
                molecules.append(current_mol)

        # print molecules
        for mol in molecules:
            # print all the data for each molecule
            print(mol.name, mol.status, mol.HOMO, mol.LUMO, mol.GAP, mol.NPROC, mol.electronic_energy, mol.dipole_xyz, mol.dipole, mol.basis_sets, mol.functional, mol.stoichiometry, sep=', ')

        return molecules