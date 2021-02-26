import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion, VectorData
from pynwb.ophys import RoiResponseSeries
from pynwb.device import Device
from pynwb.testing import TestCase, remove_test_file, AcquisitionH5IOMixin

from ndx_photometry import (
    FibersTable,
    PhotodetectorsTable,
    ExcitationSourcesTable,
    DeconvolvedRoiResponseSeries,
    MultiCommandedVoltage
)


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description='session_description',
        identifier='identifier',
        session_start_time=datetime.datetime.now(datetime.timezone.utc)
    )

    return nwbfile #, device


class TestFibersTable(TestCase):

    def setUp(self):
        """Set up an NWB file. Necessary because TetrodeSeries requires references to electrodes."""

        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        self.multi_commanded_voltage = MultiCommandedVoltage(
            name='MyMultiCommandedVoltage',
        )

        self.commandedvoltage_series = self.multi_commanded_voltage.create_commanded_voltage_series(
            name='commanded_voltage',
            data=[1, 2, 3],
            frequency=30.0,
            power=500.0,
            rate=30.0
        )

        self.commandedvoltage_series2 = self.multi_commanded_voltage.create_commanded_voltage_series(
            name='commanded_voltage2',
            data=[1, 2, 3],
            frequency=30.0,
            power=500.0,
            rate=30.0
        )

        self.excitationsources_table = ExcitationSourcesTable(
            name='excitation_sources', description='excitation sources table')
        self.excitationsources_table.add_row(
            peak_wavelength=700.0,
            source_type='laser',
            commanded_voltage=self.commandedvoltage_series
        )
        self.photodetectors_table = PhotodetectorsTable(
            name='photodetectors_table', description='photodetectors table')
        self.photodetectors_table.add_row(peak_wavelength=500.0, type='PMT', gain=100.0)
        self.fiberstable = FibersTable(name='fibers_table', description='fibers table')
        self.fiberstable.add_row(
            location='brain',
            excitation_source=DynamicTableRegion(
                name="excitation_source",
                data=[0],
                description="region of excitation source table",
                table=self.excitationsources_table
            ),
            photodetector=DynamicTableRegion(
                name="photodetector",
                data=[0],
                description="region of photodetector table",
                table=self.photodetectors_table
            ),
            notes='fibers in a brain'
        )

        ophys_module = self.nwbfile.create_processing_module(
            name='ophys', description='fiber photometry')
        ophys_module.add(self.multi_commanded_voltage)
        ophys_module.add(self.excitationsources_table)
        ophys_module.add(self.photodetectors_table)
        ophys_module.add(self.fiberstable)

        # self.assertEqual(fibertable.name, 'name')
        # self.assertEqual(tetrode_series.description, 'description')
        # np.testing.assert_array_equal(tetrode_series.data, data)
        # self.assertEqual(tetrode_series.rate, 1000.)
        # self.assertEqual(tetrode_series.starting_time, 0)
        # self.assertEqual(tetrode_series.electrodes, all_electrodes)
        # self.assertEqual(tetrode_series.trode_id, 1)


