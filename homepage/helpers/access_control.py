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

def has_purchased_book(user, book):
    """
    Ελέγχει αν ο χρήστης έχει αγοράσει το βιβλίο.

    Args:
        user:
            Ο συνδεδεμένος χρήστης.

        book:
            Το βιβλίο.

    Returns:
        True αν έχει αγοράσει το βιβλίο.
        False διαφορετικά.
    """

    # Θα υλοποιηθεί όταν δημιουργηθεί
    # το σύστημα αγορών.
    return False

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

def can_view_video(user, video, book):
    """
    Ελέγχει αν ο χρήστης
    μπορεί να δει το video.

    Args:
        user:
            Ο συνδεδεμένος χρήστης.

        video:
            Το video.

        book:
            Το βιβλίο.

    Returns:
        True αν επιτρέπεται η πρόσβαση.
        False διαφορετικά.
    """

    # Administrator
    if is_admin(user):
        return True

    # Δωρεάν Video
    if is_free_video(video):
        return True

    # Αγορά Βιβλίου
    if has_purchased_book(user, book):
        return True

    # Ενεργή Συνδρομή
    if has_active_subscription(user):
        return True

    # Ενεργό Promo Code
    if has_active_promocode(user):
        return True

    # Δεν επιτρέπεται η πρόσβαση
    return False