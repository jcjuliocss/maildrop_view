"""."""
from Globals import package_home

from OFS import SimpleItem

from Products.PageTemplates.PageTemplateFile import PageTemplateFile


import os
import time
import glob
import base64

global product_path
product_path = os.path.join(package_home(globals())) + '/'


class MaildropView(SimpleItem.SimpleItem):
    """."""

    meta_type = 'maildrop_view'

    manage_options = (
        (
            {'label': 'View', 'action': 'lista_emails'},
        )
    )

    def __init__(self, id):
        """."""
        self.id = id

    def lista_emails(self):
        """."""
        lista = glob.glob('/tmp/maildrop/spool/*')
        lista_imediatos = glob.glob('/tmp/maildrop_imediato/spool/*')

        lista = sorted(lista,
                       key=os.path.getmtime)

        lista_imediatos = sorted(lista_imediatos,
                                 key=os.path.getmtime)

        nova_lista = []
        for file_path in lista:
            timestamp_str = time.strftime(
                '%d/%m/%Y - %H:%M:%S',
                time.gmtime(os.path.getmtime(file_path)))
            nova_lista.append(
                {'arquivo': file_path,
                 'horario': timestamp_str}
            )

        nova_lista_imediatos = []
        for file_path in lista_imediatos:
            timestamp_str = time.strftime(
                '%d/%m/%Y - %H:%M:%S',
                time.gmtime(os.path.getmtime(file_path)))
            nova_lista_imediatos.append(
                {'arquivo': file_path,
                 'horario': timestamp_str}
            )

        nova_lista.sort(reverse=True)
        nova_lista_imediatos.sort(reverse=True)

        return self.listagem_emails(
            lista=nova_lista,
            lista_imediatos=nova_lista_imediatos
        )

    def abrir_email(self, arquivo):
        """."""
        from os import system

        system('mhonarc ' + arquivo)

        caminho_pasta = '/'.join(product_path.split('/')[:-3])

        caminho_arquivo = caminho_pasta + '/msg00000.html'

        arquivo = open(caminho_arquivo, 'r')

        conteudo = arquivo.read()
        conteudo = conteudo.replace('https://www.nube.com.br',
                                    'http://localhost')

        arquivo.close()

        lista_caminhos_pdfs = glob.glob(caminho_pasta + '/*.bin')

        corpo_pdf = None
        lista_pdfs = []
        for caminho_pdf in lista_caminhos_pdfs:
            arquivo_pdf = open(caminho_pdf, 'r')
            corpo_pdf = arquivo_pdf.read()
            arquivo_pdf.close()
            lista_pdfs.append(base64.encodestring(str(corpo_pdf)))

        system('rm ' + caminho_pasta + '/*.bin')
        system('rm ' + caminho_pasta + '/*.html')

        string_data = 'data:application/pdf;base64,'

        return self.render_email(
            conteudo=conteudo,
            lista_pdfs=lista_pdfs,
            string_data=string_data
        )

    listagem_emails = PageTemplateFile('zpt/lista_emails', globals())
    render_email = PageTemplateFile('zpt/render_email', globals())


def manage_add_maildrop_view(self, id):
    """."""
    self._setObject(id, MaildropView(id))
    self.REQUEST.RESPONSE.redirect(id + '/lista_emails')

manage_add_maildrop_view_form = PageTemplateFile(
    'zpt/manage_add_maildrop_view_form',
    globals())
