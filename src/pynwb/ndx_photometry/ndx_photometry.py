from pynwb import register_class, get_class
from pynwb.file import DynamicTable
from hdmf.utils import docval, call_docval_func, get_docval


# @register_class('FibersTable', 'ndx-photometry')
# class FibersTable(DynamicTable):
#     """
#     Table for storing bipolar scheme data
#     """
#
#     __columns__ = (
#         {'name': 'anodes', 'description': 'references the electrodes table', 'required': True,
#          'table': True},
#         {'name': 'cathodes', 'description': 'references the electrodes table', 'required': True,
#          'table': True}
#     )
#
#     @docval(dict(name='name', type=str, doc='name of this BipolarSchemeTable',
#                  default='BipolarSchemeTable'),  # required
#             dict(name='description', type=str, doc='Description of this DynamicTableRegion',
#                  default='references the electrodes table'),
#             *get_docval(DynamicTable.__init__, 'id', 'columns', 'colnames'))
#     def __init__(self, **kwargs):
#         call_docval_func(super(BipolarSchemeTable, self).__init__, kwargs)
#
#
# EcephysExt = get_class('EcephysExt', 'ndx-bipolar-scheme')

@register_class('ExcitationSourcesTable', 'ndx-photometry')
class ExcitationSourcesTable(DynamicTable):
    __columns__ = (
            {'name': 'peak_wavelength', 'description': '', 'required': True},
            {'name': 'type', 'description': '', 'required': True},
            {'name': 'commanded_voltage', 'description': '', 'required': True},
            {'name': 'output', 'description': '', 'required': False},
            {'name': 'model_number', 'description': '', 'required': False},

        )

@register_class('PhotodetectorsTable', 'ndx-photometry')
class PhotodetectorsTable(DynamicTable):
    __columns__ = (
            {'name': 'peak_wavelength', 'description': '', 'required': True},
            {'name': 'type', 'description': '', 'required': True},
            {'name': 'gain', 'description': '', 'required': True},
            {'name': 'model_number', 'description': '', 'required': False},

        )

@register_class('FibersTable', 'ndx-photometry')
class FibersTable(DynamicTable):
    __columns__ = (
            {'name': 'location', 'description': '', 'required': True},
            {'name': 'excitation_source', 'description': '', 'required': True},
            {'name': 'photodetector', 'description': '', 'required': True},
            {'name': 'description', 'description': '', 'required': True},
            {'name': 'fiber_model_number', 'description': '', 'required': False},
            {'name': 'dichroic_model_number', 'description': '', 'required': False},

        )