import os

def minimize_hydrogen(
    leap_gen_top_output_path: str,
    output_h_min_path: str,
    ):
    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_h_min_path)
    # Create prop dict and inputs/outputs
    
    output_h_min_traj_path =  os.path.join(output_h_min_path, 'sander.h_min.x') 
    output_h_min_rst_path =  os.path.join(output_h_min_path,  'sander.h_min.rst') 
    output_h_min_log_path =  os.path.join(output_h_min_path,  'sander.h_min.log') 

    prop = {
        'simulation_type' : "min_vacuo",
        "mdin" : { 
            'maxcyc' : 500,
            'ntpr' : 5,
            'ntr' : 1,
            'restraintmask' : '\":*&!@H=\"',
            'restraint_wt' : 50.0
        }
    }

    
    output_top_path =  os.path.join(leap_gen_top_output_path, 'structure.leap.top') 
    output_crd_path =  os.path.join(leap_gen_top_output_path, 'structure.leap.crd') 

    # Create and launch bb
    sander_mdrun(input_top_path=output_top_path,
            input_crd_path=output_crd_path,
            input_ref_path=output_crd_path,
            output_traj_path=output_h_min_traj_path,
            output_rst_path=output_h_min_rst_path,
            output_log_path=output_h_min_log_path,
            properties=prop)



def check_hydrogen_energy_minimization(
    output_h_min_path: str,
    output_h_min_energy_path: str,
    ):
    # Import module
    from biobb_amber.process.process_minout import process_minout
    
    os.makedirs(output_h_min_energy_path)
    # Create prop dict and inputs/outputs
    output_h_min_dat_path =  os.path.join(output_h_min_energy_path, 'sander.h_min.energy.dat')

    prop = {
        "terms" : ['ENERGY']
    }
    
    output_h_min_log_path =  os.path.join(output_h_min_path, 'sander.h_min.log')

    # Create and launch bb
    process_minout(input_log_path=output_h_min_log_path,
            output_dat_path=output_h_min_dat_path,
            properties=prop)  