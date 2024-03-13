# -*- coding: utf-8 -*-
from Products.MaildropView import maildropview


def initialize(context):
    """site."""
    context.registerClass(
        maildropview.MaildropView,
        constructors=(
            maildropview.manage_add_maildrop_view_form,
            maildropview.manage_add_maildrop_view,
        ),
        icon='img/icon.png'
    )
