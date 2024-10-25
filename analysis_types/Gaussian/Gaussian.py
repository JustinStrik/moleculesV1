# gets data from log files done with Gaussian
import os

from requests import get
from analysis_types.analysis_type import Analysis_Type
from molecule import Molecule
import datetime
# from analysis import Analysis

# global logfile
logfile = ''
# molecules = []
suffix = '.log'

# there is a data_lines string
# this contains the lines with the main data we are concerned with
# reduces the number of times we have to loop over the file

# class Gaussian is from  Analysis
class Gaussian(Analysis_Type):
    
    mol = None # molecule currently being analyzed
    name = 'Gaussian'
    suffix = '.log'

    def get_suffix(self):
        return suffix
    
    def check_if_correct_file_type(self, file):
        # to ensure the file is the correct type, have it check to see if the file
        # passes a test that only the correct file type would pass

        # get the first line of the file
        with open(file, 'r') as f:
            lines = f.readlines()
            return 'Entering Gaussian System' in lines[0]
    
    def get_homo_lumo(self): 
        linefound = False

        # Search for the last line containing "Alpha occ. eigenvalues"
        for line in reversed(lines):
            if linefound:
                # return to two lines before the line containing "Alpha occ. eigenvalues"
                line = lines[lines.index(line) + 2]
                values = line.split()[4:]
                # values[0] to float, not string
                self.mol.LUMO = float(values[0])
                # absolute value of the difference between homo and lumo
                # only to 5 decimal places of abs(mol.HOMO - mol.LUMO)
                self.mol.GAP = abs(self.mol.HOMO - self.mol.LUMO).__round__(5)
                break

            if 'Alpha  occ. eigenvalues --' in line:
                # Split the line into a list of values
                values = line.split()

                self.mol.HOMO = float(values[len(values) - 1]) # last value in the list
                linefound = True


    def get_dipole(self):
        self.mol.dipole_xyz = data_lines.split('RMSD=')[1].split('\\')[0]
        # convert to float RMSD=6.613e-05\\
        self.mol.dipole_xyz = float(self.mol.dipole_xyz.split('e')[0]) * 10**float(self.mol.dipole_xyz.split('e')[1])

        self.mol.dipole = data_lines.split('RMSF=')[1].split('\\')[0]
        self.mol.dipole = float(self.mol.dipole.split('e')[0]) * 10**float(self.mol.dipole.split('e')[1])



    # get whether or not there was an error, read only the bottom 100 lines of the file searching for 'Error termination'
    def get_status(self):
        for line in lines:
            if 'Error termination' in line:
                status = 'Error'
                break
            else:
                status = 'No Error'
        self.mol.status = status

    # line looks like  %NProcShared=16
    def get_NPROC(self):
        for line in lines:
            if '%NProcShared=' in line:
                self.mol.NPROC = float(line.split('=')[1])
                break

    def get_electronic_energy(self):
        # HF=-2623.6082922\
        self.mol.electronic_energy = float(data_lines.split('HF=')[1].split('\\')[0]).__round__(5)

    # first value is basis set, second is functional
    def get_basis_set(self):
        # no 'e' (exponent) should be in the basis set
        self.mol.basis_sets = float(data_lines.split('Dipole=')[1].split(',')[0])
        self.mol.functional = float(data_lines.split('Dipole=')[1].split(',')[1])
        self.mol.stoichiometry = float(data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0]) # cut off before //

    def get_method(self):
        # after FOpt\ but before the next \
        self.mol.functional = data_lines.split('FOpt\\')[1].split('\\')[0]
        self.mol.basis_sets = data_lines.split('FOpt\\')[1].split('\\')[1]

    def get_time(self):
        self.mol.time = ''
        # if line contains "elapsed time:"
        for line in lines:
            if 'Job cpu time:' in line:
                # get the time
                time_data = line.split('Job cpu time:       ')[1].split(' ')
                for data in time_data:
                    if data == '':
                        time_data.remove(data)

                # split '0 days  0 hours 21 minutes  6.9 seconds.\n' into just 0:0:21:6.9
                self.mol.cpu_time = time_data[0] + ':' + time_data[2] + ':' + time_data[4] + ':' + time_data[6]
                continue

            if 'Elapsed time:' in line:
                # get the time
                time_data = line.split('Elapsed time:       ')[1].split(' ')
                for data in time_data:
                    if data == '':
                        time_data.remove(data)
                # split '0 days  0 hours 21 minutes  6.9 seconds.\n' into just 0:0:21:6.9
                self.mol.elapsed_time = time_data[0] + ':' + time_data[2] + ':' + time_data[4] + ':' + time_data[6]
                break

    def get_data_lines(self):
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

    def get_upload_date_and_time(self):
        self.mol.upload_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.mol.upload_time = datetime.datetime.now().strftime("%H:%M:%S") 

    def get_opt_xyz(self):
        xyz_data = data_lines.split('\\\\')[3]
        # read and ignore (pop) first 4 characters
        xyz_data = xyz_data.split('\\')
        self.mol.total_charge = int(xyz_data[0].split(',')[0])
        self.mol.spin_multiplicity = int(xyz_data[0].split(',')[1])
        xyz_data.remove(xyz_data[0])
        xyz_atoms = []

        for atom in xyz_data:
            vals = atom.split(',')
            new_atom = {}
            new_atom['atom'] = vals[0]
            new_atom['x'] = float(vals[1])
            new_atom['y'] = float(vals[2])
            new_atom['z'] = float(vals[3])
            xyz_atoms.append(new_atom)

        self.mol.opt_xyz = xyz_atoms

        
    def get_charges(self):
        found_mulliken, found_hirshfeld = False, False

        # reverse iterate over lines
        for line in reversed(lines):
            if (found_hirshfeld and found_mulliken):
                return
            
            # line just contains "Mulliken charges"
            if ('Mulliken charges' in line and not found_mulliken):
                found_mulliken = True      
                # go down (not reverse) and scan all lines in this format     
                # only intterested in the last value in the line (charge)

                atom_index = 0
                for chargeline in lines[lines.index(line) + 2:]:
                    values = chargeline.split()
                    if values == []:
                        break
                    # or if first index of values isnt an int
                    if chargeline == '\n' or atom_index >= len(self.mol.opt_xyz) or not values[0].isdigit():
                        break

                    charge_val = float(values[-1])
                    atom_index = int(values[0]) - 1
                    self.mol.opt_xyz[atom_index]['mulliken'] = (float(charge_val))
                    atom_index += 1

            # if line contains "Hirshfeld charges"
            if ('Hirshfeld charges' in line and not found_hirshfeld):
                found_hirshfeld = True
                atom_index = 0

                for chargeline in lines[lines.index(line) + 2:]:
                    # break if line is empty or we have reached the end of the opt_xyz dictionary
                    if chargeline == ' \n' or atom_index >= len(self.mol.opt_xyz):
                        break
                    values = chargeline.split()
                    # add new property 'hirshfeld to the opt_xyz dictionary
                    charge_val = float(values[-1])
                    atom_index = int(values[0]) - 1
                    self.mol.opt_xyz[atom_index]['hirshfeld'] = charge_val
                    atom_index += 1 # will break if we access the value before the last

    def make_identifier(self):
        # doc_id = f'{molecule["name"]}_{molecule["basis_sets"]}_{molecule["functional"]}'
        self.mol.identifier = f'{self.mol.name}_{self.mol.basis_sets}_{self.mol.functional}'

    def get_data(self, mol, file_path):
        # get all files that end with .log in the database directory
        # make sure the logfile name is the same as the path to the file
        # logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]

        # loop over all log files
        

        with open(file_path, 'r') as mol_file:
            # Read all lines from the file
            global lines
            lines = mol_file.readlines()
            self.mol = mol
            dataLines = ''
            self.get_data_lines()


            # get the name of the file, could be in any directory so just get the last part of the path
            self.mol.name = mol_file.name.split('/')[-1].split('.')[0]
            self.get_status()
            if self.mol.status == 'Error':
                # if there was an error, skip the rest of the file
                return self.mol

            self.get_homo_lumo()
            self.get_NPROC()
            self.get_electronic_energy()
            self.get_dipole()
            self.get_time()
            self.get_method()
            self.get_basis_set()
            self.get_upload_date_and_time()
            self.get_opt_xyz()
            self.get_charges()
            self.make_identifier()

            return self.mol

    # # print molecules
    # for mol in molecules:
    #     # print all the data for each molecule
    #     print(self.mol.name, self.mol.status, self.mol.HOMO, self.mol.LUMO, self.mol.GAP, self.mol.NPROC, self.mol.electronic_energy, self.mol.dipole_xyz, self.mol.dipole, self.mol.basis_sets, self.mol.functional, self.mol.stoichiometry, sep=', ')

    #     return molecules