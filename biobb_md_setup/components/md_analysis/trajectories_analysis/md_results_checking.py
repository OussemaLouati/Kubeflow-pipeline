import os

def check_results(
    output_pdb_path: str,
    output_free_path: str,
    output_simulation_path: str,
    ligand_code: str,
    mlpipeline_ui_metadata_path: str,
    leap_gen_top_output_path: str
    ): 

    # cpptraj_rms: Computing Root Mean Square deviation to analyse structural stability 
    # RMSd against minimized and equilibrated snapshot (backbone atoms)   
    
    # Import module
    from biobb_analysis.ambertools.cpptraj_rms import cpptraj_rms
    from biobb_analysis.ambertools.cpptraj_rgyr import cpptraj_rgyr
    from plotly_chart_generation.plots import rms_during_md, rgyr_data_viz
    from plotly_chart_generation.utils import export_image_as_png 


    os.makedirs(output_simulation_path)
    # Create prop dict and inputs/outputs
    
    output_rms_first =  os.path.join(output_simulation_path,  ligand_code + '_rms_first.dat')

    prop = {
        'mask': 'backbone',
        'reference': 'first'
    }

    output_ions_top_path =  os.path.join(output_pdb_path,  'structure.ions.parmtop')
    output_free_traj_path =  os.path.join(output_free_path,  'sander.free.netcdf')

    # Create and launch bb
    cpptraj_rms(input_top_path=output_ions_top_path,
            input_traj_path=output_free_traj_path,
            output_cpptraj_path=output_rms_first,
            properties=prop)



    # Create prop dict and inputs/outputs
    output_rms_exp =  os.path.join(output_simulation_path,  ligand_code + '_rms_exp.dat')

    prop = {
        'mask': 'backbone',
        'reference': 'experimental'
    }
    
    output_path =  os.path.join(leap_gen_top_output_path,  'structure.leap.pdb') 

    # Create and launch bb
    cpptraj_rms(input_top_path=output_ions_top_path,
            input_traj_path=output_free_traj_path,
            output_cpptraj_path=output_rms_exp,
            input_exp_path=output_path, 
            properties=prop)


    # cpptraj_rgyr: Computing Radius of Gyration to measure the protein compactness during the free MD simulation   

    # Create prop dict and inputs/outputs
    
    output_rgyr =  os.path.join(output_simulation_path,  ligand_code+'_rgyr.dat')

    prop = {
        'mask': 'backbone'  
    }

    # Create and launch bb
    cpptraj_rgyr(input_top_path=output_ions_top_path,
            input_traj_path=output_free_traj_path,
            output_cpptraj_path=output_rgyr,
            properties=prop)


    encoded_chart_1_image = rms_during_md(output_simulation_path,  ligand_code + '_rms_first.dat', ligand_code + '_rms_exp.dat')
    encoded_chart_2_image = rgyr_data_viz(output_simulation_path,  ligand_code+'_rgyr.dat')
    
    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_1_image, encoded_chart_2_image])