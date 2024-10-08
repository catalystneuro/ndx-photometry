# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBDatasetSpec,
    NWBRefSpec,
    NWBLinkSpec,
)


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-photometry""",
        version="""0.5.0""",
        doc="""NWB extension for fiber photometry data""",
        author=[
            "Akshay Jaggi",
            "Ben Dichter",
            "Anna Szonja Weigl",
            "Cody Baker",
            "Paul Adkisson",
            "Luiz Tauffer",
            "Alessandra Trapani",
            "Ryan Ly",
        ],
        contact=[
            "akshay.x.jaggi@gmail.com",
            "ben.dichter@catalystneuro.com",
            "szonja.weigl@catalystneuro.com",
            "cody.baker@catalystneuro.com",
            "paul.adkisson@catalystneuro.com",
            "luiz.tauffer@catalystneuro.com",
            "alessandra.trapani@catalystneuro.com",
            "rly@lbl.gov",
        ],
    )
    ns_builder.include_namespace("core")

    fibers_table = NWBGroupSpec(
        neurodata_type_def="FibersTable",
        neurodata_type_inc="DynamicTable",
        name="fibers",
        doc="Extends DynamicTable to hold various Fibers",
        datasets=[
            NWBDatasetSpec(
                name="location",
                doc="location of fiber",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="coordinates",
                doc="Fiber placement in stereotactic coordinates (AP, ML, DV) mm relative to Bregma",
                dtype="float",
                shape=(None, 3),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="notes",
                doc="description of fiber",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="fiber_model_number",
                doc="fiber model number",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="dichroic_model_number",
                doc="dichroic model number",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    photodetectors_table = NWBGroupSpec(
        neurodata_type_def="PhotodetectorsTable",
        neurodata_type_inc="DynamicTable",
        name="photodetectors",
        doc="Extends DynamicTable to hold various Photodetectors",
        datasets=[
            NWBDatasetSpec(
                name="peak_wavelength",
                doc="peak wavelength of photodetector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
                attributes=[NWBAttributeSpec(name="unit", doc="wavelength unit", value="nanometers", dtype="text")],
            ),
            NWBDatasetSpec(
                name="type",
                doc='"PMT" or "photodiode"',
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="gain",
                doc="gain on the photodetector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="model_number",
                doc="model number of the photodetector",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    excitationsources_table = NWBGroupSpec(
        neurodata_type_def="ExcitationSourcesTable",
        neurodata_type_inc="DynamicTable",
        name="excitation_sources",
        doc="Extends DynamicTable to hold various Excitation Sources",
        datasets=[
            NWBDatasetSpec(
                name="peak_wavelength",
                doc="peak wavelength of the excitation source",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                attributes=[NWBAttributeSpec(name="unit", doc="wavelength unit", value="nanometers", dtype="text")],
            ),
            NWBDatasetSpec(
                name="source_type",
                doc='"LED" or "laser"',
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="commanded_voltage",
                doc="references CommandedVoltageSeries",
                dtype=NWBRefSpec(target_type="CommandedVoltageSeries", reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="output",
                doc="excitation output, references TimeSeries",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="model_number",
                doc="model number of the excitation source",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    commandedvoltage_series = NWBGroupSpec(
        neurodata_type_def="CommandedVoltageSeries",
        neurodata_type_inc="TimeSeries",
        doc="Extends TimeSeries to hold a Commanded Voltage",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="voltages (length number timesteps) in unit volts",
                dtype="float",
                shape=(None,),
                attributes=[NWBAttributeSpec(name="unit", doc="data unit", value="volts", dtype="text")],
            ),
            NWBDatasetSpec(
                name="frequency",
                doc="voltage frequency in unit hertz",
                dtype="float",
                attributes=[NWBAttributeSpec(name="unit", doc="frequency unit", value="hertz", dtype="text")],
                quantity="?",
            ),
            NWBDatasetSpec(
                name="power",
                doc="voltage power in unit volts",
                dtype="float",
                attributes=[NWBAttributeSpec(name="unit", doc="power unit", value="volts", dtype="text")],
            ),
        ],
    )

    multi_commanded_voltage = NWBGroupSpec(
        name="commanded_voltages",
        neurodata_type_def="MultiCommandedVoltage",
        neurodata_type_inc="NWBDataInterface",
        doc="holds CommandedVoltageSeries objects",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="CommandedVoltageSeries",
                quantity="*",
                doc="commanded voltage series",
            )
        ],
    )

    fluorophores_table = NWBGroupSpec(
        neurodata_type_def="FluorophoresTable",
        neurodata_type_inc="DynamicTable",
        name="fluorophores",
        doc="Extends DynamicTable to hold various Fluorophores",
        datasets=[
            NWBDatasetSpec(
                name="label",
                doc="name of fluorophore",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="location",
                doc="injection brain region name",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="coordinates",
                doc="Fluorophore injection location in stereotactic coordinates (AP, ML, DV) mm relative to Bregma",
                dtype="float",
                shape=(None, 3),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="emission_peak_wavelength",
                doc="Peak wavelength of emission of the fluorophore, in nanometers.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                attributes=[NWBAttributeSpec(name="unit", doc="wavelength unit", value="nanometers", dtype="text")],
            ),
            NWBDatasetSpec(
                name="excitation_peak_wavelength",
                doc="Peak wavelength of excitation of the fluorophore, in nanometers.",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                attributes=[NWBAttributeSpec(name="unit", doc="wavelength unit", value="nanometers", dtype="text")],
            ),
        ],
    )

    fiber_photometry = NWBGroupSpec(
        neurodata_type_def="FiberPhotometry",
        neurodata_type_inc="LabMetaData",
        name="fiber_photometry",
        doc="all Fiber Photometry metadata",
        groups=[
            NWBGroupSpec(name="fibers", neurodata_type_inc="FibersTable", doc="table of fibers used"),
            NWBGroupSpec(
                name="excitation_sources",
                neurodata_type_inc="ExcitationSourcesTable",
                doc="table of excitation sources used",
            ),
            NWBGroupSpec(
                name="photodetectors", neurodata_type_inc="PhotodetectorsTable", doc="table of photodetectors used"
            ),
            NWBGroupSpec(name="fluorophores", neurodata_type_inc="FluorophoresTable", doc="table of fluorophores used"),
            NWBGroupSpec(
                name="commanded_voltages",
                neurodata_type_inc="MultiCommandedVoltage",
                doc="multiple commanded voltage container",
                quantity="?",
            ),
        ],
    )

    fiberphotometryresponse_series = NWBGroupSpec(
        neurodata_type_def="FiberPhotometryResponseSeries",
        neurodata_type_inc="TimeSeries",
        doc="Extends TimeSeries to hold Fiber Photometry data",
        datasets=[
            NWBDatasetSpec(
                name="fibers",
                doc="references row(s) of FibersTable",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="excitation_sources",
                doc="references row(s) of ExcitationSourcesTable",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="fluorophores",
                doc="references row(s) of FluorophoresTable",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="photodetectors",
                doc="references row(s) of PhotodetectorsTable",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            ),
        ],
    )

    deconvolved_fiberphotometryresponse_series_series = NWBGroupSpec(
        neurodata_type_def="DeconvolvedFiberPhotometryResponseSeries",
        neurodata_type_inc="FiberPhotometryResponseSeries",
        doc="Extends FiberPhotometryResponseSeries to hold deconvolved data",
        links=[
            NWBLinkSpec(
                name="raw",
                target_type="FiberPhotometryResponseSeries",
                doc="ref to fiber photometry response series",
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name="deconvolution_filter",
                doc="description of deconvolution filter used",
                dtype="text",
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="downsampling_filter",
                doc="description of downsampling filter used",
                dtype="text",
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    # Add all new data types to this list
    new_data_types = [
        fibers_table,
        photodetectors_table,
        excitationsources_table,
        fluorophores_table,
        fiberphotometryresponse_series,
        deconvolved_fiberphotometryresponse_series_series,
        commandedvoltage_series,
        multi_commanded_voltage,
        fiber_photometry,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
