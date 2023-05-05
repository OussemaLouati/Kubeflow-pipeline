
import os

def postprocess_structure(
    output_pdb_path: str,
    output_free_path: str,
    output_imaged_traj_path: str,
    ligand_code: str 
    ): 

    """
    Post processing on the resulting 3D trajectory.

    Args:
        output_pdb_path: pdb code 
        output_free_path: 
        ligand_code: Ligand code

    Returns:

        output_imaged_traj_path: path to save the output of the step

    """
    # cpptraj_image: "Imaging" the resulting trajectory
    #                Removing water molecules and ions from the resulting structure

    # Import module
    from biobb_analysis.ambertools.cpptraj_image import cpptraj_image
    

    os.makedirs(output_imaged_traj_path)
    # Create prop dict and inputs/outputs
    output_imaged_traj =  os.path.join(output_imaged_traj_path, ligand_code + '_imaged_traj.trr')  

    prop = {
        'mask': 'solute',
        'format': 'trr'
    }

    output_ions_top_path =  os.path.join(output_pdb_path, 'structure.ions.parmtop') 
    output_free_traj_path =  os.path.join(output_free_path, 'sander.free.netcdf') 
    
    # Create and launch bb
    cpptraj_image(input_top_path=output_ions_top_path,
            input_traj_path=output_free_traj_path,
            output_cpptraj_path=output_imaged_traj,
            properties=prop)