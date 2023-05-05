def fetch_structure(
    downloaded_pdb_path: str,
    pdb_code: str ,  
    ):

    # Import module
    from pdb_ingestion.fetch_pdb import download_pdb_file 
    download_pdb_file(downloaded_pdb_path, pdb_code)
