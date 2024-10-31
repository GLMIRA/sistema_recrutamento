# Projeto de uma Empresa de Recrutamento

## Descrição
Esse sistema foi desenvolvido como parte de um desafio técnico para uma vaga de estágio.

O projeto consiste na criação de um sistema de cadastramento de currículos
 para uma empresa de recrutamento e seleção de candidatos. 
 Nele, o usuário pode criar seu currículo com dados pessoais
e suas experiências profissionais.

## Pré-requisitos
- Python 
- Django 
- SQLite3
- Django REST Framework (DRF)
- DRF Nested Routers
- Docker 


-------------------------------------
## Instalação

```bash
# Clone o repositório 
git clone https://github.com/GLMIRA/sistema_recrutamento.git 

# Navegue até o repositório 
cd sistema_recrutamento

# Instale as dependências 
pip install -r requirements.txt
```


-----------------------------
## Executar o projeto 
```Bash
cd src # Entrando no diretório onde está o manage.py

python3 manage.py migrate # Criando as tabelas no banco de dados

python3 manage.py createsuperuser # Comando para criar o superusuário 

python3 manage.py runserver # Iniciando o servidor

```
> Para mais informações sobre os comandos acima, consulte a [documentção do Django](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)


----------------------------

## Manual da interfaçe Grafica
Para o manual da [interface grafica](./INTRFACE.md) 

## Execute com o Docker
Para saber como executar o Docker, veja o [manual do Docker](./DOCKER.md) deste projeto.

## Manual das Api's
Para o manual da [api](./API.md)