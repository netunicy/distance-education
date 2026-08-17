from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from homepage.models.topics import Topics
from .models import Logo, Schoolcontexts,InformationPage,Informations
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.models.topics_video import TopicsVideo
from homepage.cloudflare.signed_playback import create_signed_playback_url
from django.http import HttpResponse
from homepage.context_builder import build_base_context
# Helpers
from homepage.helpers.video_service import get_video
from homepage.helpers.video_service import increment_video_views
from homepage.helpers.navigation import get_previous_video
from homepage.helpers.navigation import get_next_video
from homepage.helpers.navigation import get_videos_by_chapter
from homepage.helpers.video_security import create_secure_url
from homepage.helpers.access_control import can_view_video

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from homepage.models.school import Schoolcontexts
from homepage.models.school_chapter import Chapter
from homepage.models.user_purchases import UserPurchase


def homepage(request):
    logo = Logo.objects.all()
    messages.success(request, "Welcome to the Homepage!")

    contexts = Schoolcontexts.objects.prefetch_related("chapters")

    # Διόρθωση με τα πραγματικά ονόματα πεδίων του μοντέλου Schoolcontexts:
    active_levels = contexts.values_list("stage", flat=True).distinct()
    active_subjects = contexts.values_list("subject_lesson", flat=True).distinct()
    active_classes = contexts.values_list("class_is", flat=True).distinct()

    # Φιλτράρισμα των choices
    filtered_levels = [
        (val, label) for val, label in Schoolcontexts.LevelType.choices
        if val in active_levels
    ]

    filtered_subjects = [
        (val, label) for val, label in Schoolcontexts.SubjectLesson.choices
        if val in active_subjects
    ]

    filtered_classes = [
        (val, label) for val, label in Schoolcontexts.ClassLevel.choices
        if val in active_classes
    ]

    # Topics logic
    topics = Topics.objects.prefetch_related("topics_contents").all()

    active_category_keys = topics.values_list(
        "category",
        flat=True
    ).distinct()

    active_topics_categories = [
        (value, label)
        for value, label in Topics.Category.choices
        if value in active_category_keys
    ]

    cards = InformationPage.objects.all()
    modals = Informations.objects.all()

    second_row = zip(cards, modals)

    if request.user.is_authenticated:
        user_purchases = (
            UserPurchase.objects
            .filter(user=request.user)
            .select_related(
                "book",
                "chapter",
            )
            .order_by("-purchased_at")
        )

    else:

        user_purchases = UserPurchase.objects.none()

    return render(request, "homepage/homepage.html", {
        "logo": logo,
        "contexts": contexts,
        "school_levels": filtered_levels,
        "school_subjects": filtered_subjects,
        "school_classes": filtered_classes,

        "topics": topics,
        "topics_categories": active_topics_categories,

        "second_row": second_row,

        "user_purchases": user_purchases,
    })

def search(request):
    pass

def book_contents(request, book_id):

    book = get_object_or_404(Schoolcontexts, id=book_id)

    includes = []

    for line in book.includes.splitlines():

        line = line.strip()

        if line:

            includes.append(line)

    return JsonResponse({

        "title": book.title,
        "description": book.description,
        "subject": book.subject_lesson,
        "stage": book.stage,
        "class": book.class_is,
        "edition": book.edition,
        "image": book.image.url if book.image else "",
        "price_chapter": book.price_chapter,
        "price_all": book.price_all,

        "includes": includes,

        "chapters": [

        {

            "id": chapter.id,

            "order": chapter.order,

            "title": chapter.title,

            "videos": [

                {
                    "id": video.id,
                    "page": video.page,
                    "part": video.part,
                    "url": reverse(
                        "homepage:show_video",
                        args=[video.id],
                    ),
                    "is_free": video.is_free,
                    "activity_title": video.activity_title,
                }

                for video in chapter.videos.all()

            ]

        }

        for chapter in book.chapters.all()

    ]

    })

def topics_contents(request, topics_id):

    # ==========================================
    # Αναζήτηση Topics
    # ==========================================

    topic = get_object_or_404(
        Topics,
        id=topics_id,
    )

    # ==========================================
    # Τι περιλαμβάνει
    # ==========================================

    includes = [
        line.strip()
        for line in topic.includes.splitlines()
        if line.strip()
    ]

    # ==========================================
    # Περιεχόμενα Topics
    # ==========================================

    contents = []

    for content in (
        topic.topics_contents
        .prefetch_related(
            "materials",
            "school_videos",
        )
        .order_by("order")
    ):

        videos = []

        # ======================================
        # Topics Videos
        # ======================================

        for video in (
            content.materials
            .filter(
                material_type=TopicsVideo.MaterialType.VIDEO
            )
            .order_by("order")
        ):

            videos.append({

                "id": video.id,

                "title": video.title,

                "is_free": video.is_free,

                "url": (
                    reverse(
                        "homepage:show_topics_video",
                        args=[video.id],
                    )
                    if video.is_free else ""
                ),

                "source": "topics",

            })

        # ======================================
        # School Videos
        # ======================================

        for video in (
            content.school_videos
            .select_related("chapter")
            .order_by(
                "chapter__order",
                "page",
                "part",
            )
        ):

            # Τίτλος School Video
            title = video.activity_title.strip()

            if not title:
                title = f"Σελίδα {video.page}"

            videos.append({

                "id": video.id,

                "title": title,

                "is_free": video.is_free,

                "url": (
                    reverse(
                        "homepage:show_video",
                        args=[video.id],
                    )
                    if video.is_free else ""
                ),

                "source": "school",

            })

        # ======================================
        # Ενότητα
        # ======================================

        contents.append({

            "id": content.id,

            "order": content.order,

            "title": content.content,

            "description": content.description,

            "videos": videos,

        })

    # ==========================================
    # Επιστροφή JSON
    # ==========================================

    return JsonResponse({

        "id": topic.id,

        "title": topic.title,

        "slug": topic.slug,

        "description": topic.description,

        "category": topic.get_category_display(),

        "level": topic.get_level_display(),

        "image": (
            topic.image.url
            if topic.image else ""
        ),

        "price": str(topic.price),

        "includes": includes,

        "contents": contents,

    })

