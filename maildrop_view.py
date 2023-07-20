"""."""
from Globals import package_home

from OFS import SimpleItem

from Products.PageTemplates.PageTemplateFile import PageTemplateFile


import os
import time
import glob
import base64
from os import system

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

    def __init__(self, id, caminho_repo):
        """."""
        self.id = id
        self.caminho_repo = caminho_repo

    def lista_emails(self):
        """."""
        system(self.caminho_repo + 'docker-dev/commands/spool copy')
        lista = glob.glob('/tmp/maildrop/spool/*')
        lista_imediatos = glob.glob('/tmp/maildrop_imediato/spool/*')
        lista_assinebem = glob.glob(
            '/tmp/maildrop/spool/assinebem-app/*')

        # lista = sorted(lista,
        #                key=os.path.getmtime)

        # lista_imediatos = sorted(lista_imediatos,
        #                          key=os.path.getmtime)

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

        nova_lista_ass_bem = []
        for file_path in lista_assinebem:
            timestamp_str = time.strftime(
                '%d/%m/%Y - %H:%M:%S',
                time.gmtime(os.path.getmtime(file_path)))
            nova_lista_ass_bem.append(
                {'arquivo': file_path,
                 'horario': timestamp_str}
            )

        nova_lista.sort(reverse=True)
        nova_lista_imediatos.sort(reverse=True)
        nova_lista_ass_bem.sort(reverse=True)

        return self.listagem_emails(
            lista=nova_lista,
            lista_imediatos=nova_lista_imediatos,
            lista_assinebem=nova_lista_ass_bem
        )

    def abrir_email(self, arquivo):
        """."""
        system('mhonarc {} -outdir /tmp'.format(arquivo))

        # caminho_pasta = '/'.join(product_path.split('/')[:-3])

        caminho_arquivo = '/tmp/msg00000.html'

        arquivo = open(caminho_arquivo, 'r')

        conteudo = arquivo.read()
        conteudo = conteudo.replace('https://www.nube.com.br',
                                    'http://localhost')
        conteudo = conteudo.replace('https://nube.com.br',
                                    'http://localhost')
        conteudo = conteudo.replace('https://nubenet.nube.com.br',
                                    'http://localhost')

        arquivo.close()

        lista_caminhos_pdfs = glob.glob('/tmp/*.bin')

        corpo_pdf = None
        lista_pdfs = []
        for caminho_pdf in lista_caminhos_pdfs:
            arquivo_pdf = open(caminho_pdf, 'r')
            corpo_pdf = arquivo_pdf.read()
            arquivo_pdf.close()
            lista_pdfs.append(base64.encodestring(str(corpo_pdf)))

        system('rm /tmp/*.bin')
        system('rm /tmp/*.html')

        string_data = 'data:application/pdf;base64,'

        return self.render_email(
            conteudo=conteudo,
            lista_pdfs=lista_pdfs,
            string_data=string_data
        )

    def excluir_email(self, arquivo=None):
        """Excluir um email."""
        if not arquivo:
            raise Exception('Nenhum arquivo para excluir')

        os.remove(arquivo)

        if 'assinebem-app' in arquivo:
            caminho_assinebem_docker = arquivo.replace('/assinebem-app', '')
            system('docker exec assinebem-app rm -rf {}'.format(
                caminho_assinebem_docker))

        return """
            <script>
                alert('email excluido');
                window.location.assign('lista_emails');
            </script>
        """

    listagem_emails = PageTemplateFile('zpt/lista_emails', globals())
    render_email = PageTemplateFile('zpt/render_email', globals())


def manage_add_maildrop_view(self, id, caminho_repo):
    """."""
    mdv = MaildropView(id, caminho_repo)
    self._setObject(id, mdv)
    self.REQUEST.RESPONSE.redirect(id + '/lista_emails')

manage_add_maildrop_view_form = PageTemplateFile(
    'zpt/manage_add_maildrop_view_form',
    globals())
