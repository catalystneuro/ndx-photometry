import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion, VectorData, VectorIndex
from pynwb.ophys import RoiResponseSeries
from pynwb.testing import TestCase, remove_test_file

from ndx_photometry import (
    FibersTable,
    PhotodetectorsTable,
    ExcitationSourcesTable,
    DeconvolvedRoiResponseSeries,
    MultiCommandedVoltage,
    FiberPhotometry,
    FluorophoresTable
)


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )

    return nwbfile


class TestFibersTable(TestCase):
    def setUp(self):
        """Set up an NWB file. Necessary because TetrodeSeries requires references to electrodes."""

        self.nwbfile = set_up_nwbfile()

    def test_constructor(self):
        multi_commanded_voltage = MultiCommandedVoltage(
            name="MyMultiCommandedVoltage",
        )

        cmmandedvoltage_series = (
            multi_commanded_voltage.create_commanded_voltage_series(
                name="commanded_voltage",
                data=[1, 2, 3],
                frequency=30.0,
                power=500.0,
                rate=30.0,
            )
        )

        cmmandedvoltage_series2 = (
            multi_commanded_voltage.create_commanded_voltage_series(
                name="commanded_voltage2",
                data=[1, 2, 3],
                frequency=30.0,
                power=500.0,
                rate=30.0,
            )
        )

        excitationsources_table = ExcitationSourcesTable(
            description="excitation sources table"
        )
        excitationsources_table.add_row(
            peak_wavelength=700.0,
            source_type="laser",
            commanded_voltage=cmmandedvoltage_series,
        )
        photodetectors_table = PhotodetectorsTable(
            description="photodetectors table"
        )
        photodetectors_table.add_row(peak_wavelength=500.0, type="PMT", gain=100.0)

        fluorophores_table = FluorophoresTable(
            description='fluorophores'
        )
        fluorophores_table.add_row(label='dlight',location='VTA',coordinates=(3.0,2.0,1.0))

        fiberstable = FibersTable(description="fibers table")
        fiberstable.add_row(
            location="brain",
            excitation_source=DynamicTableRegion(
                name="excitation_source",
                data=[0],
                description="region of excitation source table",
                table=excitationsources_table,
            ),
            photodetector=DynamicTableRegion(
                name="photodetector",
                data=[0],
                description="region of photodetector table",
                table=photodetectors_table,
            ),
            notes="fibers in a brain",
        )

        ophys_module = self.nwbfile.create_processing_module(
            name="ophys", description="fiber photometry"
        )
        ophys_module.add(multi_commanded_voltage)
        ophys_module.add(excitationsources_table)
        ophys_module.add(photodetectors_table)
        ophys_module.add(fiberstable)


class TestTetrodeSeriesRoundtrip(TestCase):
    """Simple roundtrip test for TetrodeSeries."""

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    #def tearDown(self):
    #    remove_test_file(self.path)

    def test_roundtrip(self):
        multi_commanded_voltage = MultiCommandedVoltage(
            name="MyMultiCommandedVoltage",
        )

        cmmandedvoltage_series = (
            multi_commanded_voltage.create_commanded_voltage_series(
                name="commanded_voltage",
                data=[1, 2, 3],
                frequency=30.0,
                power=500.0,
                rate=30.0,
            )
        )

        cmmandedvoltage_series2 = (
            multi_commanded_voltage.create_commanded_voltage_series(
                name="commanded_voltage2",
                data=[1, 2, 3],
                frequency=30.0,
                power=500.0,
                rate=30.0,
            )
        )

        excitationsources_table = ExcitationSourcesTable(
            description="excitation sources table"
        )

        excitationsources_table.add_row(
            peak_wavelength=700.0,
            source_type="laser",
            commanded_voltage=cmmandedvoltage_series,
        )
        photodetectors_table = PhotodetectorsTable(
            description="photodetectors table"
        )
        photodetectors_table.add_row(peak_wavelength=500.0, type="PMT", gain=100.0)



        fluorophores_table = FluorophoresTable(
            description='fluorophores'
        )
        fluorophores_table.add_row(label='dlight',location='VTA',coordinates=(3.0,2.0,1.0))

        fluorophores_column = DynamicTableRegion(
            name="fluorophores",
            data=[0],
            description="fluorophores recorded",
            table=fluorophores_table,
        )

        fiberstable = FibersTable(
            description="fibers table",
            columns=[
                DynamicTableRegion(
                    name="excitation_source",
                    data=[0],
                    description="region of excitation source table",
                    table=excitationsources_table,
                ),
                DynamicTableRegion(
                    name="photodetector",
                    data=[0],
                    description="region of photodetector table",
                    table=photodetectors_table,
                ),
                fluorophores_column,
                VectorIndex(
                    name='fluorophores_index',
                    target=fluorophores_column,
                    data=[1],
                ),
                VectorData(
                    name="location",
                    description="location of fiber",
                    data=["my location"],
                ),
                VectorData(name="notes", description="notes", data=["my notes"]),
            ],
            colnames=["excitation_source", "photodetector", "fluorophores", "location", "notes"],
        )

        fibers_ref = DynamicTableRegion(
            name="rois", data=[0], description="source fibers", table=fiberstable
        )

        roi_response_series = RoiResponseSeries(
            name="roi_response_series",
            description="my roi response series",
            data=np.random.randn(100, 1),
            rate=30.0,
            rois=fibers_ref,
        )

        deconv_roi_response_series = DeconvolvedRoiResponseSeries(
            name="DeconvolvedRoiResponseSeries",
            description="my roi response series",
            data=np.random.randn(100, 1),
            rate=30.0,
            rois=fibers_ref,
            raw=roi_response_series,
        )

        ophys_module = self.nwbfile.create_processing_module(
            name="ophys", description="fiber photometry"
        )

        self.nwbfile.add_lab_meta_data(
            FiberPhotometry(
                fibers=fiberstable,
                excitation_sources=excitationsources_table,
                photodetectors=photodetectors_table,
                fluorophores=fluorophores_table
            )
        )

        ophys_module.add(multi_commanded_voltage)
        self.nwbfile.add_acquisition(roi_response_series)
        ophys_module.add(deconv_roi_response_series)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(ophys_module, read_nwbfile.processing["ophys"])
