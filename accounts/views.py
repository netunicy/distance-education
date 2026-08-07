import random
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.conf import settings
from .forms import RegisterForm
import mailtrap as mt
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EmailOrUsernameLoginForm
from homepage.models import Logo

# accounts/views.py

def login_view(request):
    logo=Logo.objects.all()
    if request.user.is_authenticated:
        return redirect("homepage:homepage")

    if request.method == "POST":
        form = EmailOrUsernameLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Καλώς ήρθατε ξανά, {user.username}!")
            return redirect("homepage:homepage")
    else:
        form = EmailOrUsernameLoginForm()

    return render(request, "accounts/login.html", {"form": form, "logo": logo})


# ==========================================
# 2. REGISTER VIEW (Step 1: Create & Send OTP)
# ==========================================
def register_view(request):
    logo=Logo.objects.all()
    """Δημιουργεί μη ενεργό χρήστη και στέλνει OTP μέσω Mailtrap."""
    if request.user.is_authenticated:
        return redirect("homepage:homepage")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 1. Αποθήκευση χρήστη ως μη ενεργού (is_active = False)
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # 2. Παραγωγή 6ψήφιου OTP
            otp_code = str(random.randint(100000, 999999))

            # 3. Αποθήκευση στο Session για επαλήθευση στο επόμενο βήμα
            request.session['pending_user_id'] = user.id
            request.session['register_otp'] = otp_code

            # 4. Σύνθεση και αποστολή HTML Email μέσω Mailtrap SDK
            subject = "🔒 Κωδικός Επαλήθευσης Εγγραφής"
            
            html_message = f"""
            <div style="font-family: Arial, sans-serif; padding: 24px; background-color: #f8fafc; border-radius: 8px; max-width: 500px; margin: auto;">
                <h2 style="color: #0f172a; text-align: center;">Επαλήθευση Λογαριασμού</h2>
                <p style="color: #475569; font-size: 15px;">Ευχαριστούμε για την εγγραφή σας! Ο κωδικός επιβεβαίωσης για την ενεργοποίηση του λογαριασμού σας είναι:</p>
                
                <div style="background-color: #2563eb; color: #ffffff; font-size: 28px; font-weight: bold; letter-spacing: 6px; padding: 14px; text-align: center; border-radius: 8px; margin: 24px 0;">
                    {otp_code}
                </div>
                
                <p style="color: #94a3b8; font-size: 13px; text-align: center;">Αν δεν πραγματοποιήσατε εσείς αυτή την εγγραφή, παρακαλούμε αγνοήστε το παρόν μήνυμα.</p>
            </div>
            """
            
            plain_message = f"Ο κωδικός επιβεβαίωσης για την εγγραφή σας είναι: {otp_code}"

            try:
                mail = mt.Mail(
                    sender=mt.Address(email="hello@turnonlearning.com", name="Turn On Learning"),
                    to=[mt.Address(email=user.email)], # 👈 ΔΙΟΡΘΩΣΗ: user.email χωρίς αγκύλες [ ]
                    bcc=[
                        mt.Address(email="charalampospitris1983@gmail.com"),
                    ],
                    subject=subject,
                    text=plain_message, # 👈 Σημείωση: Στο Mailtrap SDK η παράμετρος λέγεται 'text', όχι 'message'
                    html=html_message,
                    category="Registration OTP",
                )
                
                client = mt.MailtrapClient(token=settings.MAILTRAP_TOKEN)
                client.send(mail)

                messages.info(request, "Σας στάλθηκε ένας 6ψήφιος κωδικός στο email σας.")
                return redirect("accounts:verify_otp")
                
            except Exception as e:
                print(f"❌ MAILTRAP ERROR: {e}") # 👈 Εκτύπωση σφάλματος στο τερματικό
                messages.error(request, f"Αποτυχία αποστολής email. Σφάλμα: {e}")
        else:
            messages.error(request, "Παρακαλούμε διορθώστε τα σφάλματα παρακάτω.")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form, "logo": logo})


# ==========================================
# 3. VERIFY OTP VIEW (Step 2: Check & Activate)
# ==========================================
def verify_otp_view(request):
    """Ελέγχει αν το OTP είναι σωστό, ενεργοποιεί τον χρήστη και τον συνδέει."""
    user_id = request.session.get('pending_user_id')
    saved_otp = request.session.get('register_otp')

    # Προστασία: Αν δεν υπάρχει εκκρεμής συνεδρία, ανακατεύθυνση στην εγγραφή
    if not user_id or not saved_otp:
        messages.error(request, "Μη έγκυρη συνεδρία. Παρακαλούμε εγγραφείτε ξανά.")
        return redirect("accounts:register")

    if request.method == "POST":
        user_otp = request.POST.get("otp_code", "").strip()

        if user_otp == saved_otp:
            # 1. Ενεργοποίηση χρήστη στη βάση
            try:
                user = User.objects.get(id=user_id)
                user.is_active = True
                user.save()

                # 2. Καθαρισμός των μεταβλητών Session
                del request.session['pending_user_id']
                del request.session['register_otp']

                # 3. Αυτόματο Login
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Η εγγραφή και η επαλήθευση ολοκληρώθηκαν με επιτυχία!")
                return redirect("homepage:homepage")
            
            except User.DoesNotExist:
                messages.error(request, "Ο χρήστης δεν βρέθηκε.")
                return redirect("accounts:register")
        else:
            messages.error(request, "Λανθασμένος κωδικός OTP. Παρακαλούμε δοκιμάστε ξανά.")

    return render(request, "accounts/verify_otp.html")


def logout_view(request):
    logout(request)
    return redirect('homepage:homepage')
