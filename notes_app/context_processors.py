
def current_user(request):
    # print("context_preprocessor",request.user)
    return {"current_user": request.user}
