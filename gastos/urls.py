from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.pagina_principal, name='home'),
    path('registro/', views.registro_usuario, name='registro'),
    path('accounts/login/', views.login_personalizado, name='login'),
    path('salir/', views.cerrar_sesion, name='salir'),
    path('nueva-categoria/', views.nueva_categoria, name='nueva_categoria'),
    path('nuevo-ingreso/', views.nuevo_ingreso, name='nuevo_ingreso'),
    path('modulo/<int:categoria_id>/', views.detalle_categoria, name='detalle_categoria'),
    path('editar-categoria/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('eliminar-categoria/<int:categoria_id>/', views.eliminar_categoria, name='eliminar_categoria'),
]
