from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, NoteModel
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

# -------------------- HELPER: JWT AUTH --------------------
def get_authenticated_user(request):
    access_token = request.COOKIES.get("access_token")
    if not access_token:
        return None
    jwt_auth = JWTAuthentication()
    try:
        validated_token = jwt_auth.get_validated_token(access_token)
        user = jwt_auth.get_user(validated_token)
        return user
    except Exception:
        return None

def jwt_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = get_authenticated_user(request)
        if not user:
            return redirect("signin")
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper

# -------------------- SIGNUP --------------------
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(user_email=email).exists():
            messages.error(request, "Email already exists")
        else:
            User.objects.create_user(user_name=username, user_email=email, password=password)
            messages.success(request, "User created successfully")
            return redirect("signin")
    return render(request, "notes_app/signup.html")

# -------------------- SIGNIN --------------------
def signin_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.objects.filter(user_email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            response = redirect("home")
            response.set_cookie(
                key="access_token",
                value=str(refresh.access_token),
                httponly=True,
                secure=False,  # True in production
                samesite="Lax"
            )
            response.set_cookie(
                key="refresh_token",
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite="Lax"
            )
            return response
        messages.error(request, "Invalid credentials")
    return render(request, "notes_app/signin.html")

# -------------------- LOGOUT --------------------
def signout_view(request):
    response = redirect("signin")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

# -------------------- HOME & ACCOUNT --------------------
@jwt_required
def account_view(request):
    return render(request, "notes_app/account.html", {"user": request.user})


@jwt_required
def home_view(request):
    notes = NoteModel.objects.filter(user=request.user).order_by("-last_update")
    return render(request, "notes_app/home.html", {"notes": notes})

# -------------------- CREATE --------------------
@jwt_required
def create_note_view(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        NoteModel.objects.create(note_title=title, note_content=content, user=request.user)
        return redirect("home")
    return render(request, "notes_app/create_note.html")

# -------------------- EDIT --------------------
@jwt_required
def edit_note_view(request, note_id):
    try:
        note = NoteModel.objects.get(note_id=note_id, user=request.user)
    except NoteModel.DoesNotExist:
        messages.error(request, "Note not found")
        return redirect("home")

    if request.method == "POST":
        note.note_title = request.POST.get("title", note.note_title)
        note.note_content = request.POST.get("content", note.note_content)
        note.save()
        return redirect("home")

    return render(request, "notes_app/edit_note.html", {"note": note})

# -------------------- DELETE --------------------
@jwt_required
def delete_note_view(request, note_id):
    try:
        note = NoteModel.objects.get(note_id=note_id, user=request.user)
        note.delete()
    except NoteModel.DoesNotExist:
        messages.error(request, "Note not found")
    return redirect("home")
