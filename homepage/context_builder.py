from homepage.models import Logo, FooterLogo

def build_base_context():
    context = {
        # Logo της πλατφόρμας
        "logo": Logo.objects.all(),
        "footer_logo": FooterLogo.objects.all(),
    }
    return context