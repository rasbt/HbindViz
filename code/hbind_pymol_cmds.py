# Sebastian Raschka, 12/22/2016
#
# Tool to create PyMOL commands for visualizing
# hydrogen-bond interactions between a protein
# its ligands from HBind interaction tables

import sys


def generate_pymol_commands(inpath):
    with open(inpath, 'r') as f:
        txt = f.read()

    prot_resid = []
    prot_restype = []
    prot_atom = []
    lig_atomid = []
    interact_type = []

    for line in txt.split('\n'):
        if line.startswith(('| hbond', '| saltb ',
                            '| metal', '| metal_ld')):
            line = line.split()
            interact_type.append(line[1].strip())
            lig_atomid.append(line[3].strip())
            prot_restype.append(line[6].strip())
            prot_resid.append(line[7].strip())
            prot_atom.append(line[8].strip())

    print('hide lines')
    print('show cartoon')
    print('show sticks, ligand')
    print('set sphere_scale=0.32')
    for i in set(prot_resid):
        print('show sticks, (protein and chain A and resi %s)' %
              (i))

    for i in set(lig_atomid):
        print('show sphere, (ligand and id %s)' % (i))

    ld_metal = False
    metal = False
    saltb = False
    hbond = False

    for a, b, c, d, e in zip(prot_restype, prot_resid,
                             prot_atom, lig_atomid, interact_type):
        print('show sphere, /protein///%s`%s/%s' % (a, b, c))

        if e == 'hbond':
            print('distance hbond, /protein///%s`%s/%s,'
                  '(ligand and id %s)' % (a, b, c, d))
            hbond = True
        elif e == 'saltb':
            print('distance saltb, /protein///%s`%s/%s,'
                  '(ligand and id %s)' % (a, b, c, d))
            saltb = True
        elif e == 'metal':
            print('distance metal, /protein///%s`%s/%s,'
                  '(ligand and id %s)' % (a, b, c, d))
            metal = True
        elif e == 'ld_metal':
            print('distance ld_metal, /protein///%s`%s/%s,'
                  '(ligand and id %s)' % (a, b, c, d))
            ld_metal = True

    if hbond:
        print('set dash_color, yellow, hbond')
    if metal:
        print('set dash_color, green, saltb')
    if saltb:
        print('set dash_color, grey, ld_metal')
    if ld_metal:
        print('set dash_color, white, metal')

    print('hide labels')


if __name__ == '__main__':

    hbind_tabledir = sys.argv[1]
    generate_pymol_commands(hbind_tabledir)
