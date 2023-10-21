docker rm -f $(docker ps -aq) # tout supprimer
docker rmi $(docker images -q) # supprimer toutes les images
docker system prune # Vous pouvez également ajouter l'option -a pour supprimer également les images non utilisées

