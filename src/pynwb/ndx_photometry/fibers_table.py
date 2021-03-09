import os
import warnings

from pynwb import register_class, get_class

from hdmf.utils import docval, getargs
from pynwb.core import DynamicTable, VectorIndex


@docval({'name': 'excitation_source',
         'type': int,
         'doc': 'references rows of ExcitationSourcesTable',
         'default': None},
        {'name': 'photodetector',
         'type': int,
         'doc': 'references rows of PhotodetectorsTable',
         'default': None},
        {'name': 'fluorophores',
         'doc': 'references rows of FluorophoresTable',
         'type': 'array_data',
         'default': None,
         'shape':(None,)},
        {'name': 'location',
         'type': str,
         'doc': 'location of fiber',
         'default': None},
        {'name': 'notes',
         'type': str,
         'doc': 'description of fiber',
         'default': None},
        # {'name': 'fiber_model_number',
        #  'type': 'text',
        #  'doc': 'fiber model number',
        #  'default': None,
        #  'shape': (None,),
        #  'quantity':'?'},
        # {'name': 'dichroic_model_number',
        #  'type': 'text',
        #  'doc': 'the spike waveform mean for each unit. Shape is (time,) or (time, electrodes)',
        #  'default': None,
        #  'shape': (None,),
        #  'quantity':'?'},
        allow_extra=True)
def add_fiber(self, **kwargs):
    """
    Add a row to this table
    """
    super(FibersTable, self).add_row(**kwargs)
    referenced_tables = ('excitation_sources','photodetectors','fluorophores')
    for arg, table in zip(kwargs, referenced_tables):
        col = self[arg].target if isinstance(self[arg],VectorIndex) else self[arg]
        if col.table is None:
            nwbfile = self.get_ancestor(data_type='NWBFile')
            col.table = getattr(nwbfile.lab_meta_data['fiber_photometry'],table)
            if col.table is None:
                warnings.warn(f'Reference to {table} that does not yet exist')

FibersTable = get_class('FibersTable','ndx-photometry')
FibersTable.add_fiber = add_fiber
