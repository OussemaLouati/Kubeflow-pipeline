

def ligand_sys_topology_creation(
        ligand_code: str ,
        ligand_file_path: str, 
        output_reduce_h_path: str, 
        output_babel_min_path: str,
        output_acpype_path: str,
        mol_charge: int
    ):

    from bio_chemistry.system_topology import add_hydrogen_atoms, babel_minimization, ligand_topology_generation

    add_hydrogen_atoms(
        ligand_code ,
        ligand_file_path, 
        output_reduce_h_path, 
    )

    babel_minimization(
        ligand_code , 
        output_reduce_h_path,
        output_babel_min_path,   
    )

    ligand_topology_generation(
        output_acpype_path,
        output_babel_min_path,
        ligand_code ,  
        mol_charge
    )