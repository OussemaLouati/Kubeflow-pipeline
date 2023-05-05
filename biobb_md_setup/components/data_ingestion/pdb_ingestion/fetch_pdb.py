"""Module to download a PDB file."""


def download_pdb_file(
    downloaded_pdb_path: str,
    pdb_code: str ,  
    ):
    """
    Fetch and download input PDB file.

    Args:
        pdb_code: pdb code to be used to download the pdb file

    Returns:
        downloaded_pdb_path: path to save the downloaded pdb to
    """

    # Import module
    from biobb_io.api.pdb import pdb
    import os

    # Create properties dict and inputs/outputs

    os.makedirs(downloaded_pdb_path)
    downloaded_pdb =  os.path.join(downloaded_pdb_path, pdb_code + '.pdb')  
    
    prop = {
        'pdb_code': pdb_code,
        'filter': False
    }

    #Create and launch bb
    pdb(output_pdb_path=downloaded_pdb,
        properties=prop)

    
