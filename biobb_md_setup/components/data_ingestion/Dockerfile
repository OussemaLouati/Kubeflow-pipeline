FROM quay.io/biocontainers/biobb_io:3.6.0--pyhdfd78af_0 

# upgrade pip
RUN pip install pip==21.0.1

# install external libraries
ADD biobb_md_setup/components/data_ingestion/requirements.txt /tmp/requirements.txt 
RUN pip install --no-cache-dir -r /tmp/requirements.txt


WORKDIR /app 

# add data ingestion module directory
ADD biobb_md_setup/components/data_ingestion/ . 

# install pdb_ingestion package
RUN pip install -e .  



