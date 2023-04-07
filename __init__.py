import os
from cudatext import *
from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

CAPTION = _('MO File Viewer')
CAP_OFFSET = _('Offset')
CAP_ORIGINAL = _('Original')
CAP_TRAN = _('Translation')

import gettext

class Command:

    dialog_visible = False

    def __init__(self):
        self.hdlg = None
        self.messages = ''
        self.my_list = []

    def open_file(self):

        def _escape(s):
            return s.replace('\t', chr(3)).replace('\r', '|')

        self.filename = dlg_file(True, '', '', '*.mo|*.mo', _('Please, provide path to .mo file'))
        if self.filename:
            dlg_proc(self.hdlg, DLG_PROP_SET, prop={'cap': CAPTION + ' - ' + self.filename})
            translation = gettext.GNUTranslations(open(self.filename, 'rb'))
            self.messages = [str(n)+'\r'+_escape(k)+'\r'+_escape(v)+'\t' for n, (k, v) in enumerate(translation._catalog.items())]
            self.messages.insert(0, CAP_OFFSET+'\r'+CAP_ORIGINAL+'\r'+CAP_TRAN+'\t') # first row is column headers
            self.my_list = list(translation._catalog.items())
        return self.filename

    def fill_data(self):
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='mylistview', prop={
            'items': ''.join(self.messages),
            'columns': '\t'.join([
                '\r'.join([CAP_OFFSET, '70','','','L']),
                '\r'.join([CAP_ORIGINAL, '400']),
                '\r'.join([CAP_TRAN, '400']),
                ]),
            })
        # Clear the memo panels when loading the (next) file
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo1', prop={'val': ''})
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, name='memo2', prop={'val': ''})

    def run(self):
        if self.dialog_visible:
            return

        self.hdlg = dlg_proc(0, DLG_CREATE)

        def onclose(*args, **kwargs):
            self.dialog_visible = False
            timer_proc(TIMER_START_ONE, lambda *args, **kwargs: dlg_proc(self.hdlg, DLG_FREE), 100)

        dlg_proc(self.hdlg, DLG_PROP_SET, prop={
            'cap': CAPTION,
            'w': 920,
            'h': 650,
            'border': DBORDER_SIZE,
            'w_min': 400,
            'h_min': 330,
            'on_close': onclose,
        })

        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'memo')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'memo1',
            'align': ALIGN_BOTTOM,
            'sp_a': 6,
            'w': 450,
            'h': 100,
            'ex0': True,
        })

        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'memo')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'memo2',
            'align': ALIGN_BOTTOM,
            'sp_a': 6,
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
            'sp_a': 6,
            'a_b':('memo1','['),
            'columns': '\t'.join([
                '\r'.join([CAP_OFFSET, '70','','','L']),
                '\r'.join([CAP_ORIGINAL, '400']),
                '\r'.join([CAP_TRAN, '400']),
                ]),
            'on_select': onclick,
            })

        self.filename = None
        def onbutton(*args, **kwargs):
            self.open_file() and self.fill_data()

        n = dlg_proc(self.hdlg, DLG_CTL_ADD, 'button')
        dlg_proc(self.hdlg, DLG_CTL_PROP_SET, index=n, prop={
            'name': 'mybutton',
            'cap': _('Open...'),
            'align': ALIGN_TOP,
            'sp_a': 6,
            'on_change': onbutton,
            })

        dlg_proc(self.hdlg, DLG_SCALE)

        self.dialog_visible = True
        dlg_proc(self.hdlg, DLG_SHOW_NONMODAL)
