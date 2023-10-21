from django.views import View
from django.http import HttpResponse
import os
from .upload_video import upload, CATEGORY  # Assurez-vous d'importer la fonction upload appropriée

class UploadVideoView(View):
    template_name = "upload_video.html"  # Créez un modèle pour le formulaire d'upload

    def post(self, request):
        # Récupérez les données du formulaire (assurez-vous d'avoir un formulaire approprié dans votre modèle)
        videopath = request.FILES['videofile']  # Assurez-vous que le formulaire a un champ de fichier nommé 'videofile'
        title = request.POST['title']
        description = request.POST['description']
        category = request.POST['category']
        keywords = request.POST['keywords']
        date = request.POST['date']

        # Traitez les données comme nécessaire (par exemple, sauvegardez le fichier vidéo sur le serveur)

        # Utilisez la fonction upload pour télécharger la vidéo
        upload(
            videopath=videopath,
            title=title,
            description=description,
            category=CATEGORY[category],  # Assurez-vous que CATEGORY est défini correctement
            keywords=keywords,
            n_privacy_statuses=1,
            miniature_path="",
            kids=True,
            notif=True,
            date=date
        )

        return HttpResponse("Video uploaded successfully")
