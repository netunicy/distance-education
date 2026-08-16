from django.urls import path
from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("search/", views.search, name="search"),
    path("book/<int:book_id>/",views.book_contents,name="book_contents",),
    path("topics/<int:topics_id>/",views.topics_contents,name="topics_contents",),
    # ==========================================
    # Video
    # ==========================================
    # Προβολή εκπαιδευτικού βίντεο
    path("video/<int:video_id>/",views.show_video,name="show_video"),
    path("topics/video/<int:material_id>/",views.show_topics_video,name="show_topics_video"),
]