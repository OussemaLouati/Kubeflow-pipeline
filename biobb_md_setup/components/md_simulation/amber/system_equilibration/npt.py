import os

def equilibrate_system_npt(
    output_pdb_path: str,
    output_nvt_path: str,
    output_npt_path: str,
    ): 
    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_npt_path)
    # Create prop dict and inputs/outputs
    
    
    
    
    output_npt_traj_path =  os.path.join(output_npt_path,  'sander.npt.netcdf')
    output_npt_rst_path =  os.path.join(output_npt_path,  'sander.npt.rst')
    output_npt_log_path =  os.path.join(output_npt_path,  'sander.npt.log')

    prop = {
        "simulation_type" : 'npt',
        "mdin" : { 
            'nstlim' : 500, # Reducing the number of steps for the sake of time (1ps)
            'ntr' : 1,     # Overwritting restrain parameter
            'restraintmask' : '\"!:WAT,Cl-,Na+ & !@H=\"',      # Restraining solute heavy atoms
            'restraint_wt' : 2.5                               # With a force constant of 2.5 Kcal/mol*A2
        }
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_nvt_rst_path =  os.path.join(output_nvt_path,  'sander.nvt.rst')

    # Create and launch bb
    sander_mdrun(input_top_path=output_ions_top_path,
            input_crd_path=output_nvt_rst_path,
            input_ref_path=output_nvt_rst_path,
            output_traj_path=output_npt_traj_path,
            output_rst_path=output_npt_rst_path,
            output_log_path=output_npt_log_path,
            properties=prop)



def check_npt_equilibration(
    output_npt_path: str,
    output_npt_dat_path: str,
    ): 

    # Import module
    from biobb_amber.process.process_mdout import process_mdout
    
    os.makedirs(output_npt_dat_path)
    # Create prop dict and inputs/outputs
    
    output_dat_npt_path =  os.path.join(output_npt_dat_path,  'sander.md.npt.dat')

    prop = {
        "terms" : ['PRES','DENSITY']
    }

    output_npt_log_path =  os.path.join(output_npt_path,  'sander.npt.log')
    # Create and launch bb
    process_mdout(input_log_path=output_npt_log_path,
            output_dat_path=output_dat_npt_path,
            properties=prop)