import datetime
import numpy as np

from pynwb import NWBHDF5IO, NWBFile
from pynwb.core import DynamicTableRegion
from pynwb.ophys import RoiResponseSeries
from pynwb.testing import TestCase, remove_test_file

from ndx_photometry import (
    FibersTable,
    PhotodetectorsTable,
    ExcitationSourcesTable,
    FiberPhotometryResponseSeries,
    DeconvolvedFiberPhotometryResponseSeries,
    MultiCommandedVoltage,
    FiberPhotometry,
    FluorophoresTable,
)


def set_up_nwbfile():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    return nwbfile


class TestIntegrationRoundtrip(TestCase):
    """
    Full Roundtrip Integration Test
    Creates, writes, and reads instances of:
        FibersTable,
        PhotodetectorsTable,
        ExcitationSourcesTable,
        DeconvolvedFiberPhotometryResponseSeries,
        MultiCommandedVoltage,
        FiberPhotometry,
        FluorophoresTable
    """

    def setUp(self):
        self.nwbfile = set_up_nwbfile()
        self.path = "test.nwb"

    def tearDown(self):
        remove_test_file(self.path)

    def test_roundtrip(self):
        multi_commanded_voltage = MultiCommandedVoltage()

        commandedvoltage_series = multi_commanded_voltage.create_commanded_voltage_series(
            name="commanded_voltage", data=[1.0, 2.0, 3.0], frequency=30.0, power=500.0, rate=30.0, unit="volts"
        )

        _ = multi_commanded_voltage.create_commanded_voltage_series(
            name="commanded_voltage2",
            data=[4.0, 5.0, 6.0],
            power=400.0,
            rate=30.0,
            unit="volts",
        )

        excitationsources_table = ExcitationSourcesTable(description="excitation sources table")

        excitationsources_table.add_row(
            peak_wavelength=700.0,
            source_type="laser",
            commanded_voltage=commandedvoltage_series,
        )

        photodetectors_table = PhotodetectorsTable(description="photodetectors table")
        photodetectors_table.add_row(peak_wavelength=500.0, type="PMT", gain=100.0)

        fluorophores_table = FluorophoresTable(description="fluorophores")
        fluorophores_table.add_row(
            label="dlight",
            location="VTA",
            coordinates=(3.0, 2.0, 1.0),
            excitation_peak_wavelength=470.0,
            emission_peak_wavelength=516.0,
        )

        fibers_table = FibersTable(description="fibers table")

        fibers_table.add_row(
            location="my location",
        )

        self.nwbfile.add_lab_meta_data(
            FiberPhotometry(
                fibers=fibers_table,
                excitation_sources=excitationsources_table,
                photodetectors=photodetectors_table,
                fluorophores=fluorophores_table,
                commanded_voltages=multi_commanded_voltage,
            )
        )

        fiber_ref = fibers_table.create_fiber_region(region=[0], description="source fiber")
        excitation_ref = excitationsources_table.create_excitation_source_region(
            region=[0], description="excitation sources"
        )
        photodetector_ref = photodetectors_table.create_photodetector_region(region=[0], description="photodetector")
        fluorophore_ref = fluorophores_table.create_fluorophore_region(region=[0], description="fluorophore")

        fp_response_series = FiberPhotometryResponseSeries(
            name="MyFPRecording",
            data=np.random.randn(100, 1),
            unit="F",
            rate=30.0,
            fibers=fiber_ref,
            excitation_sources=excitation_ref,
            photodetectors=photodetector_ref,
            fluorophores=fluorophore_ref,
        )

        self.nwbfile.add_acquisition(fp_response_series)

        deconv_roi_response_series = DeconvolvedFiberPhotometryResponseSeries(
            name="DeconvolvedFiberPhotometryResponseSeries",
            description="my roi response series",
            data=np.random.randn(100, 1),
            unit="F",
            rate=30.0,
            raw=fp_response_series,
        )

        ophys_module = self.nwbfile.create_processing_module(name="ophys", description="fiber photometry")
        ophys_module.add(deconv_roi_response_series)

        with NWBHDF5IO(self.path, mode="w") as io:
            io.write(self.nwbfile)

        with NWBHDF5IO(self.path, mode="r", load_namespaces=True) as io:
            read_nwbfile = io.read()
            self.assertContainerEqual(ophys_module, read_nwbfile.processing["ophys"])
            self.assertContainerEqual(
                self.nwbfile.lab_meta_data["fiber_photometry"], read_nwbfile.lab_meta_data["fiber_photometry"]
            )
            self.assertContainerEqual(fp_response_series, read_nwbfile.acquisition["MyFPRecording"])
            self.assertContainerEqual(
                deconv_roi_response_series, read_nwbfile.processing["ophys"]["DeconvolvedFiberPhotometryResponseSeries"]
            )
