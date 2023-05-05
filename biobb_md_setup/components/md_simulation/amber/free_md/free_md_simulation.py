import os

def create_binary_file(
    output_pdb_path: str,
    output_npt_path: str,
    output_free_path: str,
    ): 

    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_free_path)
    # Create prop dict and inputs/outputs
    
    output_free_traj_path =  os.path.join(output_free_path,  'sander.free.netcdf')
    output_free_rst_path =  os.path.join(output_free_path,  'sander.free.rst')
    output_free_log_path =  os.path.join(output_free_path,  'sander.free.log')

    prop = {
        "simulation_type" : 'free',
        "mdin" : { 
            'nstlim' : 2500, # Reducing the number of steps for the sake of time (5ps)
            'ntwx' : 500  # Print coords to trajectory every 500 steps (1 ps)
        }
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_npt_rst_path =  os.path.join(output_npt_path,  'sander.npt.rst')

    # Create and launch bb
    sander_mdrun(input_top_path=output_ions_top_path,
                input_crd_path=output_npt_rst_path,
                output_traj_path=output_free_traj_path,
                output_rst_path=output_free_rst_path,
                output_log_path=output_free_log_path,
                properties=prop)