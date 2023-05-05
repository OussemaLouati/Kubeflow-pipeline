"""Kubefloww pipeline."""

import kfp
from kfp import dsl
from biobb_md_setup.components.data_ingestion import fetch_pdb_structure
from biobb_md_setup.components.pdb_operations import preprocess_pdb_structure, extract_ligands
from biobb_md_setup.components.md_simulation import (amber_preparation, amber_topology, hydrogen_structure_minimization,
                                             energy_system_minimization, solvating_system, energy_minimization,
                                             warm_system_up, equilibrate_system_nvt, equilibrate_system_npt,
                                             create_portable_binary_file)
from biobb_md_setup.components.chemical_conversion import ligand_system_topology_creation
from biobb_md_setup.components.md_analysis import check_md_results, remove_water_molecules_ions_and_correct_periodicity


pdbCode = "3htb"
ligandCode = "JZ4"
mol_charge = 0

@dsl.pipeline(
    name="Kubeflow pipeline",
    description="Protein-ligand complex MD Setup tutorial using BioExcel Building Blocks (biobb)")
def test_pipeline(
    pdb_code: str = pdbCode,
    ligand_code: str = ligandCode,
    mol_charge: int = mol_charge
):
    
    ###########################
    #      Pipeline steps     #
    ###########################

    # Step 1: Download input PDB file
    ingest_pdb_structure = fetch_pdb_structure(
        pdb_code=pdb_code,
    )
    ingest_pdb_structure.display_name = "Download PDB structure"
    ingest_pdb_structure.image="oussemalouati/biobb_io:3.6.0"
    ingest_pdb_structure.container.set_image_pull_policy("Always")


    # Step 2: Remove water molecules and ligands
    stripping_crystallographic_water_molecule_or_heteroatom = preprocess_pdb_structure(
        downloaded_pdb_path=ingest_pdb_structure.outputs["downloaded_pdb_path"],
        pdb_code=pdb_code,
    )
    stripping_crystallographic_water_molecule_or_heteroatom.display_name = "Preprocess PDB structure"

    # Step 3: Amber preparation
    amber_prep = amber_preparation(
        removed_ligands_pdb_path=stripping_crystallographic_water_molecule_or_heteroatom.outputs["removed_ligands_pdb_path"], 
        pdb_code=pdb_code,
    )
    amber_prep.display_name = "Prepare PDB to Amber"


    # Step 4: Ligand System Topology step I : ligand structure extraction
    extract_ligand_structure_heteroatoms = extract_ligands(
        ligand_code=ligand_code,
        output_pdb4amber_path=amber_prep.outputs["output_pdb4amber_path"],
    )
    extract_ligand_structure_heteroatoms.display_name = "Extract ligand structure"


    # Step 5: Ligand System Topology 
    topology_system = ligand_system_topology_creation(
        ligand_code=ligand_code,
        ligand_file_path=extract_ligand_structure_heteroatoms.outputs["ligand_file_path"],
        mol_charge=mol_charge
    )
    topology_system.display_name = "Create topology system"

    # Step 6: Amber topology building
    amber_topology_building = amber_topology (
        ligand_code=ligand_code,
        output_pdb4amber_path=amber_prep.outputs["output_pdb4amber_path"],
        output_acpype_path=topology_system.outputs["output_acpype_path"]
    )
    amber_topology_building.display_name = "Build amber topology"

    # Step 7: Hydrogen minimization
    hydrogen_minimization = hydrogen_structure_minimization(
        leap_gen_top_output_path=amber_topology_building.outputs["leap_gen_top_output_path"],
    )
    hydrogen_minimization.display_name = "Minimize Hydrogen"
    
    # Step 8: System minimization
    system_minimization = energy_system_minimization(
        ligand_code = ligand_code,
        output_h_min_path=hydrogen_minimization.outputs["output_h_min_path"],
        leap_gen_top_output_path=amber_topology_building.outputs["leap_gen_top_output_path"],
    )
    system_minimization.display_name = "Minimize system"  

    # Step 9: System solvation
    system_solvation = solvating_system(
        leap_gen_top_output_path=amber_topology_building.outputs["leap_gen_top_output_path"],
        output_h_min_path=hydrogen_minimization.outputs["output_h_min_path"],  
        ligand_code=ligand_code,
        output_acpype_path=topology_system.outputs["output_acpype_path"],
    )
    system_solvation.display_name = "Create solvent box and solvating the system"    

    
    # Step 10: Run system minimization
    system_minimization_running = energy_minimization(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
    )
    system_minimization_running.display_name = "Run system minimization" 

    
    # Step 11: Heating the system up
    system_warm_up = warm_system_up(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_min_path=system_minimization_running.outputs["output_min_path"],
    )
    system_warm_up.display_name = "Warm The system up" 
    
 
    # Step 12: NVT equilbration 
    nvt_system_equilibration = equilibrate_system_nvt(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_heat_path=system_warm_up.outputs["output_heat_path"],
    )
    nvt_system_equilibration.display_name = "NVT Equilibration" 
    

    # Step 13: NPT equilbration 
    npt_system_equilibration = equilibrate_system_npt(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_nvt_path=nvt_system_equilibration.outputs["output_nvt_path"]
    )
    npt_system_equilibration.display_name = "NPT Equilibration" 
    
    # Step 14: Molecular dynamics free simulation 
    portable_binary_file_creation = create_portable_binary_file(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_npt_path=npt_system_equilibration.outputs["output_npt_path"],
    )
    portable_binary_file_creation.display_name = "Free MD simulation" 

    # Step 15: Molecular dynamics results checking
    md_results_checking = check_md_results(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_free_path=portable_binary_file_creation.outputs["output_free_path"],
        leap_gen_top_output_path=amber_topology_building.outputs["leap_gen_top_output_path"],
        ligand_code=ligand_code,
    )
    md_results_checking.display_name = "Check MD simulation results" 
    
    # Step 16: Final postprocessing step
    water_molecules_ions_removal_and_periodicity_correction = remove_water_molecules_ions_and_correct_periodicity(
        output_pdb_path=system_solvation.outputs["output_pdb_path"],
        output_free_path=portable_binary_file_creation.outputs["output_free_path"],
        ligand_code=ligand_code,
    )
    water_molecules_ions_removal_and_periodicity_correction.display_name = "Strip out water molecules/ions and correct periodicity issues"
    

    #######################################
    # Container base images for each step #
    #######################################

    #  assign the container image for all the tasks 
    #  OPTIONALLY : we can set resource requets also
    for task in [
        amber_prep,
        amber_topology_building,
        hydrogen_minimization,
        system_minimization,
        system_solvation,
        system_minimization_running,
        system_warm_up,
        nvt_system_equilibration,
        npt_system_equilibration,
        portable_binary_file_creation
    ]:
        task.set_cpu_request("4").set_memory_request("6Gi")
        task.container.set_image_pull_policy("Always")
        task.image="oussemalouati/biobb_amber:3.6.2"

    for task in [
        topology_system
    ]:
        task.set_cpu_request("4").set_memory_request("6Gi")
        task.container.set_image_pull_policy("Always")
        task.image="oussemalouati/biobb_chemistry:3.6.0"
    
    for task in [
        stripping_crystallographic_water_molecule_or_heteroatom,
	    extract_ligand_structure_heteroatoms,
    ]:
        task.set_cpu_request("4").set_memory_request("6Gi")
        task.container.set_image_pull_policy("Always")
        task.image="oussemalouati/biobb_structure_utils:3.6.1"
    
   
    for task in [
        md_results_checking,
        water_molecules_ions_removal_and_periodicity_correction
    ]:
        task.set_cpu_request("4").set_memory_request("6Gi")
        task.container.set_image_pull_policy("Always")
        task.image="oussemalouati/biobb_analysis:3.7.0"

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(
        pipeline_func=test_pipeline,
        package_path=__file__.replace(".py", ".yaml"),
    )
