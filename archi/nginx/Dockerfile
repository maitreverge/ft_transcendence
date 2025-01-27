FROM nginx:alpine

# Supprimez la configuration par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Copiez les fichiers de configuration
COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

# Vérifiez la configuration lors de la construction de l'image
RUN nginx -t

CMD ["nginx", "-g", "daemon off;"]
