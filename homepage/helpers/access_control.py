from homepage.models.user_purchases import UserPurchase
from homepage.models.topic_purchases import TopicPurchase
#Ελέγχει αν ο χρήστης είναι διαχειριστής.
def is_admin(user):
    # Επιστρέφει αν ο χρήστης είναι Superuser
    return user.is_superuser

#Ελέγχει αν το video είναι δωρεάν.
def is_free_video(video):
    # Επιστρέφει αν το video είναι δωρεάν
    return video.is_free

# ==========================================
# Έλεγχος Αγοράς Βιβλίου
# ==========================================

# ==========================================
# Έλεγχος Αγοράς Βιβλίου
# ==========================================

def has_purchased_book(user, book):

    if not user.is_authenticated:
        return False

    return UserPurchase.objects.filter(
        user=user,
        book=book,
        chapter__isnull=True,
    ).exists()

# ==========================================
# Έλεγχος Αγοράς Κεφαλαίου
# ==========================================

def has_purchased_chapter(user, chapter):

    if not user.is_authenticated:
        return False

    return UserPurchase.objects.filter(
        user=user,
        chapter=chapter,
    ).exists()
# ==========================================
# Έλεγχος Συνδρομής
# ==========================================

def has_active_subscription(user):
    """
    Ελέγχει αν ο χρήστης έχει
    ενεργή συνδρομή.

    Args:
        user:
            Ο συνδεδεμένος χρήστης.

    Returns:
        True αν έχει ενεργή συνδρομή.
        False διαφορετικά.
    """

    # Θα υλοποιηθεί αργότερα
    return False

# ==========================================
# Έλεγχος Promo Code
# ==========================================

def has_active_promocode(user):
    """
    Ελέγχει αν ο χρήστης έχει
    ενεργό Promo Code.

    Args:
        user:
            Ο συνδεδεμένος χρήστης.

    Returns:
        True αν έχει ενεργό Promo Code.
        False διαφορετικά.
    """

    # Θα υλοποιηθεί αργότερα
    return False

# ==========================================
# Έλεγχος Πρόσβασης Video
# ==========================================

# ==========================================
# Έλεγχος Πρόσβασης School Video
# ==========================================

def can_view_video(user, video, book):

    # Administrator
    if is_admin(user):
        return True

    # Δωρεάν Video
    if is_free_video(video):
        return True

    # Αγορά Βιβλίου
    if has_purchased_book(user, book):
        return True

    # Αγορά Κεφαλαίου
    if has_purchased_chapter(user, video.chapter):
        return True

    # Αγορά Topic
    if user.is_authenticated:

        has_topic_access = TopicPurchase.objects.filter(
            user=user,
            topic__topics_contents__school_videos=video,
        ).exists()

        if has_topic_access:
            return True

    # Ενεργή Συνδρομή
    if has_active_subscription(user):
        return True

    # Ενεργό Promo Code
    if has_active_promocode(user):
        return True

    # Δεν επιτρέπεται η πρόσβαση
    return False
# ==========================================
# Έλεγχος Αγοράς Topic
# ==========================================

def has_purchased_topic(user, topic):

    if not user.is_authenticated:
        return False

    return TopicPurchase.objects.filter(
        user=user,
        topic=topic,
    ).exists()


# ==========================================
# Έλεγχος Πρόσβασης Topics Video
# ==========================================

def can_view_topics_video(user, material, topic):

    # Administrator
    if is_admin(user):
        return True

    # Δωρεάν Video
    if is_free_video(material):
        return True

    # Αγορά Topic
    if has_purchased_topic(user, topic):
        return True

    # Ενεργή Συνδρομή
    if has_active_subscription(user):
        return True

    # Ενεργό Promo Code
    if has_active_promocode(user):
        return True

    # Δεν επιτρέπεται η πρόσβαση
    return False