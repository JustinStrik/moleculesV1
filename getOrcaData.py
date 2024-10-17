from ORCAMolecule import ORCAMolecule

lines = [] # global lines
current_mol = []
molecules = []

def get_total_energy():
    for line in reversed(lines):
        words = line.split()
        if len(words) > 2:
            # first two are Total Energy
            if words[0] == 'Total' and words[1] == 'Energy':
                # get second to last word and store as current_mol.total_energy
                current_mol.total_energy = float(words[-2])
                break
    
def get_charge():
    # requires a list of metals
    # list of all metals atomic symbols: H, Li, Be, Na, Mg, K, Ca, Rb, Sr, Cs, Ba, Fr, Ra, Sc, Y, La, Ac, Ti, Zr, Hf, V, Nb, Ta, Cr, Mo, W, Mn, Tc, Re, Fe, Ru, Os, Co, Rh, Ir, Ni, Pd, Pt, Cu, Ag, Au, Zn, Cd, Hg, B, Al, Ga, In, Tl, C, Si, Ge, Sn, Pb, N, P, As, Sb, Bi, O, S, Se, Te, Po, F, Cl, Br, I, At, He, Ne, Ar, Kr, Xe, Rn
    metals = ['H', 'Li', 'Be', 'Na', 'Mg', 'K', 'Ca', 'Rb', 'Sr', 'Cs', 'Ba', 'Fr', 'Ra', 'Sc', 'Y', 'La', 'Ac', 'Ti', 'Zr', 'Hf', 'V', 'Nb', 'Ta', 'Cr', 'Mo', 'W', 'Mn', 'Tc', 'Re', 'Fe', 'Ru', 'Os', 'Co', 'Rh', 'Ir', 'Ni', 'Pd', 'Pt', 'Cu', 'Ag', 'Au', 'Zn', 'Cd', 'Hg', 'B', 'Al', 'Ga', 'In', 'Tl', 'C', 'Si', 'Ge', 'Sn', 'Pb', 'N', 'P', 'As', 'Sb', 'Bi', 'O', 'S', 'Se', 'Te', 'Po', 'F', 'Cl', 'Br', 'I', 'At', 'He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']
    # find the last instance of 'MULLIKEN ATOMIC CHARGES'

    last_mulliken_atomic_charges_line = -1
    last_loewdin_atomic_charges_line = -1
    # reverse iterate through the lines
    for line in reversed(lines):
        # if the line contains 'MULLIKEN ATOMIC CHARGES'
        if 'MULLIKEN ATOMIC CHARGES' in line:
            # find the index of the line
            last_mulliken_atomic_charges_line = lines.index(line)
            break

        # skip to the line after the line with the four words
        last_mulliken_atomic_charges_line += 1

    # iterate through the lines starting at the line after the line with the four words
    for line in lines[last_mulliken_atomic_charges_line:]:
        if len(line.split()) == 4:
            # if the first word in the line is in the metals list
            if line.split()[0] in metals:
                # add the charge to the current_mol object
                current_mol.mulliken_atomic_charge = float(line.split()[3])
                break

    # find the last instance of 'LOEWDIN ATOMIC CHARGES'
    for line in reversed(lines):
        if 'LOEWDIN ATOMIC CHARGES' in line:
            last_loewdin_atomic_charges_line = lines.index(line)
            break

    # skip to the line after the line with the four words
    last_loewdin_atomic_charges_line += 1

    # iterate through the lines starting at the line after the line with the four words
    for line in lines[last_loewdin_atomic_charges_line:]:
        if len(line.split()) == 4:
            if line.split()[0] in metals:
                current_mol.loewdin_atomic_charge = float(line.split()[3])
                break

    

# write get band gap function, also gets homo and lumo
def get_band_gap():
    # find line with only two words: ORBITAL ENERGIES
    last_orbital_energies_line = -1
    
    for line in reversed(lines):
        words_in_line = line.split()
        if len(words_in_line) == 2:
            if words_in_line[0] == 'ORBITAL' and words_in_line[1] == 'ENERGIES':
                last_orbital_energies_line = lines.index(line)
                break

    #skip to the line after the line with the four words
    for line in lines[last_orbital_energies_line:]:
        if len(line.split()) == 4:
            last_orbital_energies_line = lines.index(line) + 1
            break

    for line in lines[last_orbital_energies_line:]:
        words_in_line = line.split()
        previous_eev = -1
        if len(words_in_line) == 4:
            previous_eev = float(words_in_line[3])
            if float(words_in_line[3]) > 0:
                current_mol.homo = float(words_in_line[3])
                current_mol.lumo = previous_eev
                current_mol.gap = current_mol.homo - current_mol.lumo
                break

def get_software_name_and_version():
    for line in lines:
        if 'Program Version' in line:
            current_mol.software_name_and_version = line.split('Program Version')[1].split('-')[0].strip()
            break



# create get functions for all attributes

def get_orca_data(outfiles):

    # loop over all out files
    for outfile in outfiles:

        global current_mol
        current_mol = {}

        with open(outfile, 'r') as outfile:
            # Read all lines from the file
            global lines
            lines = outfile.readlines()
            current_mol = ORCAMolecule()
            current_mol.file_name = outfile.name.split('/')[-1].split('.')[0]
            get_software_name_and_version()
            get_band_gap()
            get_charge()

            molecules.append(current_mol)

    return molecules

    
            
        
