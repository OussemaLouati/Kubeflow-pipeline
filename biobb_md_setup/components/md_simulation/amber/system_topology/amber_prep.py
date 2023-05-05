"""Amber Preparation for system topology."""
import os

def amber_prep(
    removed_ligands_pdb_path: str,
    output_pdb4amber_path: str,
    pdb_code: str ,  
    ):
    """
    Amber preparation.

    Args:
        pdb_code: pdb code 
        removed_ligands_pdb_path: path to the saved "removed BME ligand pdb" to

    Returns:

        output_pdb4amber_path: path to save the output of the step
    """

    # Import module
    from biobb_amber.pdb4amber.pdb4amber_run import pdb4amber_run

    os.makedirs(output_pdb4amber_path)

    # Create properties dict and inputs/outputs  
    prop = {
        'ligand' : 'BME'
    }

    # Create properties dict and inputs/outputs
    nobme_pdb =  os.path.join(removed_ligands_pdb_path, pdb_code + '.noBME.pdb')  

    # Create prop dict and inputs/outputs
    output_pdb4amber =  os.path.join(output_pdb4amber_path,  'structure.pdb4amber.pdb')

    # Create and launch bb
    pdb4amber_run(input_pdb_path=nobme_pdb,
            output_pdb_path=output_pdb4amber,
            properties=prop)


def build_amber_topology(
    output_acpype_path: str,
    output_pdb4amber_path: str,
    leap_gen_top_output_path: str,
    ligand_code: str ,  
    ):

    # Import module
    from biobb_amber.leap.leap_gen_top import leap_gen_top

    os.makedirs(leap_gen_top_output_path)
    # Create prop dict and inputs/outputs
    output_pdb_path =  os.path.join(leap_gen_top_output_path,  'structure.leap.pdb') 

    output_top_path =  os.path.join(leap_gen_top_output_path, 'structure.leap.top')
    
    
    output_crd_path =  os.path.join(leap_gen_top_output_path,  'structure.leap.crd') 

    prop = {
        "forcefield" : ["protein.ff14SB","gaff"]
    }
    
    output_acpype_frcmod =  os.path.join(output_acpype_path, ligand_code + 'params.frcmod')
    output_acpype_lib =  os.path.join(output_acpype_path, ligand_code + 'params.lib')

    output_pdb4amber =  os.path.join(output_pdb4amber_path,  'structure.pdb4amber.pdb')
    
    # Create and launch bb
    leap_gen_top(input_pdb_path=output_pdb4amber,
           input_lib_path=output_acpype_lib,
           input_frcmod_path=output_acpype_frcmod,
           output_pdb_path=output_pdb_path,
           output_top_path=output_top_path,
           output_crd_path=output_crd_path,
           properties=prop)