# ==========================================
# Βιβλιοθήκες
# ==========================================

from django.shortcuts import get_object_or_404

from homepage.models import Video


# ==========================================
# Αναζήτηση Video
# ==========================================

def get_video(video_id):
    """
    Αναζητά ένα video.

    Args:
        video_id:
            Το μοναδικό id του video.

    Returns:
        Το αντικείμενο Video.
    """

    # Αναζητά το video.
    # Αν δεν βρεθεί εμφανίζει 404.
    video = get_object_or_404(

        Video,

        id=video_id

    )

    # Επιστρέφει το video
    return video

# ==========================================
# Ενημέρωση Προβολών
# ==========================================

def increment_video_views(video):
    """
    Αυξάνει τις προβολές του video.

    Args:
        video:
            Το αντικείμενο Video.
    """

    # Αυξάνει τις προβολές κατά 1
    video.views += 1

    # Αποθηκεύει μόνο το πεδίο views
    video.save(
        update_fields=[
            "views"
        ]
    )

#Δημιουργεί το context της σελίδας εκπαιδευτικού υλικού.
def create_learning_context(
    book,
    chapter,
    video,
    protected_video,
    previous_video,
    next_video,
    chapter_videos,
):
    # Δημιουργεί το context
    context = {
        # Βιβλίο
        "book": book,
        # Chapter
        "chapter": chapter,
        # Τρέχον video
        "video": video,
        # Προστατευμένο video
        "protected_video": protected_video,
        # Προηγούμενο video
        "previous_video": previous_video,
        # Επόμενο video
        "next_video": next_video,
        # Videos του chapter
        "chapter_videos": chapter_videos,
    }
    # Επιστρέφει το context
    return context