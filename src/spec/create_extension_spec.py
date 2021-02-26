# -*- coding: utf-8 -*-

import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec, NWBDatasetSpec, NWBRefSpec
# TODO: import the following spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""extension for fiber photometry data""",
        name="""ndx-photometry""",
        version="""0.1.0""",
        author=list(map(str.strip, """Akshay Jaggi""".split(','))),
        contact=list(map(str.strip, """akshay.x.jaggi@gmail.com""".split(',')))
    )

    # TODO: specify the neurodata_types that are used by the extension as well
    # as in which namespace they are found
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types
    # as of HDMF 1.6.1, the full ancestry of the neurodata_types that are used by
    # the extension should be included, i.e., the neurodata_type and its parent
    # type and its parent type and so on. this will be addressed in a future
    # release of HDMF.

    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('NWBDataInterface', namespace='core')
    ns_builder.include_type('NWBContainer', namespace='core')
    ns_builder.include_type('RoiResponseSeries', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='hdmf-common')
    ns_builder.include_type('DynamicTableRegion', namespace='hdmf-common')
    ns_builder.include_type('VectorData', namespace='hdmf-common')
    ns_builder.include_type('Data', namespace='hdmf-common')
    ns_builder.include_type('ElementIdentifiers', namespace='hdmf-common')

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    fibers_table = NWBGroupSpec(
        neurodata_type_def='FibersTable',
        neurodata_type_inc='DynamicTable',
        doc='Extends DynamicTable to hold various Fibers',
        datasets=[
            NWBDatasetSpec(
                name='location',
                doc='location of fiber',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData'
            ),
            NWBDatasetSpec(
                name='excitation_source',
                doc='references rows of ExcitationSourcesTable',
                dtype='int',
                shape=(None,),
                neurodata_type_inc='DynamicTableRegion'
            ),
            NWBDatasetSpec(
                name='photodetector',
                doc='references rows of PhotodetectorsTable',
                dtype='int',
                shape=(None,),
                neurodata_type_inc='DynamicTableRegion'
            ),
            NWBDatasetSpec(
                name='notes',
                doc='description of fiber',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData'
            ),
            NWBDatasetSpec(
                name='fiber_model_number',
                doc='doc',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',
                quantity='?'
            ),
            NWBDatasetSpec(
                name='dichroic_model_number',
                doc='doc',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',
                quantity='?'
            )
        ],
    )

    photodetectors_table = NWBGroupSpec(
        neurodata_type_def='PhotodetectorsTable',
        neurodata_type_inc='DynamicTable',
        doc='Extends DynamicTable to hold various Photodetectors',
        datasets=[
            NWBDatasetSpec(
                name='peak_wavelength',
                doc='peak wavelength of photodetector',
                dtype='float',
                shape=(None,),
                neurodata_type_inc='VectorData',
                attributes=[NWBAttributeSpec(name='unit', doc='',value='nanometers', dtype='text')]
            ),
            NWBDatasetSpec(
                name='type',
                doc='"PMT" or "photodiode"',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',
            ),
            NWBDatasetSpec(
                name='gain',
                doc='doc',
                dtype='float',
                shape=(None,),
                neurodata_type_inc='VectorData',
            ),
            NWBDatasetSpec(
                name='model_number',
                doc='model number of the photodector',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',
                quantity='?'
            )
        ],
    )

    excitationsources_table = NWBGroupSpec(
        neurodata_type_def='ExcitationSourcesTable',
        neurodata_type_inc='DynamicTable',
        doc='Extends DynamicTable to hold various Photodetectors',
        datasets=[
            NWBDatasetSpec(
                name='peak_wavelength',
                doc='peak wavelength of photodetector',
                dtype='float',
                shape=(None,),
                neurodata_type_inc='VectorData',
                attributes=[NWBAttributeSpec(name='unit',doc='',value='nanometers',dtype='text')]
            ),
            NWBDatasetSpec(
                name='source_type',
                doc='"LED" or "laser"',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',

            ),
            NWBDatasetSpec(
                name='commanded_voltage',
                doc='references CommandedVoltageSeries',
                dtype=NWBRefSpec(target_type='CommandedVoltageSeries', reftype='object'),
                shape=(None,),
                neurodata_type_inc='VectorData',
            ),
            NWBDatasetSpec(
                name='output',
                doc='references TimeSeries',
                dtype='float', #TODO: why not int or NWBRefSpec since this is a reference?
                shape=(None,),
                neurodata_type_inc='VectorData',
                quantity='?'
            ),
            NWBDatasetSpec(
                name='model_number',
                doc='doc',
                dtype='text',
                shape=(None,),
                neurodata_type_inc='VectorData',
                quantity='?'
            )
        ],
    )

    commandedvoltage_series = NWBGroupSpec(
        neurodata_type_def='CommandedVoltageSeries',
        neurodata_type_inc='TimeSeries',
        doc='Extends TimeSeries to hold a Commanded Voltage',
        datasets=[
            NWBDatasetSpec(
                name='data',
                doc='voltage length ntime in volts',
                dtype='float',
                shape=(None,),
                attributes=[NWBAttributeSpec(name='unit', doc='doc', value='volts', dtype='text')]
            ),
            NWBDatasetSpec(
                name='frequency',
                doc='voltage frequency in unit hertz',
                dtype='float',
                attributes=[NWBAttributeSpec(name='unit', doc='doc' ,value='hertz', dtype='text')]
            ),
            NWBDatasetSpec(
                name='power',
                doc='voltage power in unit volts',
                dtype='float',
                attributes=[NWBAttributeSpec(name='unit', doc='doc', value='volts', dtype='text')]
            ),
        ],
    )

    multi_commanded_voltage = NWBGroupSpec(
        neurodata_type_def='MultiCommandedVoltage',
        neurodata_type_inc='NWBDataInterface',
        doc='holds CommandedVoltageSeries objects',
        groups=[
            NWBGroupSpec(
                neurodata_type_inc='CommandedVoltageSeries',
                quantity='*',
                doc='commanded voltage series'
            )
        ]
    )

    deconvolvedroiresponse_series = NWBGroupSpec(
        neurodata_type_def='DeconvolvedRoiResponseSeries',
        neurodata_type_inc='RoiResponseSeries',
        doc='Extends RoiResponseSeries to hold deconvolved data',
        groups=[
            NWBGroupSpec(
                name='roi_response_series',
                neurodata_type_inc='RoiResponseSeries',
                doc='ref to roi response series'
            )
        ],
        datasets=[
            NWBDatasetSpec(
                name='deconvolution_filter',
                doc='description of deconvolution filter used',
                dtype='text',
                neurodata_type_inc='VectorData',
                quantity='?'
            ),
            NWBDatasetSpec(
                name='downsampling_filter',
                doc='description of downsampling filter used',
                dtype='text',
                neurodata_type_inc='VectorData',
                quantity='?'
            ),
        ],
    )

    # TODO: add all of your new data types to this list
    new_data_types = [
        fibers_table,
        photodetectors_table,
        excitationsources_table,
        commandedvoltage_series,
        deconvolvedroiresponse_series,
        multi_commanded_voltage
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
