import warnings

from hdmf.utils import docval
from hdmf.common import DynamicTable


class FibersTable(DynamicTable):

    @docval({'name': 'excitation_source',
             'type': 'int',
             'doc': 'references rows of ExcitationSourcesTable',
             'default': None,
             'shape': (None,)},
            {'name': 'photodetector',
             'type': 'int',
             'doc': 'references rows of PhotodetectorsTable',
             'default': None,
             'shape': (None,)},
            {'name': 'fluorophores',
             'doc': 'references rows of FluorophoresTable',
             'type': 'array_data',
             'default': None,
             'shape':(None,)},
            {'name': 'fluorophores_index',
             'doc': 'indexes fluorophores of FluorophoresTable',
             'type': 'array_data',
             'default': None,
             'shape': (None,)},
            {'name': 'location',
             'type': 'text',
             'doc': 'location of fiber',
             'default': None,
             'shape':(None,)},
            {'name': 'notes',
             'type': 'text',
             'doc': 'description of fiber',
             'default': None,
             'shape':(None,)},
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
    def add_row(self, **kwargs):
        """
        Add a row to this table
        """
        referenced_tables = kwargs.keys()
        for table in referenced_tables:
            if table in self:
                col = self[table].target
                if col.table is None:
                    if col not in dict(self):
                        nwbfile = self.get_ancestor(data_type='NWBFile')
                        col.table = dict(nwbfile)[table]
                        if col.table is None:
                            warnings.warn(f'Reference to {table} that does not yet exist')
                    else:
                        col.table = dict(self)[table]
        super(FibersTable, self).add_row(**kwargs)