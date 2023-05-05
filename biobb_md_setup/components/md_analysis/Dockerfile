FROM quay.io/biocontainers/biobb_analysis:3.7.0--pyhdfd78af_1

# upgrade pip
RUN pip install pip==21.0.1

# install external libraries
ADD biobb_md_setup/components/md_analysis/requirements.txt /tmp/requirements.txt 
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# install internal libraries
ADD biobb_md_setup/components/data_visualisation libraries/
RUN pip install -e libraries/

WORKDIR /app 

# add data md analysis module directory
ADD biobb_md_setup/components/md_analysis/ . 

# install trajectory_analysis package
RUN pip install -e . 

