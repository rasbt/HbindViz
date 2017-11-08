# Sebastian Raschka, 12/22/2016
#
# Create PyMOL commands for visualizing interactions between proteins
# and ligands from custom HBind interaction tables


import os
import sys


def write_table(inpath, outpath, tag):
    with open(inpath, 'r') as f:
        txt = f.read()
    with open(outpath, 'w') as f:

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

        f.write('hide lines\n')
        f.write('show cartoon\n')
        f.write('show sticks, %s_ligand\n' % tag)
        f.write('set sphere_scale=0.32\n')
        for i in set(prot_resid):
            f.write('show sticks, (%s_protein and chain A and resi %s)\n' %
                    (tag, i))

        for i in set(lig_atomid):
            f.write('show sphere, (%s_ligand and id %s)\n' % (tag, i))

        ld_metal = False
        metal = False
        saltb = False
        hbond = False

        for a, b, c, d, e in zip(prot_restype, prot_resid,
                                 prot_atom, lig_atomid, interact_type):
            f.write('show sphere, /%s_protein///%s`%s/%s\n' % (tag, a, b, c))


            if e == 'hbond':
                f.write('distance hbond, /%s_protein///%s`%s/%s,'
                        '(%s_ligand and id %s)\n' % (tag, a, b, c, tag, d))
                hbond = True
            elif e == 'saltb':
                f.write('distance saltb, /%s_protein///%s`%s/%s,'
                        '(%s_ligand and id %s)\n' % (tag, a, b, c, tag, d))
                saltb = True
            elif e == 'metal':
                f.write('distance metal, /%s_protein///%s`%s/%s,'
                        '(%s_ligand and id %s)\n' % (tag, a, b, c, tag, d))
                metal = True
            elif e == 'ld_metal':
                f.write('distance ld_metal, /1%s_protein///%s`%s/%s,'
                        '(%s_ligand and id %s)\n' % (tag, a, b, c, tag, d))
                ld_metal = True

        if hbond:
            f.write('set dash_color, yellow, hbond\n')
        if metal:
            f.write('set dash_color, green, saltb\n')
        if saltb:
            f.write('set dash_color, grey, ld_metal\n')
        if ld_metal:
            f.write('set dash_color, white, metal\n')

        f.write('hide labels')


if __name__ == '__main__':

    slide_tabledir = sys.argv[1]
    out_dir = sys.argv[2]

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    tables = [i for i in os.listdir(slide_tabledir)
              if i.endswith('.txt') and not i.startswith('.')]
    in_paths = [os.path.join(slide_tabledir, i) for i in tables]
    out_paths = [os.path.join(out_dir, i) for i in tables]

    for i, o in zip(in_paths, out_paths):
        tag = os.path.basename(i).split('.txt')[0]
        write_table(i, o, tag)
