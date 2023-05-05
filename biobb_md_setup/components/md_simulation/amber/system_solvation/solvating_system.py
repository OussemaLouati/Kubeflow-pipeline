import os
import shutil


def convert_amber_to_pdb(
    leap_gen_top_output_path: str,
    output_h_min_path: str,
    output_ambpdb_path: str,
    ):

    # Import module
    from biobb_amber.ambpdb.amber_to_pdb import amber_to_pdb
    
    os.makedirs(output_ambpdb_path)

    
    output_ambpdb_path =  os.path.join(output_ambpdb_path, 'structure.ambpdb.pdb')
    output_h_min_rst_path =  os.path.join(output_h_min_path, 'sander.h_min.rst')
    output_top_path =  os.path.join(leap_gen_top_output_path, 'structure.leap.top')

    # Create and launch bb
    amber_to_pdb(input_top_path=output_top_path,
            input_crd_path=output_h_min_rst_path,
            output_pdb_path=output_ambpdb_path)



def create_water_box(
    ligand_code: str,
    output_acpype_path: str,
    output_ambpdb_path: str,
    output_solv_path: str,
    ):
    # Import module
    from biobb_amber.leap.leap_solvate import leap_solvate
    

    os.makedirs(output_solv_path)
    # Create prop dict and inputs/outputs
    
    
    output_solv_pdb_path = 'structure.solv.pdb'
    output_solv_top_path = 'structure.solv.parmtop'
    output_solv_crd_path = 'structure.solv.crd'

    prop = {
    "forcefield" : ["protein.ff14SB","gaff"],
    "water_type": "TIP3PBOX",
    "distance_to_molecule": "9.0",   
    "box_type": "truncated_octahedron"
    }

    
    output_acpype_frcmod =  os.path.join(output_acpype_path, ligand_code + 'params.frcmod')
    output_acpype_lib =  os.path.join(output_acpype_path, ligand_code + 'params.lib')
    output_ambpdb_path =  os.path.join(output_ambpdb_path, 'structure.ambpdb.pdb')

    # Create and launch bb
    leap_solvate(input_pdb_path=output_ambpdb_path,
             input_lib_path=output_acpype_lib,
             input_frcmod_path=output_acpype_frcmod,
             output_pdb_path=output_solv_pdb_path,
             output_top_path=output_solv_top_path,
             output_crd_path=output_solv_crd_path,
             properties=prop)

    for fname in [output_solv_pdb_path,
                output_solv_top_path ,
                output_solv_crd_path ,
                 ]:
     
        shutil.copy2(os.path.join(os.getcwd(),fname), output_solv_path)

def add_ions(
    output_acpype_path: str,
    output_solv_path: str,
    output_pdb_path: str,
    ligand_code: str
    ):
    # Import module
    from biobb_amber.leap.leap_add_ions import leap_add_ions
    import os
    os.makedirs(output_pdb_path)

    # Create prop dict and inputs/outputs
    
    
    
    
    output_ions_pdb_path =  os.path.join(output_pdb_path,  'structure.ions.pdb')
    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_ions_crd_path =  os.path.join(output_pdb_path,  'structure.ions.crd')


    prop = {
        "forcefield" : ["protein.ff14SB","gaff"],
        "neutralise" : True,
        "positive_ions_type": "Na+",
        "negative_ions_type": "Cl-",
        "ionic_concentration" : 150, # 150mM
        "box_type": "truncated_octahedron"
    }
    
    output_acpype_frcmod =  os.path.join(output_acpype_path, ligand_code + 'params.frcmod')
    output_acpype_lib =  os.path.join(output_acpype_path, ligand_code + 'params.lib')
    output_solv_pdb_path =  os.path.join(output_solv_path, 'structure.solv.pdb')

    # Create and launch bb
    leap_add_ions(input_pdb_path=output_solv_pdb_path,
                input_lib_path=output_acpype_lib,
                input_frcmod_path=output_acpype_frcmod,
                output_pdb_path=output_ions_pdb_path,
                output_top_path=output_ions_top_path,
                output_crd_path=output_ions_crd_path,
                properties=prop)