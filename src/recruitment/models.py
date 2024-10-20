from datetime import date
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Candidate(models.Model):
    SEX_CHOICES = (
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("I", "Indefinido"),
    )
    BREED_CHOICES = (
        ("Negro", "Negro"),
        ("Pardo", "Pardo"),
        ("Amarelo", "Amarelo"),
        ("Branco", "Branco"),
    )
    phone_regex_validator = RegexValidator(
        regex=r"[1-9]{2} 9[0-9]{4}-[0-9]{4}",
        message="O telefone deve estar no formato: 99 99999-9999",
    )
    name = models.CharField(
        verbose_name="Nome do Candidato",
        name="Nome",
        max_length=100,
        null=False,
        blank=False,
    )
    birthday = models.DateField(
        verbose_name="Data de Nascimento do Candidato",
        name="Data de Nascimento",
        null=False,
        blank=False,
    )
    sex = models.CharField(
        verbose_name="Sexo do Candidato",
        name="Sexo",
        choices=SEX_CHOICES,
        max_length=1,
        null=False,
        blank=False,
    )
    breed = models.CharField(
        verbose_name="Raça do Candidato",
        name="Raça",
        choices=BREED_CHOICES,
        max_length=7,
        null=False,
        blank=False,
    )
    phone = models.CharField(
        verbose_name="Numero de Telefone do Candidato",
        name="Telefone",
        max_length=16,
        null=False,
        blank=False,
        validators=[
            phone_regex_validator,
        ],
    )
    email = models.EmailField(
        verbose_name="Email do Candidato",
        name="Email",
        null=False,
        blank=False,
    )
    url_linkedin = models.URLField(
        verbose_name="Url do Linkedin do Candidato",
        name="Linkedin",
        null=False,
        blank=False,
    )

    # def save(self, *args, **kwargs):
    #     if self.birthday >= date.today():
    #         raise ValidationError(
    #             "A data de nascimento deve ser menor que a data atual"
    #         )
    #     super(Event, self).save(*args, **kwargs)
    def clean(self):
        if self.birthday >= date.today():
            raise ValidationError(
                "A data de nascimento deve ser menor que a data atual"
            )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Candidato"


class ProfessionalExperience(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.CharField(
        verbose_name="Cargo da Experiência",
        name="Cargo",
        max_length=100,
        null=False,
        blank=False,
    )
    company = models.CharField(
        verbose_name="Nome da Empresa da Experiência",
        name="Empresa",
        max_length=100,
        null=False,
        blank=False,
    )
    start_date = models.DateField(
        verbose_name="Data de inicío da Experiência",
        name="Data Inicío",
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        verbose_name="Data de Fim da Experiência",
        name="Data Fim",
        null=True,
        blank=False,
    )
    description = models.TextField(
        verbose_name="Descrição da Experiência",
        name="Descrição",
        null=False,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if self.start_date >= date.today():
            raise ValidationError("A data de início deve ser menor que a data atual")
        if self.end_date is not None:
            if self.end_date >= date.today():
                raise ValidationError("A data de fim deve ser maior que a data atual")
            if self.end_date < self.start_date:
                raise ValidationError(
                    "A data de fim deve ser maior que a data de inicio"
                )
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.position}"

    class Meta:
        verbose_name = "Experiência Profissional"
        verbose_name_plural = "Experiências Profissionais"


class Education(models.Model):

    LEVEL_CHOICES = (
        ("MI", "Médio Incompleto"),
        ("MC", "Médio Completo"),
        ("SI", "Superior Incompleto"),
        ("SC", "Superior Completo"),
    )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    institution = models.CharField(
        verbose_name="Nome da Instituição de Formaçâo",
        name="Instuição",
        max_length=200,
        null=False,
        blank=False,
    )
    level = models.CharField(
        verbose_name="Nível de Escolaridade",
        name="Escolaridade",
        choices=LEVEL_CHOICES,
        max_length=2,
        null=False,
        blank=False,
    )
    course = models.CharField(
        verbose_name="Nome do Curso",
        name="Curso",
        max_length=100,
        null=False,
        blank=False,
    )
    start_date = models.DateField(
        verbose_name="Data Inicio do Curso",
        name="Data Início",
        null=False,
        blank=False,
    )
    end_date = models.DateField(
        verbose_name="Data Fim do Curso",
        name="Data Fim",
        null=True,
        blank=False,
    )

    def save(self, *args, **kwargs):
        if self.start_date >= date.today():
            raise ValidationError("A data de inicio deve ser menor que a data atual")
        if self.end_date is not None:
            if self.end_date >= date.today():
                raise ValidationError("A data de fim deve ser maior que a data atual")
            if self.end_date < self.start_date:
                raise ValidationError(
                    "A data de fim deve ser maior que a data de início"
                )
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.course}"

    class Meta:
        verbose_name = "Escolaridade"
