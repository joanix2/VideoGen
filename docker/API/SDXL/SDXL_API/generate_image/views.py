from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from .models import ImageModel
from .imgGenAgent import SDXLAgent  # Assurez-vous de l'importer correctement
from PIL import Image
from django.conf import settings
import os

class ImgGenView(APIView):  # Assurez-vous d'importer APIView depuis rest_framework ou le module approprié
    def __init__(self):
        super().__init__()  # Assurez-vous d'appeler le constructeur de la classe parent

        # Créez une instance de SDXLAgent
        self.sdxl_agent = SDXLAgent()

    def post(self, request):
        name = request.data.get('name')
        prompt = request.data.get('prompt')
        height = request.data.get('height', 720)
        width = request.data.get('width', 1280)
        refine = request.data.get('refine', True)

        if prompt is not None:
            if name is None:
                name = prompt
            image_data = self.sdxl_agent.get_image(prompt=prompt, height=height, width=width, refine=refine)

            # Créez le répertoire cible s'il n'existe pas
            image_dir = os.path.join(settings.MEDIA_ROOT, "images")
            os.makedirs(image_dir, exist_ok=True)

            # Créez le chemin complet pour le fichier image
            image_path = os.path.join(image_dir, f"{name}.png")

            # Sauvegardez l'image dans le fichier
            image_data.save(image_path)

            # Créez une entrée dans la base de données
            image = ImageModel.objects.create(name=name, image_file=os.path.join("images", f"{name}.png"))

            return JsonResponse({'image_url': image.image_file.url})
        else:
            return JsonResponse({'error': 'no prompt'}, status=status.HTTP_400_BAD_REQUEST)

