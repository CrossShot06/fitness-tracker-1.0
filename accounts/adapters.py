from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class DebugGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def get_authorization_url(self, request, app):
        url = super().get_authorization_url(request, app)
        print("GOOGLE REDIRECT URL:", url)  # <-- This will show up in terminal
        return url
