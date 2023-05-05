"""Setup script for packaging plotly_chart_generation."""

from setuptools import setup

setup(
    name="plotly-chart-generation",
    version="1.0.0",
    description="Plotly chart generation and export to image",
    author="oussama.louati4@gmail.com",
    install_requires=["plotly==5.10.0", "kaleido==0.2.1"],
)