
import os
import shutil
    
def add_hydrogen_atoms(
    ligand_code: str ,
    ligand_file_path: str, 
    output_reduce_h_path: str, 
    ):
   
    # Create Ligand system topology, STEP 2
    # Reduce_add_hydrogens: add Hydrogen atoms to a small molecule (using Reduce tool from Ambertools package)
    # Import module
    from biobb_chemistry.ambertools.reduce_add_hydrogens import reduce_add_hydrogens

    os.makedirs(output_reduce_h_path)
    # Create prop dict and inputs/outputs
     
    output_reduce_h =  os.path.join(output_reduce_h_path,  ligand_code + '.reduce.H.pdb')

    prop = {
        'nuclear' : 'true'
    }
  
    ligandFile =  os.path.join(ligand_file_path,  ligand_code + '.pdb')
    # Create and launch bb
    reduce_add_hydrogens(input_path=ligandFile,
                   output_path=output_reduce_h,
                   properties=prop)


def babel_minimization(
    ligand_code: str , 
    output_reduce_h_path: str,
    output_babel_min_path: str,   
    ):

    # Create Ligand system topology, STEP 3
    # Babel_minimize: Structure energy minimization of a small molecule after being modified adding hydrogen atoms
    # Import module
    from biobb_chemistry.babelm.babel_minimize import babel_minimize

    os.makedirs(output_babel_min_path)
    # Create prop dict and inputs/outputs
    output_babel_min =  os.path.join(output_babel_min_path,  ligand_code + '.H.min.mol2')
    output_reduce_h =  os.path.join(output_reduce_h_path,  ligand_code + '.reduce.H.pdb') 

    prop = {
        'method' : 'sd',
        'criteria' : '1e-10',
        'force_field' : 'GAFF'
    }


    # Create and launch bb
    babel_minimize(input_path=output_reduce_h,
              output_path=output_babel_min,
              properties=prop)


def ligand_topology_generation(
    output_acpype_path: str,
    output_babel_min_path: str,
    ligand_code: str ,  
    mol_charge: int
    ):

    # Create Ligand system topology, STEP 4
    # Acpype_params_gmx: Generation of topologies for AMBER with ACPype
    # Import module
    from biobb_chemistry.acpype.acpype_params_ac import acpype_params_ac
    
    os.makedirs(output_acpype_path)
    # Create prop dict and inputs/outputs
    
    output_acpype_inpcrd =   ligand_code+'params.inpcrd'
    output_acpype_frcmod =   ligand_code + 'params.frcmod'
    output_acpype_lib =  ligand_code + 'params.lib'
    output_acpype_prmtop = ligand_code+'params.prmtop'
    output_acpype =   ligand_code+'params'

    
    
    output_babel_min =  os.path.join(output_babel_min_path,  ligand_code + '.H.min.mol2') 

    prop = {
        'basename' : output_acpype,
        'charge' : mol_charge
    }

    # Create and launch bb
    acpype_params_ac(input_path=output_babel_min, 
                output_path_inpcrd=output_acpype_inpcrd,
                output_path_frcmod=output_acpype_frcmod,
                output_path_lib=output_acpype_lib,
                output_path_prmtop=output_acpype_prmtop,
                properties=prop)
  
    for fname in [output_acpype_inpcrd,
                output_acpype_frcmod ,
                output_acpype_lib ,
                output_acpype_prmtop, 
                 ]:
     
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(os.getcwd(),fname), output_acpype_path)

