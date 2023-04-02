import os
from cudatext import *
#from cudax_lib import get_translation
#_   = get_translation(__file__)  # I18N

CAPTION = 'MO File Viewer'

import gettext

class Command:
    
    dialog_visible = False
    
    def __init__(self):
        self.hdlg = None
        self.messages = ''
        self.my_list = []
        
    def open_file(self):
        try:
            self.filename = dlg_file(True, '', '', '*.mo|*.mo', 'Please, provide path to .mo file')
            dlg_proc(self.hdlg, DLG_PROP_SET, prop={'cap': CAPTION + ' - ' + self.filename})
            translation = gettext.GNUTranslations(open(self.filename, 'rb'))
            self.messages = [str(n)+'\r'+k.replace('\t',chr(3))+'\r'+v.replace('\t',chr(3))+'\t' for n, (k, v) in enumerate(translation._catalog.items())]
            self.messages.insert(0,'Offset\rOriginal\rTranslation\t') # first row is column headers
            self.my_list = list(translation._catalog.items())
        except:
            print("MO File Viewer: exception occurred")
            
    def fill_data(self):
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='mylistview', prop={
            'items': ''.join(self.messages),
            'columns': '\t'.join([
                '\r'.join(['Offset', '70','','','L']),
                '\r'.join(['Original', '400']),
                '\r'.join(['Translation', '400']),
                ]),
            })
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo1', prop={'val': ''})
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo2', prop={'val': ''})

    def run(self):
        if self.dialog_visible:
            return
        
        self.hdlg = dlg_proc(0, DLG_CREATE)
        
        def onclose(*args, **kwargs):
            self.dialog_visible = False
            timer_proc(TIMER_START_ONE, lambda *args, **wargs: dlg_proc(self.hdlg, DLG_FREE), 100)
        
        dlg_proc(self.hdlg, DLG_PROP_SET, prop={'cap': 'MO File Viewer', 'w': 920, 'h': 650, 'border': DBORDER_SIZE,
        'w_min': 400,
        'h_min': 330,
        'on_close': onclose})
        
        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'memo')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'memo1',
            'align': ALIGN_BOTTOM,
            'sp_a': 10,
            'w': 450,
            'h': 100,
            'ex0': True,
        })

        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'memo')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'memo2',
            'align': ALIGN_BOTTOM,
            'sp_a': 10,
            'w': 450,
            'h': 100,
            'ex0': True,
        })
        
        def onclick(id_dlg, id_ctl, data):
            index = data[0]
            selected = data[1]
            if selected:
                dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo1', prop={'val': self.my_list[index][0].replace('\t',chr(3))})
                dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo2', prop={'val': self.my_list[index][1].replace('\t',chr(3))})
        
        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'listview')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'mylistview',
            'align': ALIGN_TOP,
            'sp_a': 10,
            'a_b':('memo1','['),
            'columns': '\t'.join([
                '\r'.join(['Offset', '70','','','L']),
                '\r'.join(['Original', '400']),
                '\r'.join(['Translation', '400']),
                ]),
            'on_select': onclick,
            })
            
        self.filename = None
        def onbutton(*args, **kwargs):
            self.open_file()
            self.fill_data()
            
        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'button')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'mybutton',
            'cap': 'Open...',
            'align': ALIGN_TOP,
            'sp_a': 10,
            'on_change': onbutton,
            })
        
        dlg_proc(self.hdlg, DLG_SCALE)
        
        self.dialog_visible = True
        dlg_proc(self.hdlg, DLG_SHOW_NONMODAL)

