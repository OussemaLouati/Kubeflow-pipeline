def solv_system(
    leap_gen_top_output_path: str,
    output_h_min_path: str,
    output_ambpdb_path: str,
    ligand_code: str,
    output_acpype_path: str,
    output_solv_path: str,
    output_pdb_path: str,
    ):

    from amber.system_solvation.solvating_system import convert_amber_to_pdb,create_water_box, add_ions
    
    convert_amber_to_pdb(
        leap_gen_top_output_path,
        output_h_min_path,
        output_ambpdb_path,
    )
    
    create_water_box(
        ligand_code,
        output_acpype_path,
        output_ambpdb_path,
        output_solv_path,
    )

    add_ions(
        output_acpype_path,
        output_solv_path,
        output_pdb_path,
        ligand_code
    )
    

    ## TODO : NGLVIEW VISUALISATION