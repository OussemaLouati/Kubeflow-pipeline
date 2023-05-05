




def preprocess_structure(
    downloaded_pdb_path: str,
    nowat_pdb_path: str,
    removed_ligands_pdb_path: str,
    pdb_code: str ,  
    ):

    # Import module
    from structure_utils.preprocessing import remove_pdb_water_ligands

    
    remove_pdb_water_ligands(
        downloaded_pdb_path,
        nowat_pdb_path,
        removed_ligands_pdb_path,
        pdb_code,  
    )
 




 
    