@login_required
def show_topics_video(request, material_id):

    material = get_object_or_404(
        TopicsVideo,
        id=material_id,
    )

    secure_video_url = create_signed_playback_url(
        material.cloudflare_uid,
    )

    context = {
        "material": material,
        "secure_video_url": secure_video_url,
    }

    return render(
        request,
        "homepage/show_topics_video.html",
        context,
    )


@login_required
def show_video(request, video_id):

    # Αναζητά το video με βάση το μοναδικό id
    video = get_video(video_id)

    # Παίρνει το chapter στο οποίο ανήκει το video
    chapter = video.chapter

    # Παίρνει το βιβλίο στο οποίο ανήκει το chapter
    book = chapter.context

    # Ελέγχει αν ο χρήστης μπορεί να δει το video
    if not can_view_video(
        request.user,
        video,
        book,
    ):
        return redirect("homepage:homepage")

    # Αυξάνει τις προβολές του video
    increment_video_views(video)

    # Δημιουργεί το προστατευμένο Cloudflare Signed Playback URL
    secure_video_url = create_signed_playback_url(
        video.cloudflare_uid,
    )

    # Αναζητά το προηγούμενο video
    previous_video = get_previous_video(video)

    # Αναζητά το επόμενο video
    next_video = get_next_video(video)

    # Παίρνει όλα τα videos του chapter
    chapter_videos = get_videos_by_chapter(chapter)

    # ==========================================
    # Δημιουργία Context
    # ==========================================

    context = build_base_context()

    context.update({

        # Το βιβλίο
        "book": book,

        # Το chapter
        "chapter": chapter,

        # Το video
        "video": video,

        # Το προστατευμένο video
        "secure_video_url": secure_video_url,

        # Το προηγούμενο video
        "previous_video": previous_video,

        # Το επόμενο video
        "next_video": next_video,

        # Τα videos του chapter
        "chapter_videos": chapter_videos,

    })

    return render(
        request,
        "homepage/show_video.html",
        context,
    )

@login_required
def chapter_payment(request, book_id, chapter_id):

    # ==========================================
    # Βιβλίο
    # ==========================================

    book = get_object_or_404(
        Schoolcontexts,
        id=book_id,
    )

    # ==========================================
    # Κεφάλαιο
    # ==========================================

    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        context=book,
    )

    # ==========================================
    # Προσωρινός έλεγχος
    # ==========================================

    print("BOOK:", book)
    print("BOOK ID:", book.id)

    print("CHAPTER:", chapter)
    print("CHAPTER ID:", chapter.id)

    print("PRICE:", book.price_chapter)

    return HttpResponse(
        f"""
        Βιβλίο: {book}<br>
        Book ID: {book.id}<br><br>

        Κεφάλαιο: {chapter.title}<br>
        Chapter ID: {chapter.id}<br><br>

        Τιμή κεφαλαίου: £{book.price_chapter}
        """
    )

@login_required
def pay_success(request):

    # ==========================================
    # Stripe Session ID
    # ==========================================

    session_id = request.GET.get("session_id")

    if not session_id:
        return render(
            request,
            "payment_error.html",
            {
                "error_message": "Δεν βρέθηκε η συναλλαγή."
            },
        )

    # ==========================================
    # Stripe
    # ==========================================

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:

        session = stripe.checkout.Session.retrieve(
            session_id
        )

    except stripe.error.StripeError:

        return render(
            request,
            "payment_error.html",
            {
                "error_message": "Δεν ήταν δυνατή η επιβεβαίωση της πληρωμής."
            },
        )

    # ==========================================
    # Έλεγχος πληρωμής
    # ==========================================

    if session.payment_status != "paid":

        return render(
            request,
            "payment_error.html",
            {
                "error_message": "Η πληρωμή δεν έχει ολοκληρωθεί."
            },
        )

    # ==========================================
    # Metadata
    # ==========================================

    metadata = session.metadata

    user_id = metadata.get("user_id")
    book_id = metadata.get("book_id")
    chapter_id = metadata.get("chapter_id")

    # ==========================================
    # Έλεγχος χρήστη
    # ==========================================

    if str(request.user.id) != user_id:

        return render(
            request,
            "payment_error.html",
            {
                "error_message": "Η συναλλαγή δεν ανήκει στον συγκεκριμένο χρήστη."
            },
        )

    # ==========================================
    # Βιβλίο
    # ==========================================

    book = get_object_or_404(
        Schoolcontexts,
        id=book_id,
    )

    # ==========================================
    # Κεφάλαιο
    # ==========================================

    chapter = get_object_or_404(
        Chapter,
        id=chapter_id,
        context=book,
    )

    # ==========================================
    # Καταχώριση αγοράς
    # ==========================================

    purchase, created = UserPurchase.objects.get_or_create(

        stripe_session_id=session.id,

        defaults={
            "user": request.user,
            "book": book,
            "chapter": chapter,
            "amount_paid": session.amount_total,
        },
    )

    # ==========================================
    # Success
    # ==========================================

    return render(
        request,
        "pay_success.html",
        {
            "purchase": purchase,
            "created": created,
        },
    )