from hdmf.utils import docval, popargs
from pynwb import get_class

FibersTable = get_class('FibersTable', 'ndx-photometry')
FluorophoresTable = get_class('FluorophoresTable', 'ndx-photometry')
PhotodetectorsTable = get_class('PhotodetectorsTable', 'ndx-photometry')
ExcitationSourcesTable = get_class('ExcitationSourcesTable', 'ndx-photometry')
FiberPhotometryResponseSeries = get_class('FiberPhotometryResponseSeries', 'ndx-photometry')

@docval(
    {'name': 'region', 'type': list, 'doc': 'the indices of the fibers table'},
    {'name': 'description', 'type': str, 'doc': 'a brief description of what these fibers are'},
)
def create_fiber_region(self, **kwargs):
    region, description = popargs('region', 'description', kwargs)
    return super(FibersTable, self).create_region(name='fibers', region=region, description=description)

@docval(
    {'name': 'region', 'type': list, 'doc': 'the indices of the fluorophores table'},
    {'name': 'description', 'type': str, 'doc': 'a brief description of what these fluorophores are'},
)
def create_fluorophore_region(self, **kwargs):
    region, description = popargs('region', 'description', kwargs)
    return super(FluorophoresTable, self).create_region(name='fluorophores', region=region, description=description)

@docval(
    {'name': 'region', 'type': list, 'doc': 'the indices of the photodetectors table'},
    {'name': 'description', 'type': str, 'doc': 'a brief description of what these photodetectors are'},
)
def create_photodetector_region(self, **kwargs):
    region, description = popargs('region', 'description', kwargs)
    return super(PhotodetectorsTable, self).create_region(name='photodetectors', region=region, description=description)

@docval(
    {'name': 'region', 'type': list, 'doc': 'the indices of the excitation sources table'},
    {'name': 'description', 'type': str, 'doc': 'a brief description of what these excitation sources are'},
)
def create_excitation_source_region(self, **kwargs):
    region, description = popargs('region', 'description', kwargs)
    return super(ExcitationSourcesTable, self).create_region(name='excitation_sources', region=region, description=description)


FibersTable.create_fiber_region = create_fiber_region
FluorophoresTable.create_fluorophore_region = create_fluorophore_region
PhotodetectorsTable.create_photodetector_region = create_photodetector_region
ExcitationSourcesTable.create_excitation_source_region = create_excitation_source_region