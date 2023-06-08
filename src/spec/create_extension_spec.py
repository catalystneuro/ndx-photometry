# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import (
    NWBNamespaceBuilder,
    export_spec,
    NWBGroupSpec,
    NWBAttributeSpec,
    NWBDatasetSpec,
    NWBRefSpec,
    NWBLinkSpec
)

# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""extension for fiber photometry data""",
        name="""ndx-photometry""",
        version="""0.1.0""",
        author=list(map(str.strip, """Akshay Jaggi""".split(","))),
        contact=list(map(str.strip, """akshay.x.jaggi@gmail.com""".split(","))),
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.

    ns_builder.include_type("TimeSeries", namespace="core")
    ns_builder.include_type("NWBDataInterface", namespace="core")
    ns_builder.include_type("NWBContainer", namespace="core")
    ns_builder.include_type("RoiResponseSeries", namespace="core")
    ns_builder.include_type("LabMetaData", namespace="core")
    ns_builder.include_type("DynamicTable", namespace="hdmf-common")
    ns_builder.include_type("DynamicTableRegion", namespace="hdmf-common")
    ns_builder.include_type("VectorData", namespace="hdmf-common")
    ns_builder.include_type("VectorIndex", namespace="hdmf-common")
    ns_builder.include_type("Data", namespace="hdmf-common")
    ns_builder.include_type("ElementIdentifiers", namespace="hdmf-common")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    fibers_table = NWBGroupSpec(
        neurodata_type_def="FibersTable",
        neurodata_type_inc="DynamicTable",
        name='fibers',
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
                name="excitation_source",
                doc="references rows of ExcitationSourcesTable",
                dtype="int",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            NWBDatasetSpec(
                name="photodetector",
                doc="references rows of PhotodetectorsTable",
                dtype="int",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            NWBDatasetSpec(
                name="fluorophores",
                doc="references rows of FluorophoresTable",
                shape=(None,),
                neurodata_type_inc="DynamicTableRegion",
            ),
            # NWBDatasetSpec(
            #     name="fluorophores_index",
            #     doc="indexes fluorophores of FluorophoresTable",
            #     shape=(None,),
            #     neurodata_type_inc="VectorIndex",
            # ),
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
        name='photodetectors',
        doc="Extends DynamicTable to hold various Photodetectors",
        datasets=[
            NWBDatasetSpec(
                name="peak_wavelength",
                doc="peak wavelength of photodetector",
                dtype="float",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
                attributes=[
                    NWBAttributeSpec(
                        name="unit", doc="wavelength unit", value="nanometers", dtype="text"
                    )
                ],
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
                attributes=[
                    NWBAttributeSpec(
                        name="unit", doc="wavelength unit", value="nanometers", dtype="text"
                    )
                ],
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
                dtype=NWBRefSpec(
                    target_type="CommandedVoltageSeries", reftype="object"
                ),
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
                attributes=[
                    NWBAttributeSpec(
                        name="unit", doc="data unit", value="volts", dtype="text"
                    )
                ],
            ),
            NWBDatasetSpec(
                name="frequency",
                doc="voltage frequency in unit hertz",
                dtype="float",
                attributes=[
                    NWBAttributeSpec(
                        name="unit", doc="frequency unit", value="hertz", dtype="text"
                    )
                ],
                quantity="?",
            ),
            NWBDatasetSpec(
                name="power",
                doc="voltage power in unit volts",
                dtype="float",
                attributes=[
                    NWBAttributeSpec(
                        name="unit", doc="power unit", value="volts", dtype="text"
                    )
                ],
            ),
        ],
    )

    multi_commanded_voltage = NWBGroupSpec(
        name='commanded_voltages',
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

    deconvolvedroiresponse_series = NWBGroupSpec(
        neurodata_type_def="DeconvolvedRoiResponseSeries",
        neurodata_type_inc="RoiResponseSeries",
        doc="Extends RoiResponseSeries to hold deconvolved data",
        links=[
            NWBLinkSpec(
                name="raw",
                target_type="RoiResponseSeries",
                doc="ref to roi response series",
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

    fluorophores_table = NWBGroupSpec(
        neurodata_type_def="FluorophoresTable",
        neurodata_type_inc="DynamicTable",
        name='fluorophores',
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
                doc='injection brain region name',
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
            NWBDatasetSpec(
                name="coordinates",
                doc="injection taxonomical coordinates in (AP, ML, Z) in mm relative to Bregma",
                dtype="float",
                shape=(None,3),
                neurodata_type_inc="VectorData",
                quantity="?",
            ),
        ],
    )

    fiber_photometry = NWBGroupSpec(
        neurodata_type_def='FiberPhotometry',
        neurodata_type_inc='LabMetaData',
        name='fiber_photometry',
        doc='all Fiber Photometry metadata',
        groups=[
            NWBGroupSpec(
                name='fibers',
                neurodata_type_inc='FibersTable',
                doc='table of fibers used'
            ),
            NWBGroupSpec(
                name='excitation_sources',
                neurodata_type_inc='ExcitationSourcesTable',
                doc='table of excitation sources used'
            ),
            NWBGroupSpec(
                name='photodetectors',
                neurodata_type_inc='PhotodetectorsTable',
                doc='table of photodetectors used'
            ),
            NWBGroupSpec(
                name='fluorophores',
                neurodata_type_inc='FluorophoresTable',
                doc='table of fluorophores used'
            ),
            NWBGroupSpec(
                name='commanded_voltages',
                neurodata_type_inc='MultiCommandedVoltage',
                doc='multiple commanded voltage container',
                quantity="?",
            )
        ]
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        fibers_table,
        photodetectors_table,
        excitationsources_table,
        commandedvoltage_series,
        deconvolvedroiresponse_series,
        multi_commanded_voltage,
        fiber_photometry,
        fluorophores_table
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "spec")
    )
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
