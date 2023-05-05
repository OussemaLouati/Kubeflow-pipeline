
import kfp
from kfp.components import InputArtifact, OutputArtifact   


@kfp.components.func_to_container_op
def ligand_system_topology_creation(
        ligand_code: str ,
        ligand_file_path: InputArtifact("dir"), 
        output_reduce_h_path: OutputArtifact("dir"), 
        output_babel_min_path: OutputArtifact("dir"),
        output_acpype_path: OutputArtifact("dir"),
        mol_charge: int
    ):

    from bio_chemistry import ligand_sys_topology_creation
    ligand_sys_topology_creation(ligand_code, ligand_file_path, output_reduce_h_path, output_babel_min_path,
        output_acpype_path, mol_charge)