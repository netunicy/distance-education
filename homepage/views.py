from django.shortcuts import render
from homepage.models.training import Training
from .models import Logo, Mycontexts,InformationPage
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from homepage.models.TrainingMaterial import TrainingMaterial
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

def homepage(request):
    logo = Logo.objects.all()
    messages.success(request, "Welcome to the Homepage!")
    
    contexts = Mycontexts.objects.prefetch_related("chapters")

    # Διόρθωση με τα πραγματικά ονόματα πεδίων του μοντέλου Mycontexts:
    active_levels = contexts.values_list("stage", flat=True).distinct()
    active_subjects = contexts.values_list("subject_lesson", flat=True).distinct()
    active_classes = contexts.values_list("class_is", flat=True).distinct()

    # Φιλτράρισμα των choices
    filtered_levels = [
        (val, label) for val, label in Mycontexts.LevelType.choices 
        if val in active_levels
    ]
    filtered_subjects = [
        (val, label) for val, label in Mycontexts.SubjectLesson.choices 
        if val in active_subjects
    ]
    filtered_classes = [
        (val, label) for val, label in Mycontexts.ClassLevel.choices 
        if val in active_classes
    ]

    # Training logic
    trainings = Training.objects.prefetch_related("training_contents").filter(is_published=True)
    active_category_keys = trainings.values_list("category", flat=True).distinct()
    active_training_categories = [
        (value, label) for value, label in Training.Category.choices 
        if value in active_category_keys
    ]

    second_row_images = InformationPage.objects.filter(
        page__in=["refund_policy", "copyright_notice", "privacy_policy", "about_us", "faq", "terms_and_conditions", "announcements", "contact"]
    )

    return render(request, "homepage/homepage.html", {
        "logo": logo,
        "contexts": contexts,
        "school_levels": filtered_levels,
        "school_subjects": filtered_subjects,
        "school_classes": filtered_classes,
        "trainings": trainings,
        "training_categories": active_training_categories,
        "second_row": second_row_images,
    })

def search(request):
    pass

def book_contents(request, book_id):

    book = get_object_or_404(Mycontexts, id=book_id)

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
        "image": book.image,
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

def training_contents(request, training_id):

    # ==========================================
    # Αναζήτηση Προγράμματος
    # ==========================================

    training = get_object_or_404(Training,id=training_id,is_published=True,)

    # ==========================================
    # Τι περιλαμβάνει
    # ==========================================

    includes = [
        line.strip()
        for line in training.includes.splitlines()
        if line.strip()
    ]

    # ==========================================
    # Περιεχόμενα Προγράμματος
    # ==========================================

    contents = []

    for content in training.training_contents.prefetch_related("materials").order_by("order"):

        # Πρώτο δωρεάν video της ενότητας
        free_video = content.materials.filter(material_type=TrainingMaterial.MaterialType.VIDEO,is_free=True,).first()

        contents.append({

            "id": content.id,

            "order": content.order,

            "title": content.content,

            "description": content.description,

            # Υπάρχει δωρεάν video;
            "has_free_video": free_video is not None,

            # URL δωρεάν video
            "video_url": (
                reverse(
                    "homepage:show_training_video",
                    args=[free_video.id],
                )
                if free_video else ""
            ),

        })

    # ==========================================
    # Επιστροφή JSON
    # ==========================================

    return JsonResponse({

        "id": training.id,

        "title": training.title,

        "slug": training.slug,

        "description": training.description,

        "category": training.category,

        "level": training.level,

        "image": training.image,

        "price": training.price,

        "includes": includes,

        "contents": contents,

    })

@login_required
def show_training_video(request, material_id):

    # ==========================================
    # Αναζήτηση Training Material
    # ==========================================

    # Αναζητά το εκπαιδευτικό υλικό
    material = get_object_or_404(
        TrainingMaterial,
        id=material_id,
    )

    # Δημιουργεί το προστατευμένο Cloudflare Signed Playback URL
    secure_video_url = create_signed_playback_url(
        material.cloudflare_uid,
    )

    context = {

        # Το εκπαιδευτικό υλικό
        "material": material,

        # Το προστατευμένο video
        "secure_video_url": secure_video_url,

    }

    return render(
        request,
        "homepage/show_training_video.html",
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

def terms_and_conditions(request):
    return redirect("homepage:homepage")

def contact(request):
    return redirect("homepage:homepage")

def announcements(request):
    return redirect("homepage:homepage")

def faq(request):
    return redirect("homepage:homepage")

def about_us(request):
    return redirect("homepage:homepage")

def privacy_policy(request):
    return redirect("homepage:homepage")

def copyright_notice(request):
    return redirect("homepage:homepage")

def refund_policy(request):
    return redirect("homepage:homepage")

