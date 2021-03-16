Overview
========

Introduction
------------
This is an NWB extension for storing photometry recordings and associated metadata. This extension stores photometry information across three folders in the NWB file: acquisition, processing, and general. The acquisiton folder contains an ROIResponseSeries (inherited from `pynwb.ophys`), which references rows of a FibersTable rather than 2 Photon ROIs. The new types for this extension are in metadata and processing

Metadata
---------
1. ``FibersTable`` stores rows for each fiber with information about the location, excitation, source, photodetector, fluorophore, and more (associated with each fiber).
2. ``ExcitationSourcesTable`` stores rows for each excitation source with information about the peak wavelength, source type, and the commanded voltage series of type ``CommandedVoltageSeries``
3. ``PhotodectorsTable`` stores rows for each photodetector with information about the peak wavelength, type, etc.
4. ``FluorophoresTable`` stores rows for each fluorophore with information about the fluorophore itself and the injeciton site.

Processing
----------
1. ``DeconvoledROIResponseSeries`` stores DfOverF and Fluorescence traces and extends ``ROIResponseSeries`` to contain information about the deconvolutional and downsampling procedures performed.


This extension was developed by Ryan Ly, Ben Dichter, and Akshay Jaggi.
