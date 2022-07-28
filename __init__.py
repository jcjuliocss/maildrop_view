"""init do site."""
import maildrop_view


def initialize(context):
    """site."""
    context.registerClass(
        maildrop_view.MaildropView,
        constructors=(
            maildrop_view.manage_add_maildrop_view_form,
            maildrop_view.manage_add_maildrop_view,
        ),
        icon='img/icon.png'
    )
