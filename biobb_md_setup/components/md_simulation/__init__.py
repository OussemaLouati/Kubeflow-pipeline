"""MD simulation using Amber tools."""

import kfp
from kfp.components import InputArtifact, OutputArtifact, OutputPath   


@kfp.components.func_to_container_op
def amber_preparation(removed_ligands_pdb_path: InputArtifact("dir"), output_pdb4amber_path: OutputArtifact("dir"), pdb_code: str):
    
    from amber.system_topology.amber_prep import amber_prep
    amber_prep(removed_ligands_pdb_path, output_pdb4amber_path, pdb_code )

@kfp.components.func_to_container_op
def amber_topology( output_acpype_path: InputArtifact("dir"), output_pdb4amber_path: InputArtifact("dir"),
    leap_gen_top_output_path: OutputArtifact("dir"), ligand_code: str  ):

    from amber.system_topology.amber_prep import build_amber_topology

    build_amber_topology( output_acpype_path, output_pdb4amber_path, leap_gen_top_output_path,ligand_code)


@kfp.components.func_to_container_op
def hydrogen_structure_minimization(
    leap_gen_top_output_path: InputArtifact("dir"),
    output_h_min_path: OutputArtifact("dir"),
    output_h_min_energy_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):
    from amber.system_minimization import hydrogen_minimization
    hydrogen_minimization(leap_gen_top_output_path, output_h_min_path,
                            output_h_min_energy_path, mlpipeline_ui_metadata_path)

@kfp.components.func_to_container_op
def energy_system_minimization(
    ligand_code: str ,
    output_h_min_path: InputArtifact("dir"),
    leap_gen_top_output_path: InputArtifact("dir"),
    output_min_energy_path: OutputArtifact("dir"),
    output_dat_min_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):

    from amber.system_minimization import energy_sys_minimization
    energy_sys_minimization(ligand_code, output_h_min_path, leap_gen_top_output_path, output_min_energy_path,
                            output_dat_min_path, mlpipeline_ui_metadata_path)
    


@kfp.components.func_to_container_op
def solvating_system(
    leap_gen_top_output_path: InputArtifact("dir"),
    output_h_min_path: InputArtifact("dir"),
    output_ambpdb_path: OutputArtifact("dir"),
    ligand_code: str,
    output_acpype_path: InputArtifact("dir"),
    output_solv_path: OutputArtifact("dir"),
    output_pdb_path: OutputArtifact("dir"),
    ):

    from amber.system_solvation import solv_system
    solv_system(leap_gen_top_output_path, output_h_min_path, output_ambpdb_path,  ligand_code, output_acpype_path,
                    output_solv_path, output_pdb_path)
    
    

@kfp.components.func_to_container_op
def energy_minimization(
    output_pdb_path: InputArtifact("dir"),
    output_min_path: OutputArtifact("dir"),
    output_dat_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):

    from amber.system_minimization import en_system_minimization
    en_system_minimization(output_pdb_path, output_min_path, output_dat_path,mlpipeline_ui_metadata_path)



@kfp.components.func_to_container_op
def warm_system_up(
    output_pdb_path: InputArtifact("dir"),
    output_min_path: InputArtifact("dir"),
    output_heat_path: OutputArtifact("dir"),
    output_dat_heat_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):

    from amber.system_heating import warm_sys_up
    warm_sys_up(output_pdb_path, output_min_path,output_heat_path, output_dat_heat_path, mlpipeline_ui_metadata_path)


@kfp.components.func_to_container_op
def equilibrate_system_nvt(
    output_pdb_path: InputArtifact("dir"),
    output_heat_path: InputArtifact("dir"),
    output_nvt_path: OutputArtifact("dir"),
    output_nvt_dat_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):

    from amber.system_equilibration import equilibrate_sys_nvt
    equilibrate_sys_nvt(output_pdb_path,  output_heat_path, output_nvt_path, output_nvt_dat_path, mlpipeline_ui_metadata_path)


@kfp.components.func_to_container_op
def equilibrate_system_npt(
    output_pdb_path: InputArtifact("dir"),
    output_nvt_path: InputArtifact("dir"),
    output_npt_path: OutputArtifact("dir"),
    output_npt_dat_path: OutputArtifact("dir"),
    mlpipeline_ui_metadata_path: OutputPath("UI-Metadata")
    ):

    from amber.system_equilibration import equilibrate_sys_npt
    equilibrate_sys_npt(output_pdb_path, output_nvt_path, output_npt_path, output_npt_dat_path, mlpipeline_ui_metadata_path)


@kfp.components.func_to_container_op
def create_portable_binary_file(
    output_pdb_path: InputArtifact("dir"),
    output_npt_path: InputArtifact("dir"),
    output_free_path: OutputArtifact("dir"),
    ): 

    from amber.free_md.free_md_simulation import create_binary_file
    create_binary_file( output_pdb_path,output_npt_path, output_free_path )
