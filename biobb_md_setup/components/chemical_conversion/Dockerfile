FROM quay.io/biocontainers/biobb_chemistry:3.6.0--pyhdfd78af_0

# upgrade pip
RUN pip install pip==21.0.1

# install external libraries
ADD biobb_md_setup/components/chemical_conversion/requirements.txt /tmp/requirements.txt 
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app 

# add chemical conversion module directory
COPY biobb_md_setup/components/chemical_conversion/ . 

# install chemical_conversion package
RUN pip install -e . 