from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, User
from django.forms import model_to_dict
from djongo import models


class MicroContentProgress(models.Model):
    #MOD: falla al crear el id (clave duplicada). Django la crea por defecto correctamente
    #Modificado por MK. Cambio o atributo id por micro_id e quitolle o de Primary Key.
    micro_id = models.IntegerField(default=0) 
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    mark = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def to_dict(self):
        micro_content_dict = model_to_dict(self, fields=['micro_id', 'title', 'completed', 'mark'])
        return micro_content_dict


class UnitProgress(models.Model):
    #MOD: falla al crear el id (clave duplicada). Django la crea por defecto correctamente
    #Modificado por MK. Idem que en el anterior
    unit_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    micro_contents = models.ArrayModelField(
        model_container=MicroContentProgress
    )

    def __str__(self):
        return self.name

    def to_dict(self):
        unit_dict = model_to_dict(self, fields=['unit_id', 'name', 'completed'])
        unit_dict["micro_contents"] = []
        for micro_content in self.micro_contents:
            unit_dict['micro_contents'].append(micro_content.to_dict())
        return unit_dict


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    telegram_id = models.CharField(max_length=1000)
    alexa_id = models.CharField(max_length=1000)
    moodle_id = models.CharField(max_length=1000)
    birth_date = models.CharField(max_length=50, default='01/01/1901')
    faculty = models.CharField(max_length=1000, default='student')
    progress = models.ArrayModelField(
        model_container=UnitProgress,
        default="-"
    )

    def __str__(self):
        return self.user.username

    def to_dict(self):
        student_dict = model_to_dict(self, fields=['telegram_id', 'alexa_id', 'moodle_id', 'birth_date'])
        student_dict['progress'] = []
        for unit in self.progress:
            student_dict['progress'].append(unit.to_dict())
        return student_dict
