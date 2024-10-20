# Generated by Django 5.1.2 on 2024-10-20 18:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome do Candidato')),
                ('birthday', models.DateField(verbose_name='Data de Nascimento do Candidato')),
                ('sex', models.CharField(choices=[('F', 'Feminino'), ('M', 'Masculino'), ('I', 'Indefinido')], max_length=1, verbose_name='Sexo do Candidato')),
                ('breed', models.CharField(choices=[('Negro', 'Negro'), ('Pardo', 'Pardo'), ('Amarelo', 'Amarelo'), ('Branco', 'Branco')], max_length=7, verbose_name='Raça do Candidato')),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message='O telefone deve estar no formato: 99 99999-9999', regex='[1-9]{2} 9[0-9]{4}-[0-9]{4}')], verbose_name='Numero de Telefone do Candidato')),
                ('email', models.EmailField(max_length=254, verbose_name='Email do Candidato')),
                ('url_linkedin', models.URLField(verbose_name='Url do Linkedin do Candidato')),
            ],
            options={
                'verbose_name': 'Candidato',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200, verbose_name='Nome da Instituição de Formaçâo')),
                ('level', models.CharField(choices=[('MI', 'Médio Incompleto'), ('MC', 'Médio Completo'), ('SI', 'Superior Incompleto'), ('SC', 'Superior Completo')], max_length=2, verbose_name='Nível de Escolaridade')),
                ('course', models.CharField(max_length=100, verbose_name='Nome do Curso')),
                ('start_date', models.DateField(verbose_name='Data Inicio do Curso')),
                ('end_date', models.DateField(null=True, verbose_name='Data Fim do Curso')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate')),
            ],
            options={
                'verbose_name': 'Escolaridade',
            },
        ),
        migrations.CreateModel(
            name='ProfessionalExperience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=100, verbose_name='Cargo da Experiência')),
                ('company', models.CharField(max_length=100, verbose_name='Nome da Empresa da Experiência')),
                ('start_date', models.DateField(verbose_name='Data de inicío da Experiência')),
                ('end_date', models.DateField(null=True, verbose_name='Data de Fim da Experiência')),
                ('description', models.TextField(verbose_name='Descrição da Experiência')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruitment.candidate')),
            ],
            options={
                'verbose_name': 'Experiência Profissional',
                'verbose_name_plural': 'Experiências Profissionais',
            },
        ),
    ]
