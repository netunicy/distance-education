from homepage.models import Logo, FooterLogo, Informations, BackgroundImage


def build_base_context():
    context = {
        "logo": Logo.objects.all(),
        "footer_logo": FooterLogo.objects.all(),
        "footer_infos": Informations.objects.all(),
        "background_image": BackgroundImage.objects.first(),
    }

    return context