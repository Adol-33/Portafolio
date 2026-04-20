""" Vistas para la aplicación de galería de proyectos fotográficos y videográficos."""
from django.shortcuts import render, get_object_or_404
from .models import Proyecto, Categoria


def inicio(request):
    """ Vista para la página de inicio, mostrando los proyectos destacados """
    destacados = Proyecto.objects.filter(destacado=True)[:6]
    return render(request, 'galeria/inicio.html', {'destacados': destacados})


def lista_proyectos(request):
    """ Vista para la lista de proyectos, con filtrado por tipo y categoría """
    proyectos = Proyecto.objects.all()
    categorias = Categoria.objects.all()

    tipo = request.GET.get('tipo')
    categoria_slug = request.GET.get('categoria')

    if tipo:
        proyectos = proyectos.filter(tipo=tipo)
    if categoria_slug:
        proyectos = proyectos.filter(categoria__slug=categoria_slug)

    if request.htmx:
        return render(request, 'galeria/parciales/_grid_proyectos.html', {
            'proyectos': proyectos,
        })

    return render(request, 'galeria/proyectos.html', {
        'proyectos': proyectos,
        'categorias': categorias,
        'tipo_actual': tipo or '',
        'categoria_actual': categoria_slug or '',
    })


def detalle_proyecto(request, slug):
    """ Vista para el detalle de un proyecto específico, identificado por su slug """
    proyecto = get_object_or_404(Proyecto, slug=slug)

    if request.htmx:
        return render(request, 'galeria/parciales/_detalle_modal.html', {
            'proyecto': proyecto,
        })

    return render(request, 'galeria/detalle.html', {'proyecto': proyecto})


def sobre_mi(request):
    """ Vista para la página 'Sobre mí' """

    return render(request, 'galeria/sobre_mi.html')


def contacto(request):
    """ Vista para la página de contacto, con un formulario simple """
    if request.method == 'POST':
        # Aquí puedes procesar el formulario de contacto
        if request.htmx:
            return render(request, 'galeria/parciales/_contacto_exito.html')
    return render(request, 'galeria/contacto.html')



