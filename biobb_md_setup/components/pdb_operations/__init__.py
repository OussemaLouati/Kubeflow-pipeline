import kfp
from kfp.components import InputArtifact, OutputArtifact



@kfp.components.func_to_container_op
def preprocess_pdb_structure(
    downloaded_pdb_path: InputArtifact("dir"),
    nowat_pdb_path: OutputArtifact("dir"),
    removed_ligands_pdb_path: OutputArtifact("dir"),
    pdb_code: str ,  
    ):

    # Import module
    from structure_utils import preprocess_structure
    preprocess_structure(
        downloaded_pdb_path,
        nowat_pdb_path,
        removed_ligands_pdb_path,
        pdb_code,  
    )


@kfp.components.func_to_container_op
def extract_ligands(
    output_pdb4amber_path: InputArtifact("dir"),
    ligand_file_path: OutputArtifact("dir"),
    ligand_code: str ,  
    ):

    # Import module
    from structure_utils.preprocessing import extract_ligand_structure
    extract_ligand_structure(ligand_code, output_pdb4amber_path,ligand_file_path)