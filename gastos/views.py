from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from .models import Categoria, Gasto, Ingreso, Presupuesto
from .forms import CategoriaForm, GastoForm, IngresoForm, PresupuestoForm

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'landing.html')

@login_required
def pagina_principal(request):
    user = request.user
    ahora = timezone.now()
    
    if not Categoria.objects.filter(usuario=user).exists():
        defaults = [("Internet", "#3b82f6"), ("Comida", "#f59e0b"), ("Saldo", "#8b5cf6")]
        for nom, col in defaults:
            Categoria.objects.create(nombre=nom, usuario=user, color=col, icono=" ")
    
    total_mes_gastos = Gasto.objects.filter(
        usuario=user, 
        fecha__year=ahora.year, 
        fecha__month=ahora.month
    ).aggregate(Sum('monto'))['monto__sum'] or 0
    
    total_mes_ingresos = Ingreso.objects.filter(
        usuario=user, 
        fecha__year=ahora.year, 
        fecha__month=ahora.month
    ).aggregate(Sum('monto'))['monto__sum'] or 0
    
    balance = float(total_mes_ingresos) - float(total_mes_gastos)
    
    categorias = Categoria.objects.filter(usuario=user)
    
    return render(request, 'home.html', {
        'total_mes_gastos': total_mes_gastos,
        'total_mes_ingresos': total_mes_ingresos,
        'balance': balance,
        'categorias': categorias,
        'mes_actual': ahora.strftime('%B')
    })

@login_required
def nueva_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.icono = " "
            categoria.save()
            return redirect('home')
    else:
        form = CategoriaForm(initial={'color': '#2563eb'})
        
    return render(request, 'nueva_categoria.html', {'form': form})

@login_required
def nuevo_ingreso(request):
    if request.method == 'POST':
        form = IngresoForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario = request.user
            ingreso.save()
            return redirect('home')
    else:
        form = IngresoForm()
    return render(request, 'nuevo_ingreso.html', {'form': form, 'titulo': 'Añadir Ingreso'})

@login_required
def detalle_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.categoria = categoria
            gasto.usuario = request.user
            gasto.save()
            return redirect('detalle_categoria', categoria_id=categoria.id)
    else:
        form = GastoForm()
        
    gastos = categoria.gastos.all().order_by('-fecha')
    
    return render(request, 'detalle_categoria.html', {
        'categoria': categoria,
        'form': form,
        'gastos': gastos
    })

def login_personalizado(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'registro.html', {'form': form})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('login')
