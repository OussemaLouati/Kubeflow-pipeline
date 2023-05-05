def hydrogen_minimization(
    leap_gen_top_output_path: str,
    output_h_min_path: str,
    output_h_min_energy_path: str,
    mlpipeline_ui_metadata_path: str
    ):

    from amber.system_minimization.hydrogen_minimization import minimize_hydrogen, check_hydrogen_energy_minimization
    from plotly_chart_generation.plots import plot_energy_minimization
    from plotly_chart_generation.utils import export_image_as_png  

    minimize_hydrogen(leap_gen_top_output_path, output_h_min_path )
    
    check_hydrogen_energy_minimization(output_h_min_path, output_h_min_energy_path)
    

    ## TODO : PLOTLY VISUALISATION
    encoded_chart_image = plot_energy_minimization(output_h_min_energy_path, "sander.h_min.energy.dat")
    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])



def energy_sys_minimization(
    ligand_code: str ,
    output_h_min_path: str,
    leap_gen_top_output_path: str,
    output_min_energy_path: str,
    output_dat_min_path: str,
    mlpipeline_ui_metadata_path: str
    ):

    from amber.system_minimization.system_minimization import minimize_system, check_system_minimization
    from plotly_chart_generation.plots import plot_energy_minimization
    from plotly_chart_generation.utils import export_image_as_png 
    
    minimize_system(
        ligand_code ,
        output_h_min_path,
        leap_gen_top_output_path,
        output_min_energy_path,
    )
    
    check_system_minimization(
        output_min_energy_path,
        output_dat_min_path ,
    )
    

    ## TODO : PLOTLY VISUALISATION
    encoded_chart_image = plot_energy_minimization(output_dat_min_path, 'sander.n_min.energy.dat')

    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])



def en_system_minimization(
    output_pdb_path: str,
    output_min_path: str,
    output_dat_path: str,
    mlpipeline_ui_metadata_path:str
    ):

    from amber.system_minimization.system_minimization import run_system_minimization, check_minimization_results
    from plotly_chart_generation.plots import plot_energy_minimization
    from plotly_chart_generation.utils import export_image_as_png
    
    run_system_minimization(
        output_pdb_path,
        output_min_path,
    )
    
    check_minimization_results(
        output_min_path,
        output_dat_path,
    )
    

    ## TODO : PLOTLY VISUALISATION
    encoded_chart_image = plot_energy_minimization(output_dat_path, 'sander.min.energy.dat')

    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])