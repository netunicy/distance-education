from django.urls import path

from homepage import views

from homepage.helpers.stripe_pay import (
    chapter_stripe_payment,
    book_stripe_payment,
)


app_name = "homepage"


urlpatterns = [

    # ==========================================
    # HOME
    # ==========================================

    path("",views.homepage,name="homepage",),


    # ==========================================
    # SEARCH
    # ==========================================

    path("search/",views.search,name="search",),
    # ==========================================
    # BOOK CONTENTS
    # ==========================================
    path("book/<int:book_id>/",views.book_contents,name="book_contents",),
    # ==========================================
    # TOPICS CONTENTS
    # ==========================================
    path("topics/<int:topics_id>/",views.topics_contents,name="topics_contents",),
    # ==========================================
    # VIDEOS
    # ==========================================
    path("video/<int:video_id>/",views.show_video,name="show_video",),
    path("topics/video/<int:material_id>/",views.show_topics_video,name="show_topics_video",),
    # ==========================================
    # CHAPTER PAYMENT
    # ==========================================
    path("chapter-payment/<int:book_id>/<int:chapter_id>/",chapter_stripe_payment,name="chapter_payment",),
    # ==========================================
    # BOOK PAYMENT
    # ==========================================
    path("book-payment/<int:book_id>/",book_stripe_payment,name="book_payment",),
    # ==========================================
    # PAYMENT SUCCESS
    # ==========================================
    path("pay_success/",views.pay_success,name="pay_success",),
]