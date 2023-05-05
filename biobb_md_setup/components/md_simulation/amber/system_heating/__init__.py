def warm_sys_up(
    output_pdb_path: str,
    output_min_path: str,
    output_heat_path: str,
    output_dat_heat_path: str,
    mlpipeline_ui_metadata_path: str
    ):

    from amber.system_heating.system_warming_up import warm_system_up, check_system_warm_up_result
    from plotly_chart_generation.plots import plot_energy_system_warmup
    from plotly_chart_generation.utils import export_image_as_png
    
    warm_system_up(
        output_pdb_path,
        output_min_path,
        output_heat_path,
    )

    check_system_warm_up_result(
        output_heat_path,
        output_dat_heat_path,
    )

    ## TODO : PLOTLY VISUALISATION
    encoded_chart_image = plot_energy_system_warmup(output_dat_heat_path)

    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])