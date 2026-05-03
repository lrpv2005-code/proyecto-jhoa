from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default="#2563eb")
    icono = models.CharField(max_length=20, default="💰") 

    def __str__(self):
        return self.nombre

class Gasto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='gastos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

class Ingreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    fuente = models.CharField(max_length=100, default="General")

    def __str__(self):
        return f"{self.descripcion} - ${self.monto}"

class Presupuesto(models.Model):
    categoria = models.OneToOneField(Categoria, on_delete=models.CASCADE, related_name='presupuesto')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    limite = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Presupuesto {self.categoria.nombre} - ${self.limite}"