import pytest
import datetime
from pynwb import NWBFile
from ndx_photometry import (
    FibersTable,
    PhotodetectorsTable,
    ExcitationSourcesTable,
    FiberPhotometry,
    FluorophoresTable,
)

@pytest.fixture()
def fibers_table():
    nwbfile = NWBFile(
        session_description="session_description",
        identifier="identifier",
        session_start_time=datetime.datetime.now(datetime.timezone.utc),
    )
    excitation_sources_table = ExcitationSourcesTable(description="description")
    photodetectors_table = PhotodetectorsTable(description="description")
    fluorophores_table = FluorophoresTable(description="description")
    fibers_table = FibersTable(description="description")
    nwbfile.add_lab_meta_data(
        FiberPhotometry(
            fibers=fibers_table,
            excitation_sources=excitation_sources_table,
            photodetectors=photodetectors_table,
            fluorophores=fluorophores_table,
        )
    )
    return fibers_table

def test_with_notes(fibers_table):
    fibers_table.add_fiber(
        excitation_source=0,
        photodetector=0,
        fluorophores=[0],
        location="location",
        notes="notes",
    )
    assert fibers_table["notes"][0] == "notes"

def test_without_notes(fibers_table):
    fibers_table.add_fiber(
        excitation_source=0,
        photodetector=0,
        fluorophores=[0],
        location="location",
    )
    with pytest.raises(KeyError):
        fibers_table["notes"][0]

if __name__ == '__main__':
    test_with_notes(fibers_table)
    test_without_notes(fibers_table)
