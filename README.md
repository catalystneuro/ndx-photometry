# ndx-photometry Extension for NWB
[![Build Status](https://travis-ci.com/akshay-jaggi/ndx-photometry.svg?branch=master)](https://travis-ci.com/akshay-jaggi/ndx-photometry)
[![Documentation Status](https://readthedocs.org/projects/ndx-photometry/badge/?version=latest)](https://ndx-photometry.readthedocs.io/en/latest/?badge=latest)

![NWB - Photometry](https://user-images.githubusercontent.com/844306/144680873-3e2d957f-97ff-45cb-b625-517f5e7dfb9f.png)

## Introduction
This is an NWB extension for storing photometry recordings and associated metadata. This extension stores photometry information across three folders in the NWB file: acquisition, processing, and general. The acquisiton folder contains a `FiberPhotometryResponseSeries` which references rows of `FibersTable`, `ExcitationSourcesTable`, `PhotodetectorsTable` and `FluorophoresTable`. The new types for this extension are in metadata and processing.

### Metadata
1. `FibersTable` stores rows for each fiber with information about the location, photodetector, and more (associated with each fiber).
2. `ExcitationSourcesTable` stores rows for each excitation source with information about the peak wavelength, source type, and the commanded voltage series of type `CommandedVoltageSeries`
3. `PhotodectorsTable` stores rows for each photodetector with information about the peak wavelength, type, etc.
4. `FluorophoresTable` stores rows for each fluorophore with information about the fluorophore itself and the injeciton site.

### Processing
1. `DeconvoledROIResponseSeries` stores DfOverF and Fluorescence traces and extends `ROIResponseSeries` to contain information about the deconvolutional and downsampling procedures performed.


This extension was developed by Akshay Jaggi, Ben Dichter, and Ryan Ly.


## Installation

```
pip install ndx-photometry
```


## Usage

```python
import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.ophys import RoiResponseSeries
from ndx_photometry import (
    FibersTable,
    PhotodetectorsTable,
    ExcitationSourcesTable,
    FluorophoresTable,
    FiberPhotometryResponseSeries,
    FiberPhotometry
)


nwbfile = NWBFile(
    session_description="session_description",
    identifier="identifier",
    session_start_time=datetime.datetime.now(datetime.timezone.utc),
)

# Create a Fibers table, and add one (or many) fiber
fibers_table = FibersTable(description="fibers table")
fibers_table.add_row(
    location="my location",
    notes="notes"
)

# Create an Excitation Sources table, and a one (or many) excitation source
excitationsources_table = ExcitationSourcesTable(description="excitation sources table")
excitationsources_table.add_row(
    peak_wavelength=700.0,
    source_type="laser",
)

# Create a Photodetectors table, and add one (or many) photodetector
photodetectors_table = PhotodetectorsTable(description="photodetectors table")
photodetectors_table.add_row(
    peak_wavelength=500.0,
    type="PMT",
    gain=100.0
)

# Create a Fluorophores table, and add one (or many) fluorophore
fluorophores_table = FluorophoresTable(description="fluorophores")
fluorophores_table.add_row(
    label="dlight",
    location="VTA",
    coordinates=(3.0,2.0,1.0),
    excitation_peak_wavelength=700.0,
    emission_peak_wavelength=500.0
)

# Here we add the metadata tables to the metadata section
nwbfile.add_lab_meta_data(
    FiberPhotometry(
        fibers=fibers_table,
        excitation_sources=excitationsources_table,
        photodetectors=photodetectors_table,
        fluorophores=fluorophores_table
    )
)

# Create a raw FiberPhotometryResponseSeries, this is your main acquisition
# We should create DynamicTableRegion referencing the correct rows for each table
fiber_ref = fibers_table.create_fiber_region(region=[0], description='source fiber')
excitation_ref = excitationsources_table.create_excitation_source_region(region=[0], description='excitation sources')
photodetector_ref = photodetectors_table.create_photodetector_region(region=[0], description='photodetector')
fluorophore_ref = fluorophores_table.create_fluorophore_region(region=[0], description='fluorophore')

fp_response_series = FiberPhotometryResponseSeries(
    name="MyFPRecording",
    data=np.random.randn(100, 1),
    unit='F',
    rate=30.0,
    fibers=fiber_ref,
    excitation_sources=excitation_ref,
    photodetectors=photodetector_ref,
    fluorophores=fluorophore_ref,
)

nwbfile.add_acquisition(fp_response_series)

# write nwb file
filename = 'test.nwb'
with NWBHDF5IO(filename, 'w') as io:
    io.write(nwbfile)

# read nwb file and check its contents
with NWBHDF5IO(filename, 'r', load_namespaces=True) as io:
    nwbfile = io.read()
    # Access and print information about the acquisition
    print(nwbfile.acquisition["MyFPRecording"])
    # Access and print all of the metadata
    print(nwbfile.lab_meta_data)
```

This extension was created using [ndx-template](https://github.com/nwb-extensions/ndx-template).
