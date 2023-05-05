def equilibrate_sys_nvt(
    output_pdb_path: str,
    output_heat_path: str,
    output_nvt_path: str,
    output_nvt_dat_path: str,
    mlpipeline_ui_metadata_path: str
    ):

    from amber.system_equilibration.nvt import equilibrate_system_nvt, check_nvt_equilibration
    from plotly_chart_generation.plots import plot_energy_nvt
    from plotly_chart_generation.utils import export_image_as_png

    equilibrate_system_nvt(
        output_pdb_path,
        output_heat_path,
        output_nvt_path,
    )

    check_nvt_equilibration(
        output_nvt_path,
        output_nvt_dat_path,
    )

    encoded_chart_image = plot_energy_nvt(output_nvt_dat_path)
    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])


def equilibrate_sys_npt(
    output_pdb_path: str,
    output_nvt_path: str,
    output_npt_path: str,
    output_npt_dat_path: str,
    mlpipeline_ui_metadata_path: str
    ):

    from amber.system_equilibration.npt import equilibrate_system_npt, check_npt_equilibration
    from plotly_chart_generation.plots import plot_energy_npt
    from plotly_chart_generation.utils import export_image_as_png

    equilibrate_system_npt( output_pdb_path, output_nvt_path,  output_npt_path  )

    check_npt_equilibration(output_npt_path, output_npt_dat_path  )

    encoded_chart_image = plot_energy_npt(output_npt_dat_path)
    export_image_as_png(mlpipeline_ui_metadata_path,[encoded_chart_image])