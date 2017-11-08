

Usage:

python generate-pymol-commands.py example/hbind_tables/ example/outputs/

Open files in pymol:

- 1cip_ligand.mol2
- 1cip_protein.pdb

use _ligand and _protein, and make sure those names match with the output commands, e.g., 

    ...
    show sticks, 1cip_ligand
    set sphere_scale=0.32
    show sticks, (1cip_protein and chain A and resi 15)
    show sticks, (1cip_protein and chain A and resi 239)
    ...

Copy and paste those into the pymol prompt and hit enter.

that's it