# print the names of all the files in the current directory
import os
from molecule import molecule
import datetime

# global logfile
logfile = ''
molecules = []
# there is a data_lines string
# this contains the lines with the main data we are concerned with
# reduces the number of times we have to loop over the file

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
    # no 'e' (exponent) should be in the basis set
    current_mol.dipole = [] # type: ignore
    current_mol.dipole.append(float(data_lines.split('Dipole=')[1].split(',')[0]))
    current_mol.dipole.append(float(data_lines.split('Dipole=')[1].split(',')[1]))
    current_mol.dipole.append(float(data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0]))

    #     # no 'e' (exponent) should be in the basis set
    # current_mol.basis_sets = float(data_lines.split('Dipole=')[1].split(',')[0])
    # current_mol.functional = float(data_lines.split('Dipole=')[1].split(',')[1])
    # print(data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0])
    # current_mol.stoichiometry = float(data_lines.split('Dipole=')[1].split(',')[2].split('\\')[0])

def get_charges():
    found_mulliken, found_hirshfeld = False, False

    # reverse iterate over lines
    for line in reversed(lines):
        if (found_hirshfeld and found_mulliken):
            return
        
        if (line == '  Mulliken charges:\n' and not found_mulliken):
            found_mulliken = True      
            # go down (not reverse) and scan all lines in this format     
            # only intterested in the last value in the line (charge)

            iter = 0
            for chargeline in lines[lines.index(line) + 1:]:
                if chargeline == '\n':
                    break
                values = chargeline.split()
                current_mol.opt_xyz[iter]['mulliken'](float(values[len(values) - 1]))
                iter += 1

        # if line contains "Hirshfeld charges"
        if (line == '  Hirshfeld charges:\n' and not found_hirshfeld):
            found_hirshfeld = True
            iter = 0

            for chargeline in lines[lines.index(line) + 1:]:
                if chargeline == '\n':
                    break
                values = chargeline.split()
                current_mol.opt_xyz[iter]['hirshfeld'](float(values[len(values) - 1]))
                iter += 1

# elapsed time
def get_time():
    current_mol.time = ''
    # if line contains "elapsed time:"
    for line in lines:
        if 'Job cpu time:' in line:
            # get the time
            time_data = line.split('Job cpu time:       ')[1].split(' ')
            for data in time_data:
                if data == '':
                    time_data.remove(data)

            # split '0 days  0 hours 21 minutes  6.9 seconds.\n' into just 0:0:21:6.9
            current_mol.cpu_time = time_data[0] + ':' + time_data[2] + ':' + time_data[4] + ':' + time_data[6]
            continue

        if 'Elapsed time:' in line:
            # get the time
            time_data = line.split('Elapsed time:       ')[1].split(' ')
            for data in time_data:
                if data == '':
                    time_data.remove(data)
            # split '0 days  0 hours 21 minutes  6.9 seconds.\n' into just 0:0:21:6.9
            current_mol.elapsed_time = time_data[0] + ':' + time_data[2] + ':' + time_data[4] + ':' + time_data[6]
            break

def get_upload_date_and_time():
    current_mol.upload_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_mol.upload_time = datetime.datetime.now().strftime("%H:%M:%S")

def get_opt_xyz():
    xyz_data = data_lines.split('\\\\')[3]
    # read and ignore (pop) first 4 characters
    xyz_data = xyz_data.split('\\')
    current_mol.total_charge = int(xyz_data[0].split(',')[0])
    current_mol.spin_multiplicity = int(xyz_data[0].split(',')[1])
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

    current_mol.opt_xyz = xyz_atoms
    



# get whether or not there was an error, read only the bottom 100 lines of the file searching for 'Error termination'
def get_status():
    status = 'No Error'
    for line in lines:
        if 'Error termination' in line:
            status = 'Error'
            break
    current_mol.status = status

# line looks like  %NProcShared=16
def get_NPROC():
    for line in lines:
        if '%NProcShared=' in line:
            current_mol.NPROC = float(line.split('=')[1])
            break

# gets functional and basis set
def get_method():
    # after FOpt\ but before the next \
    current_mol.functional = data_lines.split('FOpt\\')[1].split('\\')[0]
    current_mol.basis_sets = data_lines.split('FOpt\\')[1].split('\\')[1]

def get_electronic_energy():
    # HF=-2623.6082922\
    current_mol.electronic_energy = float(data_lines.split('HF=')[1].split('\\')[0]).__round__(5)

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
            
def get_name():
    # get the name of the molecule
    # in data lines, between two \\
    # test = data_lines.split('\\\\')
    # current_mol.name = data_lines.split('\\\\')[2]

    # name is name of file without .log
    current_mol.name = current_mol.name.split('.log')[0]


def get_data(logfiles):
    # get all files that end with .log in the database directory
    # make sure the logfile name is the same as the path to the file
    # logfiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.log')]

    # loop over all log files
    for logfile in logfiles: 
        global current_mol
        current_mol = molecule()
        global lines
        lines = ''
        global data_lines
        data_lines = ''
        with open(logfile, 'r') as logfile:
            # Read all lines from the file
            lines = logfile.readlines()
            dataLines = ''
            get_status()
            get_name()
            if current_mol.status == 'Error':
                # if there was an error, skip the rest of the file
                molecules.append(current_mol)
                continue
            get_data_lines()
            get_upload_date_and_time()

            get_homo_lumo()
            get_NPROC()
            get_electronic_energy()
            get_dipole()
            get_time()
            get_method()
            get_opt_xyz()
            get_charges()

            # add the molecule to the list of molecules
            molecules.append(current_mol)

    return molecules

    
