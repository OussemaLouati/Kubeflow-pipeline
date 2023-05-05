"""Kubeflow components for ingesting data."""

import kfp
from kfp.components import  OutputArtifact, OutputPath


@kfp.components.func_to_container_op
def fetch_pdb_structure( downloaded_pdb_path: OutputArtifact("dir"), pdb_code: str ,  
                        ):

    from pdb_ingestion import fetch_structure
    fetch_structure( downloaded_pdb_path, pdb_code )
    
