# print the names of all the files in the current directory
import os
from molecule.py import molecule
# global logfile
logfile = ''
lines = ''
molecules = []
current_mol = ''

def get_homo_lumo(): 
    linefound = False

    # Search for the last line containing "Alpha occ. eigenvalues"
    for line in reversed(lines):
        if linefound:
            # return to two lines before the line containing "Alpha occ. eigenvalues"
            line = lines[lines.index(line) + 2]
            values = line.split()[4:]
            lumo = values[0]
            break

        if 'Alpha  occ. eigenvalues --' in line:
            # Split the line into a list of values
            values = line.split()[4:]

            # Check if the list has 4 or 5 values
            if len(values) == 4:
                # Return the fourth value
                linefound = True
                homo = values[3]
                continue

    # Print the result
    print(homo, lumo)

# get whether or not there was an error, read only the bottom 100 lines of the file searching for 'Error termination'
def get_status():
    # Read the last 100 lines from the file
    reveresed_lines = logfile.readlines()[-100:]
    for line in reveresed_lines:
        if 'Error termination' in line:
            status = 'Error'
            break
        else:
            status = 'No Error'
    print(status)

# line looks like  %NProcShared=16
def get_NPROC():
    for line in lines:
        if '%NProcShared=' in line:
            NPROC = line.split('=')[1]
            break
    print(NPROC)


if __name__ == '__main__':
    # get all files that end with .log in the current directory
    logfiles = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.log')]

    # loop over all log files
    for logfile in logfiles:
        with open(logfile, 'r') as logfile:
            # Read all lines from the file
            lines = logfile.readlines()
            current_mol = molecule()

            get_homo_lumo()
            get_status()
            get_NPROC()

    
