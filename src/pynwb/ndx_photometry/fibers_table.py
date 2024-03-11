import warnings

from pynwb import register_class

from hdmf.utils import docval, popargs
from pynwb.core import VectorIndex, DynamicTable

@register_class('FibersTable', 'ndx-photometry')
class FibersTable(DynamicTable):
    __columns__ = (
        {'name': 'location', 'description': 'location of fiber'},
        {'name': 'excitation_source', 'description': 'references rows of ExcitationSourcesTable', 'table': True},
        {'name': 'photodetector', 'description': 'references rows of PhotodetectorsTable', 'table': True},
        {'name': 'fluorophores', 'description': 'references rows of FluorophoresTable', 'table': True},
        {'name': 'notes', 'description': 'description of fiber'},
        {'name': 'fiber_model_number', 'description': 'fiber model number'},
        {'name': 'dichroic_model_number', 'description': 'dichroic model number'}
    )

    @docval(
        {'name': 'name', 'type': str, 'doc': 'name of this FibersTable', 'default': 'fibers'},
        {'name': 'description', 'type': str, 'doc': 'description of this FibersTable'},
        {'name': 'target_tables', 'type': dict, 'doc': 'the excitation_source, fluorophores, and photodetectors tables that fibers references'},
    )
    def __init__(self, **kwargs):
        name, description, target_tables = popargs('name', 'description', 'target_tables', kwargs)
        super().__init__(name=name, description=description, target_tables=target_tables)

    @docval(
        {'name': 'excitation_source', 'type': int, 'doc': 'references rows of ExcitationSourcesTable'},
        {'name': 'photodetector', 'type': int, 'doc': 'references rows of PhotodetectorsTable'},
        {'name': 'fluorophores', 'doc': 'references rows of FluorophoresTable', 'type': 'array_data'},
        {'name': 'location', 'type': str, 'doc': 'location of fiber'},
        {'name': 'notes', 'type': str, 'doc': 'description of fiber', 'default': None},
        {'name': 'fiber_model_number', 'type': str, 'doc': 'fiber model number', 'default': None},
        {'name': 'dichroic_model_number', 'type': str, 'doc': 'dichroic model number', 'default': None},
        allow_extra=True
    )
    def add_row(self, **kwargs):
        super().add_row(**kwargs)


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
        {'name': 'fiber_model_number',
         'type': str,
         'doc': 'fiber model number',
         'default': None},
        {'name': 'dichroic_model_number',
         'type': str,
         'doc': 'dichroic model number',
         'default': None},
        allow_extra=True)
def add_fiber(self, **kwargs):
    """
    Add a row per fiber to the fibers table
    Checks to see if the tables are properly referenced
    If not, gets their references from the nwbfile

    This implementation is for legacy purposes and is not recommended for use.
    Please use the add_row method instead.
    """
    deprecation_message = """
        This method is being deprecated on or after October 2024 in favor of the add_row method.
        Please use the add_row method instead.
        """
    warnings.warn(deprecation_message, category=FutureWarning)
    super(FibersTable, self).add_row(**kwargs)
    referenced_tables = ('excitation_sources','photodetectors','fluorophores')
    for arg, table in zip(kwargs, referenced_tables):
        col = self[arg].target if isinstance(self[arg],VectorIndex) else self[arg]
        if col.table is None:
            nwbfile = self.get_ancestor(data_type='NWBFile')
            col.table = getattr(nwbfile.lab_meta_data['fiber_photometry'],table)
            if col.table is None:
                warnings.warn(f'Reference to {table} that does not yet exist')


FibersTable.add_fiber = add_fiber
