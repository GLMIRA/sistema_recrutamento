# sistema_recrutamento
Sistema de recrutamento para uma empresa 

candidato/<int:id_candidato>/experiencia/<id_experiencia> --> detalhe de experiencia
candidato/<int:id_candidato>/experiencia/ --> lista de experiencias
candidato/<int:id_candidato>/experiencia/criar/ --> criar experiencia




## Executando o conteiner

> ***Pré requisitos***: Ter o Docker instalado. para instlação acesse a [documentação do docker](https://www.docker.com/)

Para rodar a aplicação siga o seguinte passo a passo:

1. Clone este projeto:

```bash
git clone https://github.com/GLMIRA/sistema_recrutamento.git
```

2. Acesse a pasta do projeto:

```bash
cd sistema_recrutamento
```

3. Buildar a imagem do container:

```bash
docker build -t {{nome da imagem}} . # subistitua {{nome da imagem}} por um nome de sua preferência
```

4. Rode o container:

```bash
docker run --name {{nome do conteiner}} -p 8000:8000 {{nome da imagem}} # subistitua {{nome da imagem}} pelo nome utilizado no passo 3
```

5. Crie seu superuser:

```bash
docker exec -it {{nome do conteiner}} /bin/sh # acessando o shell do conteiner
python manage.py createsuperuser #Criando superuser
```

6. Acesse a aplicação no browser de sua preferência pelo endereço `http://localhost:8000`