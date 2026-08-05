from homepage.models import Logo

def build_base_context():
    context = {
        # Logo της πλατφόρμας
        "logo": Logo.objects.all(),
    }
    return context