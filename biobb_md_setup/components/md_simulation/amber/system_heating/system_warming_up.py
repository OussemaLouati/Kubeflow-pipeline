import os

def warm_system_up(
    output_pdb_path: str,
    output_min_path: str,
    output_heat_path: str,
    ):
    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_heat_path)
    # Create prop dict and inputs/outputs
    
    
    output_heat_traj_path =  os.path.join(output_heat_path,  'sander.heat.netcdf')
    output_heat_rst_path =  os.path.join(output_heat_path,  'sander.heat.rst')
    output_heat_log_path =  os.path.join(output_heat_path,  'sander.heat.log')

    prop = {
        "simulation_type" : "heat",
        "mdin" : { 
            'nstlim' : 2500, # Reducing the number of steps for the sake of time (5ps)
            'ntr' : 1,     # Overwritting restrain parameter
            'restraintmask' : '\"!:WAT,Cl-,Na+\"',      # Restraining solute
            'restraint_wt' : 10.0                       # With a force constant of 10 Kcal/mol*A2
        }
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_min_rst_path =  os.path.join(output_min_path,  'sander.min.rst')

    # Create and launch bb
    sander_mdrun(input_top_path=output_ions_top_path,
                input_crd_path=output_min_rst_path,
                input_ref_path=output_min_rst_path,
                output_traj_path=output_heat_traj_path,
                output_rst_path=output_heat_rst_path,
                output_log_path=output_heat_log_path,
                properties=prop)



def check_system_warm_up_result(
    output_heat_path: str,
    output_dat_heat_path: str,
    ):
    # Import module
    from biobb_amber.process.process_mdout import process_mdout
    
    os.makedirs(output_dat_heat_path)
    # Create prop dict and inputs/outputs
    
    output_dat_heat =  os.path.join(output_dat_heat_path,  'sander.md.temp.dat')

    prop = {
        "terms" : ['TEMP']
    }
    
    output_heat_log_path =  os.path.join(output_heat_path,  'sander.heat.log')
    # Create and launch bb
    process_mdout(input_log_path=output_heat_log_path,
            output_dat_path=output_dat_heat,
            properties=prop)