from django.urls import path
from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("search/", views.search, name="search"),
    path("book/<int:book_id>/",views.book_contents,name="book_contents",),
    path("training/<int:training_id>/",views.training_contents,name="training_contents",),
    # ==========================================
    # Video
    # ==========================================
    # Προβολή εκπαιδευτικού βίντεο
    path("video/<int:video_id>/",views.show_video,name="show_video"),
    path("training/video/<int:material_id>/",views.show_training_video,name="show_training_video",),
    path("terms-and-conditions/", views.terms_and_conditions, name="terms_and_conditions"),
    path("contact/", views.contact, name="contact"),
    path("announcements/", views.announcements, name="announcements"),
    path("faq/", views.faq, name="faq"),
    path("about-us/", views.about_us, name="about_us"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("copyright-notice/", views.copyright_notice, name="copyright_notice"),
    path("refund-policy/", views.refund_policy, name="refund_policy"),
]