class TestTetrodeSeriesRoundtrip(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = 'test.nwb'

    #def tearDown(self):
    #    remove_test_file(self.path)

    def test_roundtrip(self):
        self.multi_commanded_voltage = MultiCommandedVoltage(
            name='MyMultiCommandedVoltage',
        )

        self.commandedvoltage_series = self.multi_commanded_voltage.create_commanded_voltage_series(
            name='commanded_voltage',
            data=[1, 2, 3],
            frequency=30.0,
            power=500.0,
            rate=30.0
        )

        self.commandedvoltage_series2 = self.multi_commanded_voltage.create_commanded_voltage_series(
            name='commanded_voltage2',
            data=[1, 2, 3],
            frequency=30.0,
            power=500.0,
            rate=30.0
        )

        self.excitationsources_table = ExcitationSourcesTable(
            name='excitation_sources', description='excitation sources table')

        self.excitationsources_table.add_row(
            peak_wavelength=700.0,
            source_type='laser',
            commanded_voltage=self.commandedvoltage_series
        )
        self.photodetectors_table = PhotodetectorsTable(
            name='photodetectors_table', description='photodetectors table')
        self.photodetectors_table.add_row(
            peak_wavelength=500.0, type='PMT', gain=100.0)

        self.fiberstable = FibersTable(
            name='fibers_table',
            description='fibers table',
            columns=[
                DynamicTableRegion(
                    name="excitation_source",
                    data=[0],
                    description="region of excitation source table",
                    table=self.excitationsources_table),
                DynamicTableRegion(
                    name="photodetector",
                    data=[0],
                    description="region of photodetector table",
                    table=self.photodetectors_table
                ),
                VectorData(
                    name='location',
                    description='location of fiber',
                    data=['my location']
                ),
                VectorData(
                    name='notes',
                    description='notes',
                    data=['my notes']
                )
            ],
            colnames=["excitation_source", "photodetector", 'location',
                      'notes']
        )

        fibers_ref = DynamicTableRegion(
            name='rois',
            data=[0],
            description='source fibers',
            table=self.fiberstable
        )

        roi_response_series = RoiResponseSeries(
            name='roi_response_series',
            description='my roi response series',
            data=np.random.randn(100, 1),
            rate=30.,
            rois=fibers_ref
        )

        deconv_roi_response_series = DeconvolvedRoiResponseSeries(
            name='DeconvolvedRoiResponseSeries',
            description='my roi response series',
            data=np.random.randn(100, 1),
            rate=30.,
            rois=fibers_ref,
            roi_response_series=roi_response_series
        )

        self.ophys_module = self.nwbfile.create_processing_module(
            name='ophys', description='fiber photometry')

        self.ophys_module.add(self.multi_commanded_voltage)
        self.ophys_module.add(self.excitationsources_table)
        self.ophys_module.add(self.photodetectors_table)
        self.ophys_module.add(self.fiberstable)
        self.ophys_module.add(roi_response_series)
        self.ophys_module.add(deconv_roi_response_series)

        with NWBHDF5IO(self.path, mode='w') as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode='r', load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(self.ophys_module, read_nwbfile.processing['ophys'])
#
#
# class TestTetrodeSeriesRoundtripPyNWB(AcquisitionH5IOMixin, TestCase):
#     """Complex, more complete roundtrip test for TetrodeSeries using pynwb.testing infrastructure."""
#
#     def setUpContainer(self):
#         """ Return the test TetrodeSeries to read/write """
#         self.device = Device(
#             name='device_name'
#         )
#
#         self.group = ElectrodeGroup(
#             name='electrode_group',
#             description='description',
#             location='location',
#             device=self.device
#         )
#
#         self.table = get_electrode_table()  # manually create a table of electrodes
#         for i in range(10):
#             self.table.add_row(
#                 x=i,
#                 y=i,
#                 z=i,
#                 imp=np.nan,
#                 location='location',
#                 filtering='filtering',
#                 group=self.group,
#                 group_name='electrode_group'
#             )
#
#         all_electrodes = DynamicTableRegion(
#             data=list(range(0, 10)),
#             description='all the electrodes',
#             name='electrodes',
#             table=self.table
#         )
#
#         data = np.random.rand(100, 3)
#         tetrode_series = TetrodeSeries(
#             name='name',
#             description='description',
#             data=data,
#             rate=1000.,
#             electrodes=all_electrodes,
#             trode_id=1
#         )
#         return tetrode_series
#
#     def addContainer(self, nwbfile):
#         """Add the test TetrodeSeries and related objects to the given NWBFile."""
#         nwbfile.add_device(self.device)
#         nwbfile.add_electrode_group(self.group)
#         nwbfile.set_electrode_table(self.table)
#         nwbfile.add_acquisition(self.container)
