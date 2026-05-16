from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from .models import Categoria, Gasto, Ingreso, Presupuesto
from .forms import CategoriaForm, GastoForm, IngresoForm, PresupuestoForm

SVG_ICONS = {
    'shopping-cart': '<circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>',
    'home': '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline>',
    'car': '<rect width="16" height="6" x="4" y="9" rx="2"></rect><path d="M3 10V6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v4"></path><path d="M14 9V5"></path><path d="M10 9V5"></path><circle cx="7" cy="17" r="2"></circle><circle cx="17" cy="17" r="2"></circle>',
    'coffee': '<path d="M17 8h1a4 4 0 1 1 0 8h-1"></path><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"></path><line x1="6" y1="2" x2="6" y2="4"></line><line x1="10" y1="2" x2="10" y2="4"></line><line x1="14" y1="2" x2="14" y2="4"></line>',
    'gift': '<polyline points="20 12 20 22 4 22 4 12"></polyline><rect width="20" height="5" x="2" y="7"></rect><line x1="12" y1="22" x2="12" y2="7"></line><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"></path><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"></path>',
    'trending-up': '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>',
    'tool': '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path>',
    'music': '<path d="M9 18V5l12-2v13"></path><circle cx="6" cy="18" r="3"></circle><circle cx="18" cy="16" r="3"></circle>',
    'dollar-sign': '<line x1="12" y1="1" x2="12" y2="23"></line><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>',
    'heart': '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"></path>',
    'phone': '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"></rect><path d="M12 18h.01"></path>',
    'shirt': '<path d="M20.38 3.46 16 2a4 4 0 0 1-8 0L3.62 3.46a2 2 0 0 0-1.62 1.96v4.42a2 2 0 0 0 .39 1.16l2.23 3.1a2 2 0 0 1 .38 1.16V20a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5.89a2 2 0 0 1 .38-1.16l2.23-3.1a2 2 0 0 0 .39-1.16V5.42a2 2 0 0 0-1.62-1.96z"></path>',
    'gamepad': '<line x1="6" y1="12" x2="10" y2="12"></line><line x1="8" y1="10" x2="8" y2="14"></line><circle cx="15" cy="13" r="1"></circle><circle cx="18" cy="11" r="1"></circle><path d="M15 6a5 5 0 0 0-3 1.35A5 5 0 0 0 9 6H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-5z"></path>',
    'popcorn': '<path d="M18 8a2 2 0 0 0 0-4 2 2 0 0 0-4 0 2 2 0 0 0-4 0 2 2 0 0 0-4 0 2 2 0 0 0 0 4"></path><path d="M10 22 9 8h6l-1 14Z"></path><path d="M20 8c.5 0 .9.4.8.9l-2.4 12.2c-.1.5-.6.9-1.1.9h-10.6c-.5 0-1-.4-1.1-.9L3.2 8.9c-.1-.5.3-.9.8-.9h16Z"></path>',
    'drumstick': '<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"></path><path d="M7 2v4"></path><path d="M21 15V2v0a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"></path><line x1="9" y1="11" x2="9" y2="22"></line>'
}

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
            Categoria.objects.create(nombre=nom, usuario=user, color=col, icono="dollar-sign")
    
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
    
    meses = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }
    mes_actual = meses[ahora.month]
    
    # Datos para gráficos
    chart_data_pie = []
    for cat in categorias:
        total_cat = Gasto.objects.filter(
            categoria=cat,
            fecha__year=ahora.year,
            fecha__month=ahora.month
        ).aggregate(Sum('monto'))['monto__sum'] or 0
        if total_cat > 0:
            chart_data_pie.append({
                'nombre': cat.nombre,
                'monto': float(total_cat),
                'color': cat.color
            })

    return render(request, 'home.html', {
        'total_mes_gastos': float(total_mes_gastos),
        'total_mes_ingresos': float(total_mes_ingresos),
        'balance': balance,
        'categorias': categorias,
        'mes_actual': mes_actual,
        'chart_data_pie': chart_data_pie,
        'icons': SVG_ICONS,
        'icon_keys': list(SVG_ICONS.keys()),
    })

@login_required
def nueva_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            return redirect('home')
    else:
        form = CategoriaForm(initial={'color': '#2563eb'})
        
    return render(request, 'nueva_categoria.html', {
        'form': form, 
        'icons': SVG_ICONS,
        'icon_keys': list(SVG_ICONS.keys())
    })

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
        'gastos': gastos,
        'icons': SVG_ICONS,
        'icon_keys': list(SVG_ICONS.keys())
    })

@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('detalle_categoria', categoria_id=categoria.id)
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'nueva_categoria.html', {
        'form': form, 
        'icons': SVG_ICONS, 
        'titulo': f'Editar {categoria.nombre}',
        'es_edicion': True
    })

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id, usuario=request.user)
    categoria.delete()
    return redirect('home')

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
