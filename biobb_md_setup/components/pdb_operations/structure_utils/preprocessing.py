
"""Preliminary Preprocessing steps on the downloaded PDB."""


def remove_pdb_water_ligands(
    downloaded_pdb_path: str,
    nowat_pdb_path: str,
    removed_ligands_pdb_path: str,
    pdb_code: str ,  
    ):
    """
    Remove water molecules from the downloaded object.

    Args:
        pdb_code: pdb code 
        downloaded_pdb_path: Path to the downladed PDB file

    Returns:
        nowat_pdb_path: path to save the removed PO4 ligands pdb to
        removed_ligands_pdb_path: path to save the removed BME ligand pdb to
    """

    # Import module
    from biobb_structure_utils.utils.remove_pdb_water import remove_pdb_water
    from biobb_structure_utils.utils.remove_ligand import remove_ligand
    import os

    os.makedirs(nowat_pdb_path)

    # Create properties dict and inputs/outputs
    nowat_pdb =  os.path.join(nowat_pdb_path, pdb_code + '.nowat.pdb') 
    downloaded_pdb =  os.path.join(downloaded_pdb_path, pdb_code + '.pdb')  

    

    #Create and launch bb
    remove_pdb_water(input_pdb_path=downloaded_pdb,
        output_pdb_path=nowat_pdb)



    os.makedirs(removed_ligands_pdb_path)
    # Removing PO4 ligands:

    # Create properties dict and inputs/outputs  
    nopo4_pdb =  os.path.join(removed_ligands_pdb_path, pdb_code + '.noPO4.pdb')  

    prop = {
        'ligand' : 'PO4'
    }

    #Create and launch bb
    remove_ligand(input_structure_path=nowat_pdb,
        output_structure_path=nopo4_pdb,
        properties=prop)

    # Removing BME ligand:

    # Create properties dict and inputs/outputs
    nobme_pdb =  os.path.join(removed_ligands_pdb_path, pdb_code + '.noBME.pdb')  

    prop = {
        'ligand' : 'BME'
    }

    #Create and launch bb
    remove_ligand(input_structure_path=nopo4_pdb,
        output_structure_path=nobme_pdb,
        properties=prop)  


def extract_ligand_structure(
    ligand_code: str ,
    output_pdb4amber_path: str,
    ligand_file_path: str, 
    ):
    
    # Create Ligand system topology, STEP 1
    # Extracting Ligand JZ4
    # Import module
    from biobb_structure_utils.utils.extract_heteroatoms import extract_heteroatoms
    import os


    os.makedirs(ligand_file_path)
    
    # Create properties dict and inputs/outputs
    ligandFile =  os.path.join(ligand_file_path,  ligand_code + '.pdb')
    output_pdb4amber =  os.path.join(output_pdb4amber_path,  'structure.pdb4amber.pdb')

    print(os.listdir(output_pdb4amber_path))
    print(output_pdb4amber)

    prop = {
         'heteroatoms' : [{"name": "JZ4"}]
    }

    extract_heteroatoms(input_structure_path=output_pdb4amber,
        output_heteroatom_path=ligandFile,
        properties=prop)