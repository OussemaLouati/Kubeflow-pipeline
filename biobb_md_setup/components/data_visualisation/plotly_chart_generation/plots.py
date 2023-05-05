"""Plotly chart generation and export to an image"""


def plot_energy_minimization(output_energy_path: str, dat_file_name: str):

    from plotly_chart_generation.utils import plot_potential_energy
    
    return plot_potential_energy(output_energy_path = output_energy_path, 
                                  dat_file_name = dat_file_name,
                                  title= "Energy Minimization",
                                  xaxis_title= "Energy Minimization Step" ,
                                  yaxis_title= "Potential Energy kcal/mol" )

def plot_energy_system_warmup(output_dat_heat_path: str):

    from plotly_chart_generation.utils import plot_potential_energy
     
    return plot_potential_energy( output_energy_path = output_dat_heat_path, 
                                dat_file_name = 'sander.md.temp.dat',
                                title= "Heating process",
                                xaxis_title= "Heating Step (ps)" ,
                                yaxis_title= "Temperature (K)" )

def plot_energy_nvt(output_nvt_dat_path: str):
    from plotly_chart_generation.utils import plot_potential_energy
    return plot_potential_energy(  output_energy_path = output_nvt_dat_path, 
                                   dat_file_name = 'sander.md.nvt.temp.dat',
                                   title= "NVT equilibration",
                                   xaxis_title= "Equilibration Step (ps)" ,
                                   yaxis_title= "Temperature (K)" 
                              )

def plot_energy_npt(output_npt_dat_path: str):
     from plotly_chart_generation.utils import plot_npt_energy
     return plot_npt_energy(  output_energy_path = output_npt_dat_path, 
                              dat_file_name = 'sander.md.npt.dat',
                              )



def rms_during_md(output_simulation_path: str, first_dat: str , exp_dat:str):
     from plotly_chart_generation.utils import rms_md
     return rms_md(  output_simulation_path = output_simulation_path, 
                     first_dat=first_dat , 
                     exp_dat= exp_dat
                              )


def rgyr_data_viz(output_simulation_path: str, filename: str):
     from plotly_chart_generation.utils import rgyr_data
     return rgyr_data(  output_simulation_path = output_simulation_path, 
                        filename= filename, 
                    )