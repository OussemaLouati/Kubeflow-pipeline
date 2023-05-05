import os 

def equilibrate_system_nvt(
    output_pdb_path: str,
    output_heat_path: str,
    output_nvt_path: str,
    ): 

    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_nvt_path)
    # Create prop dict and inputs/outputs
    
    output_nvt_traj_path =  os.path.join(output_nvt_path,  'sander.nvt.netcdf')
    output_nvt_rst_path =  os.path.join(output_nvt_path,  'sander.nvt.rst')
    output_nvt_log_path =  os.path.join(output_nvt_path,  'sander.nvt.log')

    prop = {
        "simulation_type" : 'nvt',
        "mdin" : { 
            'nstlim' : 500, # Reducing the number of steps for the sake of time (1ps)
            'ntr' : 1,     # Overwritting restrain parameter
            'restraintmask' : '\"!:WAT,Cl-,Na+ & !@H=\"',      # Restraining solute heavy atoms
            'restraint_wt' : 5.0                              # With a force constant of 5 Kcal/mol*A2
        }
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_heat_rst_path =  os.path.join(output_heat_path,  'sander.heat.rst')

    # Create and launch bb
    sander_mdrun(input_top_path=output_ions_top_path,
                input_crd_path=output_heat_rst_path,
                input_ref_path=output_heat_rst_path,
                output_traj_path=output_nvt_traj_path,
                output_rst_path=output_nvt_rst_path,
                output_log_path=output_nvt_log_path,
                properties=prop)


def check_nvt_equilibration(
    output_nvt_path: str,
    output_nvt_dat_path: str,
    ): 
    # Import module
    from biobb_amber.process.process_mdout import process_mdout
    
    os.makedirs(output_nvt_dat_path)
    # Create prop dict and inputs/outputs
    output_dat_nvt_path =  os.path.join(output_nvt_dat_path,  'sander.md.nvt.temp.dat')

    prop = {
    "terms" : ['TEMP']
    }
    
    output_nvt_log_path =  os.path.join(output_nvt_path,  'sander.nvt.log')

    # Create and launch bb
    process_mdout(input_log_path=output_nvt_log_path,
            output_dat_path=output_dat_nvt_path,
            properties=prop)
