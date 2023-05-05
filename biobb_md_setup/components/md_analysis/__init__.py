"""MD simulation using Amber tools."""

import kfp
from kfp.components import InputArtifact, OutputArtifact, OutputPath   

@kfp.components.func_to_container_op
def check_md_results(
    output_pdb_path: InputArtifact("dir"),
    output_free_path: InputArtifact("dir"),
    output_simulation_path: OutputArtifact("dir"),
    ligand_code: str,
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata"),
    leap_gen_top_output_path: InputArtifact("dir")
    ): 

    from trajectories_analysis.md_results_checking import check_results

    check_results(output_pdb_path,
        output_free_path,
        output_simulation_path,
        ligand_code,
        mlpipeline_ui_metadata_path,
        leap_gen_top_output_path )

@kfp.components.func_to_container_op
def remove_water_molecules_ions_and_correct_periodicity(
    output_pdb_path: InputArtifact("dir"),
    output_free_path: InputArtifact("dir"),
    output_imaged_traj_path: OutputArtifact("dir"),
    ligand_code: str 
    ):

    from trajectories_analysis.postprocessing import postprocess_structure

    postprocess_structure(output_pdb_path, output_free_path, output_imaged_traj_path, ligand_code)