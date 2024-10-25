# gets data from output files done with Orca
# this template is from Gaussian Analysis
from analysis_types.analysis_type import Analysis_Type
import datetime

# there is a data_lines string
# this contains the lines with the main data we are concerned with
# reduces the number of times we have to loop over the file

# class Orca is from  Analysis
class Orca(Analysis_Type):
    
    mol = None # molecule currently being analyzed
    name = 'Orca'
    suffix = '.log' # TODO change to the suffix of the output files for Orca
    data_lines = '' # string containing all the data lines from the file
    lines = [] # all the lines from the file

    def get_suffix(self):
        return self.suffix

    def get_homo_lumo(self): 
        # TODO replace with function to get homo and lumo from Orca analysis output
        print(f"get_homo_lumo not implemeneted yet in {self.mol.name}")
        pass
        linefound = False

        # Search for the last line containing "Alpha occ. eigenvalues"
        for line in reversed(self.lines):
            if linefound:
                # return to two lines before the line containing "Alpha occ. eigenvalues"
                line = self.lines[self.lines.index(line) + 2]
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
        # TODO replace with function to get dipole from Orca analysis output
        print(f"get_diple not implemeneted yet in {self.mol.name}")
        pass
        self.mol.dipole_xyz = self.data_lines.split('RMSD=')[1].split('\\')[0]
        # convert to float RMSD=6.613e-05\\
        self.mol.dipole_xyz = float(self.mol.dipole_xyz.split('e')[0]) * 10**float(self.mol.dipole_xyz.split('e')[1])

        self.mol.dipole = self.data_lines.split('RMSF=')[1].split('\\')[0]
        self.mol.dipole = float(self.mol.dipole.split('e')[0]) * 10**float(self.mol.dipole.split('e')[1])



    # get whether or not there was an error, read only the bottom 100 lines of the file searching for 'Error termination'
    def get_status(self):
        # TODO replace with function to get status from Orca analysis output
        print(f"get_status not implemeneted yet in {self.mol.name}") # TODO
        pass
        for line in self.lines:
            if 'Error termination' in line:
                status = 'Error'
                break
            else:
                status = 'No Error'
        self.mol.status = status

    # line looks like  %NProcShared=16
    def get_NPROC(self):
        # TODO replace with function to get NPROC from Orca analysis output
        print(f"get_diple not implemeneted yet in {self.mol.name}")
        pass
        for line in self.lines:
            if '%NProcShared=' in line:
                self.mol.NPROC = float(line.split('=')[1])
                break

    def get_electronic_energy(self):
        # TODO replace with function to get electronic energy from Orca analysis output
        # or remove function if Analysis_Type does not yield electronic energy
        print(f"get_diple not implemeneted yet in {self.mol.name}")
        pass
        # HF=-2623.6082922\
        self.mol.electronic_energy = float(self.data_lines.split('HF=')[1].split('\\')[0]).__round__(5)

    # first value is basis set, second is functional
    def get_basis_set(self):
        # TODO replace with function to get basis set and functional from Orca analysis output
        # or remove function if Analysis_Type does not yield basis set and functional
        print(f"get_basis_set not implemeneted yet in {self.mol.name}")
        pass
        # no 'e' (exponent) should be in the basis set
        self.mol.basis_sets = float(self.data_lines.split('Dipole=')[1].split(',')[0])
        self.mol.functional = float(self.data_lines.split('Dipole=')[1].split(',')[1])
        self.mol.stoichiometry = float(self.data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0]) # cut off before //

    def get_method(self):
        # TODO replace with function to get method from Orca analysis output
        # or remove function if Analysis_Type does not yield method
        print(f"get_method not implemeneted yet in {self.mol.name}")
        pass

        # after FOpt\ but before the next \
        self.mol.functional = self.data_lines.split('FOpt\\')[1].split('\\')[0]
        self.mol.basis_sets = self.data_lines.split('FOpt\\')[1].split('\\')[1]

    def get_time(self):
        # TODO replace with function to get time from Orca analysis output
        # or remove function if Analysis_Type does not yield time
        print(f"get_time not implemeneted yet in {self.mol.name}")
        pass

        self.mol.time = ''
        # if line contains "elapsed time:"
        for line in self.lines:
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
        # TODO change to the format of the data lines in the output file to that of Orca Analysis output
        print('getting data lines not implemented yet for molecule:', self.mol.name)
        self.data_lines = self.lines
        pass
    
        # data lines start with '1\1\ and end with @, so read all lines between those two
        # and add it to one string
        # data lines are lines with the main data we are concerned with
        # this is used to reduce the number of times we have to loop over the file
        # it is optional, but recommended for large files
        self.data_lines = ''
        dataStart = False
        for line in self.lines:
            if '1\\1\\' in line or dataStart:
                dataStart = True
                self.data_lines += line
                if '@' in line:
                    # remove all the \n from the string
                    self.data_lines = self.data_lines.replace('\n', '')
                    self.data_lines = self.data_lines.replace(' ', '')
                    break   

    def get_upload_date_and_time(self):
        self.mol.upload_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.mol.upload_time = datetime.datetime.now().strftime("%H:%M:%S") 

    def get_opt_xyz(self):
        # TODO change to the format of the opt_xyz in the output file to that of Orca Analysis output
        # or remove function if Analysis_Type does not yield opt_xyz
        print('getting opt_xyz not implemented yet for molecule:', self.mol.name)
        pass

        xyz_data = self.data_lines.split('\\\\')[3]
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
        # TODO change to the format of the charges in the output file to that of Orca Analysis output
        # or remove function if Analysis_Type does not yield charges
        print('getting charges not implemented yet for molecule:', self.mol.name)
        pass
        found_mulliken, found_hirshfeld = False, False

        # reverse iterate over lines
        for line in reversed(self.lines):
            if (found_hirshfeld and found_mulliken):
                return
            
            # line just contains "Mulliken charges"
            if ('Mulliken charges' in line and not found_mulliken):
                found_mulliken = True      
                # go down (not reverse) and scan all lines in this format     
                # only intterested in the last value in the line (charge)

                atom_index = 0
                for chargeline in self.lines[self.lines.index(line) + 2:]:
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

                for chargeline in self.lines[self.lines.index(line) + 2:]:
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
        # TODO only if molecule analysis does not have basis_sets and functional
        # bring up to database administrator to create a standard for new identifier tag for the molecule

        self.mol.identifier = f'{self.mol.name}_{self.mol.basis_sets}_{self.mol.functional}'

        
    def get_total_energy(self):
        for line in reversed(self.lines):
            words = line.split()
            if len(words) > 2:
                # first two are Total Energy
                if words[0] == 'Total' and words[1] == 'Energy':
                    # get second to last word and store as self.mol.total_energy
                    self.mol.total_energy = float(words[-2])
                    break
        
    def get_charge(self):
        # requires a list of metals
        # list of all metals atomic symbols: H, Li, Be, Na, Mg, K, Ca, Rb, Sr, Cs, Ba, Fr, Ra, Sc, Y, La, Ac, Ti, Zr, Hf, V, Nb, Ta, Cr, Mo, W, Mn, Tc, Re, Fe, Ru, Os, Co, Rh, Ir, Ni, Pd, Pt, Cu, Ag, Au, Zn, Cd, Hg, B, Al, Ga, In, Tl, C, Si, Ge, Sn, Pb, N, P, As, Sb, Bi, O, S, Se, Te, Po, F, Cl, Br, I, At, He, Ne, Ar, Kr, Xe, Rn
        metals = ['H', 'Li', 'Be', 'Na', 'Mg', 'K', 'Ca', 'Rb', 'Sr', 'Cs', 'Ba', 'Fr', 'Ra', 'Sc', 'Y', 'La', 'Ac', 'Ti', 'Zr', 'Hf', 'V', 'Nb', 'Ta', 'Cr', 'Mo', 'W', 'Mn', 'Tc', 'Re', 'Fe', 'Ru', 'Os', 'Co', 'Rh', 'Ir', 'Ni', 'Pd', 'Pt', 'Cu', 'Ag', 'Au', 'Zn', 'Cd', 'Hg', 'B', 'Al', 'Ga', 'In', 'Tl', 'C', 'Si', 'Ge', 'Sn', 'Pb', 'N', 'P', 'As', 'Sb', 'Bi', 'O', 'S', 'Se', 'Te', 'Po', 'F', 'Cl', 'Br', 'I', 'At', 'He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']
        # find the last instance of 'MULLIKEN ATOMIC CHARGES'

        last_mulliken_atomic_charges_line = -1
        last_loewdin_atomic_charges_line = -1
        # reverse iterate through the lines
        for line in reversed(self.lines):
            # if the line contains 'MULLIKEN ATOMIC CHARGES'
            if 'MULLIKEN ATOMIC CHARGES' in line:
                # find the index of the line
                last_mulliken_atomic_charges_line = self.lines.index(line)
                break

            # skip to the line after the line with the four words
            last_mulliken_atomic_charges_line += 1

        # iterate through the lines starting at the line after the line with the four words
        for line in self.lines[last_mulliken_atomic_charges_line:]:
            if len(line.split()) == 4:
                # if the first word in the line is in the metals list
                if line.split()[0] in metals:
                    # add the charge to the self.mol object
                    self.mol.mulliken_atomic_charge = float(line.split()[3])
                    break

        # find the last instance of 'LOEWDIN ATOMIC CHARGES'
        for line in reversed(self.lines):
            if 'LOEWDIN ATOMIC CHARGES' in line:
                last_loewdin_atomic_charges_line = self.lines.index(line)
                break

        # skip to the line after the line with the four words
        last_loewdin_atomic_charges_line += 1

        # iterate through the self.lines starting at the line after the line with the four words
        for line in self.lines[last_loewdin_atomic_charges_line:]:
            if len(line.split()) == 4:
                if line.split()[0] in metals:
                    self.mol.loewdin_atomic_charge = float(line.split()[3])
                    break

    # write get band gap function, also gets homo and lumo
    def get_band_gap(self):
        # find line with only two words: ORBITAL ENERGIES
        last_orbital_energies_line = -1
        
        for line in reversed(self.lines):
            words_in_line = line.split()
            if len(words_in_line) == 2:
                if words_in_line[0] == 'ORBITAL' and words_in_line[1] == 'ENERGIES':
                    last_orbital_energies_line = self.lines.index(line)
                    break

        #skip to the line after the line with the four words
        for line in self.lines[last_orbital_energies_line:]:
            if len(line.split()) == 4:
                last_orbital_energies_line = self.lines.index(line) + 1
                break

        for line in self.lines[last_orbital_energies_line:]:
            words_in_line = line.split()
            previous_eev = -1
            if len(words_in_line) == 4:
                previous_eev = float(words_in_line[3])
                if float(words_in_line[3]) > 0:
                    self.mol.homo = float(words_in_line[3])
                    self.mol.lumo = previous_eev
                    self.mol.gap = self.mol.homo - self.mol.lumo
                    break

    def get_software_name_and_version(self):
        for line in self.lines:
            if 'Program Version' in line:
                self.mol.software_name_and_version = line.split('Program Version')[1].split('-')[0].strip()
                break

    # extract useful data from the file
    def get_data(self, molecule, file_path):

        with open(file_path, 'r') as mol_file:
            # Read all lines from the file
            self.lines = mol_file.readlines()
            self.mol = molecule
            self.get_data_lines() # optional, could just use whole file, to do that, remove this line and 

            # get the name of the file, could be in any directory so just get the last part of the path
            molecule.name = mol_file.name.split('/')[-1].split('.')[0]
            self.get_status()
            if molecule.status == 'Error':
                # if there was an error, skip the rest of the file
                return self.mol

            # run all the functions to get the data
            # self.get_homo_lumo()
            # self.get_NPROC()
            # self.get_electronic_energy()
            # self.get_dipole()
            # self.get_time()
            # self.get_method()
            # self.get_basis_set()
            # self.get_upload_date_and_time()
            # self.get_opt_xyz()
            # self.get_charges()
            self.get_band_gap()
            self.get_software_name_and_version
            self.get_total_energy()
            self.get_charge()
            self.make_identifier()

            return self.mol