from homepage.models import SchoolVideo 

def get_previous_video(video):
    #Επιστρέφει το προηγούμενο video του βιβλίου.
    # Παίρνει όλα τα videos του βιβλίου
    book_videos = list(get_book_videos(video.chapter.context))
    current_index = book_videos.index(video)
    # Αν υπάρχει προηγούμενο video
    if current_index > 0:
        # Επιστρέφει το προηγούμενο
        return book_videos[current_index - 1]
    # Δεν υπάρχει προηγούμενο
    return None

#Επιστρέφει το επόμενο video του βιβλίου.
def get_next_video(video):
    # Παίρνει όλα τα videos του βιβλίου
    book_videos = list(get_book_videos(video.chapter.context))
    # Βρίσκει τη θέση του τρέχοντος video
    current_index = book_videos.index(video)
    # Αν υπάρχει επόμενο video
    if current_index < len(book_videos) - 1:
        # Επιστρέφει το επόμενο
        return book_videos[current_index + 1]
    # Δεν υπάρχει επόμενο
    return None

def get_book_videos(book):
    #Επιστρέφει όλα τα videos του βιβλίου με τη σωστή σειρά ταξινόμησης.
    # Αναζητά όλα τα videos του βιβλίου
    book_videos = SchoolVideo.objects.filter(chapter__context=book)
    # Επιστρέφει όλα τα videos
    return book_videos

def get_videos_by_chapter(chapter):
    # Αναζητά όλα τα videos του συγκεκριμένου chapter
    chapter_videos = SchoolVideo.objects.filter(chapter=chapter)

    # Επιστρέφει τα videos
    return chapter_videos