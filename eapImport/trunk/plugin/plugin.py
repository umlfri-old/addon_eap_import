__author__ = 'janik'

from convertor import Convertor

def pluginMain(interface):
    interface.transaction.autocommit = True
    ft = interface.file_type_manager.register_file_type('application/eap', 'Enterprise architect project')
    ft.add_extension('eap')
    ft.import_enabled = True
    ft.register_import_handler(lambda fileName: Convertor(interface, fileName))
