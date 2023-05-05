FROM quay.io/biocontainers/biobb_amber:3.6.2--pyhdfd78af_0

# upgrade pip
RUN pip install pip==21.0.1

# install external libraries
ADD biobb_md_setup/components/md_simulation/requirements.txt /tmp/requirements.txt 
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# install internal libraries
ADD biobb_md_setup/components/data_visualisation libraries/
RUN pip install -e libraries/

WORKDIR /app 

# add data md simulation module directory
ADD biobb_md_setup/components/md_simulation/ . 

# install amber package
RUN pip install -e .  

