
import os


def minimize_system(
        ligand_code: str ,
        output_h_min_path: str,
        leap_gen_top_output_path: str,
        output_min_energy_path: str,
    ):
    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun

    os.makedirs(output_min_energy_path)
    # Create prop dict and inputs/outputs

    output_n_min_traj_path =  os.path.join(output_min_energy_path, 'sander.n_min.x')
    output_n_min_rst_path =  os.path.join(output_min_energy_path, 'sander.n_min.rst')
    output_n_min_log_path =  os.path.join(output_min_energy_path, 'sander.n_min.log')

    prop = {
        'simulation_type' : "min_vacuo",
        "mdin" : { 
            'maxcyc' : 500,
            'ntpr' : 5,
            'restraintmask' : '\":' + ligand_code + '\"',
            'restraint_wt' : 500.0
        }
    }
    
    
    output_h_min_rst_path =  os.path.join(output_h_min_path, 'sander.h_min.rst')
    output_top_path =  os.path.join(leap_gen_top_output_path, 'structure.leap.top')

    # Create and launch bb
    sander_mdrun(input_top_path=output_top_path,
            input_crd_path=output_h_min_rst_path,
            output_traj_path=output_n_min_traj_path,
            output_rst_path=output_n_min_rst_path,
            output_log_path=output_n_min_log_path,
            properties=prop)


def check_system_minimization(
    output_min_energy_path: str,
    output_dat_min_path: str,
    ):
    # Import module
    from biobb_amber.process.process_minout import process_minout
    
    os.makedirs(output_dat_min_path)
    # Create prop dict and inputs/outputs
    
    output_n_min_dat_path =  os.path.join(output_dat_min_path, 'sander.n_min.energy.dat')

    prop = {
        "terms" : ['ENERGY']
    }
   
    output_n_min_log_path =  os.path.join(output_min_energy_path, 'sander.n_min.log')
    
    # Create and launch bb
    process_minout(input_log_path=output_n_min_log_path,
            output_dat_path=output_n_min_dat_path,
            properties=prop)



def run_system_minimization(
    output_pdb_path: str,
    output_min_path: str,
    ):  
    # Import module
    from biobb_amber.sander.sander_mdrun import sander_mdrun
    
    os.makedirs(output_min_path)

    # Create prop dict and inputs/outputs
    
    output_min_traj_path =  os.path.join(output_min_path,  'sander.min.x')
    output_min_rst_path =  os.path.join(output_min_path,  'sander.min.rst')
    output_min_log_path =  os.path.join(output_min_path,  'sander.min.log')

    prop = {
        "simulation_type" : "minimization",
        "mdin" : { 
            'maxcyc' : 300, # Reducing the number of minimization steps for the sake of time
            'ntr' : 1,      # Overwritting restrain parameter
            'restraintmask' : '\"!:WAT,Cl-,Na+\"',      # Restraining solute
            'restraint_wt' : 15.0                       # With a force constant of 50 Kcal/mol*A2
        }
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_ions_crd_path =  os.path.join(output_pdb_path,  'structure.ions.crd')

    # Create and launch bb
    sander_mdrun(input_top_path=output_ions_top_path,
                input_crd_path=output_ions_crd_path,
                input_ref_path=output_ions_crd_path,
                output_traj_path=output_min_traj_path,
                output_rst_path=output_min_rst_path,
                output_log_path=output_min_log_path,
                properties=prop)



def check_minimization_results(
    output_min_path: str,
    output_dat_path: str,
    ):  
    # Import module
    from biobb_amber.process.process_minout import process_minout
    
    os.makedirs(output_dat_path)
    # Create prop dict and inputs/outputs
    
    output_dat =  os.path.join(output_dat_path,  'sander.min.energy.dat')

    prop = {
        "terms" : ['ENERGY']
    }
    
    output_min_log_path =  os.path.join(output_min_path,  'sander.min.log')

    # Create and launch bb
    process_minout(input_log_path=output_min_log_path,
            output_dat_path=output_dat,
            properties=prop)