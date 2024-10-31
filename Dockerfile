# Montando o container com base na imagem do python
FROM  python:3.12-alpine
#Copiando o projeto para dentro do container 
COPY ./src /src
COPY ./requirements.txt /
#Instalando as dependencias 
RUN pip install -r requirements.txt
#Definindo o diretorio de trabalho de container 
WORKDIR /src
#Expondo a porta do container
EXPOSE 8000
#Iniciando a aplicação(EntryPoint)
# CMD [ "sh","-c","python3 manage.py migrate && python3 manage.py creatsuperuser --no-input --username $DJANGO_SUPER_USERNAME --email $DJANGO_SUPERUSER_EMAIL python3 manage.py runserver 0.0.0.0:8000" ]
CMD [ "sh","-c","python3 manage.py migrate --noinput && python3 manage.py runserver 0.0.0.0:8000 --noreload" ]