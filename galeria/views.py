""" Vistas para la aplicación de galería de proyectos fotográficos y videográficos."""
from django.shortcuts import render, get_object_or_404
from .models import Proyecto, Categoria


def inicio(request):
    """ Vista para la página de inicio, mostrando los proyectos destacados """
    # Obtener los proyectos destacados (marcados como destacados en el modelo)
    # y limitar a los 6 más recientes para mostrar en la página de inicio,
    # lo que permite destacar lo mejor del portafolio y atraer a los visitantes a explorar más
    destacados = Proyecto.objects.filter(destacado=True)[:6]
    # Renderizar la plantilla de inicio con los proyectos destacados en el contexto,
    # lo que permite mostrar una selección atractiva de trabajos en la página principal del sitio
    return render(request, 'galeria/inicio.html', {'destacados': destacados})


def lista_proyectos(request):
    """ Vista para la lista de proyectos, con filtrado por tipo y categoría """
    # Obtener todos los proyectos y categorías disponibles
    proyectos = Proyecto.objects.all()
    categorias = Categoria.objects.all()

    # Aplicar filtros por tipo y categoría
    tipo = request.GET.get('tipo')
    categoria_slug = request.GET.get('categoria')

    # Si se ha especificado un tipo, filtrar los proyectos por ese tipo (foto o video)
    if tipo:
        proyectos = proyectos.filter(tipo=tipo)
    if categoria_slug:
        proyectos = proyectos.filter(categoria__slug=categoria_slug)
    # Si se ha especificado una categoría, filtrar los proyectos por esa categoría,
    # utilizando el slug de la categoría para hacer la búsqueda más amigable y legible en la URL
    if request.htmx:
        return render(request, 'galeria/parciales/_grid_proyectos.html', {
            'proyectos': proyectos,
        })

    # Renderizar la plantilla de lista de proyectos con los proyectos filtrados en el contexto
    return render(request, 'galeria/proyectos.html', {
        'proyectos': proyectos,
        'categorias': categorias,
        'tipo_actual': tipo or '',
        'categoria_actual': categoria_slug or '',
    })


def detalle_proyecto(request, slug):
    """ Vista para el detalle de un proyecto específico, identificado por su slug """
    # Obtener el proyecto correspondiente al slug proporcionado, o devolver un error 404 si no se encuentra,
    # lo que permite mostrar una página de detalle para cada proyecto individual,
    # con toda su información y medios asociados, y manejar de manera elegante el caso en que el proyecto no exista
    proyecto = get_object_or_404(Proyecto, slug=slug)

    # Renderizar la plantilla de detalle del proyecto con el proyecto en el contexto,
    # lo que permite mostrar la información del proyecto en un modal si se utiliza HTMX,
    # o en una página completa si se accede directamente, proporcionando una experiencia
    # de usuario fluida y adaptable según el contexto de navegación
    if request.htmx:
        return render(request, 'galeria/parciales/_detalle_modal.html', {
            'proyecto': proyecto,
        })

    # Renderizar la plantilla de detalle del proyecto con el proyecto en el contexto,
    # lo que permite mostrar la información del proyecto en una página completa si se accede directamente,
    # proporcionando una experiencia de usuario fluida y adaptable según el contexto de navegación
    # y asegurando que el proyecto se muestre correctamente tanto en modales como en páginas completas
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



