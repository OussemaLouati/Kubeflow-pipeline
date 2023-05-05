FROM quay.io/biocontainers/biobb_structure_utils:3.6.1--pyhdfd78af_0

# upgrade pip
RUN pip install pip==21.0.1

# install external libraries
ADD biobb_md_setup/components/pdb_operations/requirements.txt /tmp/requirements.txt 
RUN pip install --no-cache-dir -r /tmp/requirements.txt


WORKDIR /app 

# add pdb operations module directory
ADD biobb_md_setup/components/pdb_operations/ . 

# install structure_utils package
RUN pip install -e .  
