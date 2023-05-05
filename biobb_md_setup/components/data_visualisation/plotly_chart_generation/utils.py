"""Plotly utility methods."""

import os
import json
import tempfile
import base64
import plotly
import plotly.graph_objs as go
from plotly import subplots

def plot_potential_energy(output_energy_path: str, 
                         dat_file_name: str, 
                         title: str ,
                         xaxis_title: str, 
                         yaxis_title: str):

    output_h_min_dat_path =  os.path.join(output_energy_path, dat_file_name)

    #Read data from file and filter energy values higher than 1000 Kj/mol^-1
    with open(output_h_min_dat_path,'r') as energy_file:
        x,y = map(
            list,
            zip(*[
                (float(line.split()[0]),float(line.split()[1]))
                for line in energy_file 
                if not line.startswith(("#","@")) 
                if float(line.split()[1]) < 1000 
            ])
        )

    fig = go.Figure ({
        "data": [go.Scatter(x=x, y=y)],
        "layout": go.Layout(title=title,
                            xaxis=dict(title = xaxis_title),
                            yaxis=dict(title = yaxis_title)
                           )
    })

    export_path= create_temp_file()

    fig.write_image(export_path)

    return encode_image_base64(export_path)



def plot_npt_energy(output_energy_path: str, dat_file_name: str):

    output_dat_npt_path =  os.path.join(output_energy_path, dat_file_name)
    # Read pressure and density data from file 
    with open(output_dat_npt_path,'r') as pd_file:
        x,y,z = map(
            list,
            zip(*[
                (float(line.split()[0]),float(line.split()[1]),float(line.split()[2]))
                for line in pd_file 
                if not line.startswith(("#","@")) 
            ])
        )

    trace1 = go.Scatter(
        x=x,y=y
    )
    trace2 = go.Scatter(
        x=x,y=z
    )

    fig = subplots.make_subplots(rows=1, cols=2, print_grid=False)

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)

    fig['layout']['xaxis1'].update(title='Time (ps)')
    fig['layout']['xaxis2'].update(title='Time (ps)')
    fig['layout']['yaxis1'].update(title='Pressure (bar)')
    fig['layout']['yaxis2'].update(title='Density (Kg*m^-3)')

    fig['layout'].update(title='Pressure and Density during NPT Equilibration')
    fig['layout'].update(showlegend=False)

    export_path= create_temp_file()

    fig.write_image(export_path)

    return encode_image_base64(export_path)


def rms_md(output_simulation_path: str, first_dat: str, exp_dat: str): 
    
    output_rms_first =  os.path.join(output_simulation_path,  first_dat)
    # Read RMS vs first snapshot data from file 
    with open(output_rms_first,'r') as rms_first_file:
        x,y = map(
            list,
                zip(*[
                    (float(line.split()[0]),float(line.split()[1]))
                        for line in rms_first_file 
                            if not line.startswith(("#","@")) 
            ])
        )
    

    output_rms_exp =  os.path.join(output_simulation_path,  exp_dat)
    # Read RMS vs experimental structure data from file 
    with open(output_rms_exp,'r') as rms_exp_file:
        x2,y2 = map(
            list,
                zip(*[
                    (float(line.split()[0]),float(line.split()[1]))
                        for line in rms_exp_file
                            if not line.startswith(("#","@")) 
            ])
        )
    
    trace1 = go.Scatter(
        x = x,
        y = y,
        name = 'RMSd vs first'
    )

    trace2 = go.Scatter(
        x = x,
        y = y2,
        name = 'RMSd vs exp'
    )

    data = [trace1, trace2]


    fig = go.Figure ({
        "data": data,
        "layout": go.Layout(title="RMSd during free MD Simulation",
                        xaxis=dict(title = "Time (ps)"),
                        yaxis=dict(title = "RMSd (Angstrom)")
                       )
    })

    export_path= create_temp_file()

    fig.write_image(export_path)

    return encode_image_base64(export_path)


def rgyr_data(output_simulation_path: str, filename: str):

    output_rgyr =  os.path.join(output_simulation_path,  filename)
    # Read Rgyr data from file 
    with open(output_rgyr,'r') as rgyr_file:
        x,y = map(
        list,
        zip(*[
            (float(line.split()[0]),float(line.split()[1]))
            for line in rgyr_file 
            if not line.startswith(("#","@")) 
        ])
    )


    fig = go.Figure ({
    "data": [go.Scatter(x=x, y=y)],
    "layout": go.Layout(title="Radius of Gyration",
                        xaxis=dict(title = "Time (ps)"),
                        yaxis=dict(title = "Rgyr (Angstrom)")
                       )
    })

    export_path= create_temp_file()

    fig.write_image(export_path)

    return encode_image_base64(export_path)

def export_image_as_png(mlpipeline_ui_metadata_path,encoded_chart_list):
    outputs = []
    for encoded_chart_image in encoded_chart_list:
        chart_image_tag = f'<img src="data:image/png;base64,{encoded_chart_image}" />'
        outputs.append({"type": "web-app", "storage": "inline", "source": chart_image_tag})

    metadata = {
        "outputs": outputs
    }
    with open(mlpipeline_ui_metadata_path, "w") as metadata_file:
        json.dump(metadata, metadata_file)


def encode_image_base64(export_path):
    with open(export_path, "rb") as f:
        encoded_chart = base64.b64encode(f.read())

    return str(encoded_chart.decode())


def create_temp_file():
    return os.path.join(
        tempfile._get_default_tempdir(), next(tempfile._get_candidate_names()) + ".png"
    )