# Vistas para cargar y mostrar evaluaciones
import json
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
      Paciente, Estudio, Diagnostico, Sintoma, 
      Comorbilidad, Informe, Medicacion, Normativa, Resultado
)    
from .forms import (
     PacienteForm, EstudioForm, DiagnosticoForm, SintomaForm,
     ComorbilidadForm, InformeForm, MedicacionForm, NormativaForm, ResultadoForm, BuscarPacienteForm, RelacionesForm
)

def index(request):
    return render(request, 'app/index.html')
    
    
def listar_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'app/listar_pacientes.html', {'pacientes': pacientes})

def agregar_diagnostico(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST)
        if form.is_valid():
            diagnostico = form.save(commit=False)
            diagnostico.paciente = paciente
            diagnostico.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = DiagnosticoForm()
    return render(request, 'app/agregar_diagnostico.html', {'form': form, 'paciente': paciente})
    

def agregar_sintoma(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = SintomaForm(request.POST)
        if form.is_valid():
            sintoma = form.save(commit=False)
            sintoma.paciente = paciente
            sintoma.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = SintomaForm()
    return render(request, 'app/agregar_sintoma.html', {'form': form, 'paciente': paciente})

def listar_normativas(request):
    normativas = Normativa.objects.all().order_by('estudio', 'sexo', 'edad_min')
    return render(request, 'app/listar_normativas.html', {'normativas': normativas})

def agregar_normativa(request):
    if request.method == 'POST':
        form = NormativaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Normativa agregada correctamente.")
            return redirect('app:listar_normativas')
    else:
        form = NormativaForm()
    return render(request, 'app/agregar_normativa.html', {'form': form})

def editar_normativa(request, normativa_id):
    normativa = get_object_or_404(Normativa, id=normativa_id)
    if request.method == 'POST':
        form = NormativaForm(request.POST, instance=normativa)
        if form.is_valid():
            form.save()
            messages.success(request, "Normativa actualizada correctamente.")
            return redirect('app:listar_normativas')
    else:
        form = NormativaForm(instance=normativa)
    return render(request, 'app/editar_normativa.html', {'form': form, 'normativa': normativa})

def agregar_comorbilidad(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = ComorbilidadForm(request.POST)
        if form.is_valid():
            comorbilidad = form.save(commit=False)
            comorbilidad.paciente = paciente
            comorbilidad.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = ComorbilidadForm()
    return render(request, 'app/agregar_comorbilidad.html', {'form': form, 'paciente': paciente})

def cargar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm()
    return render(request, 'app/cargar_paciente.html', {'form': form})


def detalle_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    diagnosticos = Diagnostico.objects.filter(paciente=paciente)
    sintomas = Sintoma.objects.filter(paciente=paciente)
    comorbilidades = Comorbilidad.objects.filter(paciente=paciente)
    informes = Informe.objects.filter(paciente=paciente)
    medicaciones = Medicacion.objects.filter(paciente=paciente)
    resultados = Resultado.objects.filter(paciente=paciente)
    hijos = list(paciente.hijos_padre.all()) + list(paciente.hijos_madre.all())

    return render(request, 'app/detalle_paciente.html', {
        'paciente': paciente,
        'diagnosticos': diagnosticos,
        'sintomas': sintomas,
        'comorbilidades': comorbilidades,
        'informes': informes,
        'medicaciones': medicaciones,
        'resultados': resultados,
        'padre': paciente.padre,
        'madre': paciente.madre,
        'conyuge': paciente.conyuge,
        'hijos': hijos,
    })


def agregar_informe(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.paciente = paciente
            informe.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = InformeForm()

    return render(request, 'app/agregar_informe.html', {'form': form, 'paciente': paciente})


def agregar_medicacion(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    if request.method == 'POST':
        form = MedicacionForm(request.POST)
        if form.is_valid():
            medicacion = form.save(commit=False)
            medicacion.paciente = paciente
            medicacion.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = MedicacionForm()

    return render(request, 'app/agregar_medicacion.html', {'form': form, 'paciente': paciente})

 
def editar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'app/editar_paciente.html', {'form': form, 'paciente': paciente})

def eliminar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        paciente.delete()
        return redirect('app:listar_pacientes')
    return render(request, 'app/eliminar_paciente.html', {'paciente': paciente})
    
# diagnostico
def editar_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    if request.method == 'POST':
        form = DiagnosticoForm(request.POST, instance=diagnostico)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=diagnostico.paciente.id)
    else:
        form = DiagnosticoForm(instance=diagnostico)
    return render(request, 'app/editar_diagnostico.html', {'form': form, 'paciente': diagnostico.paciente})

def eliminar_diagnostico(request, diagnostico_id):
    diagnostico = get_object_or_404(Diagnostico, id=diagnostico_id)
    paciente_id = diagnostico.paciente.id
    if request.method == 'POST':
        diagnostico.delete()
        return redirect('app:detalle_paciente', paciente_id=paciente_id)
    return render(request, 'app/eliminar_confirmar.html', {
        'objeto': diagnostico, 'tipo': 'Diagnóstico', 'volver': 'app:detalle_paciente', 'paciente_id': paciente_id
    })

# ediciones sintomas
def editar_sintomas(request, sintomas_id):
    sintomas = get_object_or_404(Sintomas, id=sintomas_id)
    if request.method == 'POST':
        form = SintomasForm(request.POST, instance=sintomas)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=sintomas.paciente.id)
    else:
        form = SintomasForm(instance=sintomas)
    return render(request, 'app/editar_sintomas.html', {'form': form, 'paciente': sintomas.paciente})

def eliminar_sintomas(request, sintomas_id):
    sintomas = get_object_or_404(Sintomas, id=sintomas_id)
    paciente_id = sintomas.paciente.id
    if request.method == 'POST':
        sintomas.delete()
        return redirect('app:detalle_paciente', paciente_id=paciente_id)
    return render(request, 'app/eliminar_confirmar.html', {
        'objeto': sintomas, 'tipo': 'Sintomas', 'volver': 'app:detalle_paciente', 'paciente_id': paciente_id
    })

# ediciones Comorbilidad
def editar_comorbilidad(request, comorbilidad_id):
    comorbilidad = get_object_or_404(Comorbilidad, id=comorbilidad_id)
    if request.method == 'POST':
        form = ComorbilidadForm(request.POST, instance=comorbilidad)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=comorbilidad.paciente.id)
    else:
        form = ComorbilidadForm(instance=comorbilidad)
    return render(request, 'app/editar_comorbilidad.html', {'form': form, 'paciente': comorbilidad.paciente})

def eliminar_comorbilidad(request, comorbilidad_id):
    comorbilidad = get_object_or_404(Comorbilidad, id=comorbilidad_id)
    paciente_id = comorbilidad.paciente.id
    if request.method == 'POST':
        comorbilidad.delete()
        return redirect('app:detalle_paciente', paciente_id=paciente_id)
    return render(request, 'app/eliminar_confirmar.html', {
        'objeto': comorbilidad, 'tipo': 'Comorbilidad', 'volver': 'app:detalle_paciente', 'paciente_id': paciente_id
    })

# ediciones informe
def editar_informe(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    if request.method == 'POST':
        form = InformeForm(request.POST, instance=informe)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=informe.paciente.id)
    else:
        form = InformeForm(instance=informe)
    return render(request, 'app/editar_informe.html', {'form': form, 'paciente': informe.paciente})

def eliminar_informe(request, informe_id):
    informe = get_object_or_404(Informe, id=informe_id)
    paciente_id = informe.paciente.id
    if request.method == 'POST':
        informe.delete()
        return redirect('app:detalle_paciente', paciente_id=paciente_id)
    return render(request, 'app/eliminar_confirmar.html', {
        'objeto': informe, 'tipo': 'Informe', 'volver': 'app:detalle_paciente', 'paciente_id': paciente_id
    })

# ediciones medicacion
def editar_medicacion(request, medicacion_id):
    medicacion = get_object_or_404(Medicacion, id=medicacion_id)
    if request.method == 'POST':
        form = MedicacionForm(request.POST, instance=medicacion)
        if form.is_valid():
            form.save()
            return redirect('app:detalle_paciente', paciente_id=medicacion.paciente.id)
    else:
        form = MedicacionForm(instance=medicacion)
    return render(request, 'app/editar_medicacion.html', {'form': form, 'paciente': medicacion.paciente})

def eliminar_medicacion(request, medicacion_id):
    medicacion = get_object_or_404(Medicacion, id=medicacion_id)
    paciente_id = medicacion.paciente.id
    if request.method == 'POST':
        medicacion.delete()
        return redirect('app:detalle_paciente', paciente_id=paciente_id)
    return render(request, 'app/eliminar_confirmar.html', {
        'objeto': medicacion, 'tipo': 'Medicacion', 'volver': 'app:detalle_paciente', 'paciente_id': paciente_id
    })


def agregar_resultado(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    resultados = Resultado.objects.filter(paciente=paciente).order_by('-fecha')  # opcional: ordenar por fecha                                                                                                          

    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        if form.is_valid():
            estudio = form.cleaned_data['estudio']
            puntaje_bruto = form.cleaned_data['puntaje_bruto']

            # Verificar si ya existe resultado para ese estudio
            resultado_existente = Resultado.objects.filter(paciente=paciente, estudio=estudio).first()

            if resultado_existente:
                messages.warning(request, "Ya existe un resultado para este estudio. Se actualizará el valor.")

                resultado = resultado_existente
                resultado.puntaje_bruto = puntaje_bruto
            else:
                resultado = form.save(commit=False)
                resultado.paciente = paciente

            # Buscar normativa
            normativa = Normativa.objects.filter(
                estudio=resultado.estudio,
                sexo=paciente.sexo,
                edad_min__lte=paciente.edad(),
                edad_max__gte=paciente.edad(),
                anios_estudio_min__lte=paciente.años_educacion,
                anios_estudio_max__gte=paciente.años_educacion
            ).first()

            if normativa:
                resultado.media = normativa.media
                resultado.desviacion = normativa.desviacion
                resultado.puntuacion_z = round((resultado.puntaje_bruto - normativa.media) / normativa.desviacion, 2)
                resultado.save()

                messages.success(request, "✅ Resultado guardado correctamente.")
                return redirect('app:agregar_resultado', paciente_id=paciente.id)
            else:
                messages.error(request, "❌ No se encontró normativa adecuada para este estudio.")
    else:
        form = ResultadoForm()

    return render(request, 'app/agregar_resultado.html', {
        'form': form,
        'paciente': paciente,
        'resultados': resultados
    })
    

def cargar_resultado(request):
    if request.method == 'POST':
        form = ResultadoForm(request.POST)
        if form.is_valid():
            resultado = form.save(commit=False)
            normativa = Normativa.objects.filter(
                estudio=resultado.estudio,
                sexo=resultado.paciente.sexo,
                edad_min__lte=resultado.paciente.edad(),
                edad_max__gte=resultado.paciente.edad(),
            )
            if resultado.estudio.depende_educacion:
                normativa = normativa.filter(
                    educacion_min__lte=resultado.paciente.anios_estudio,
                    educacion_max__gte=resultado.paciente.anios_estudio
                )
            normativa = normativa.first()
            if normativa:
                resultado.media = normativa.media
                resultado.desviacion = normativa.desviacion
            resultado.save()
            return redirect('app:detalle_paciente', paciente_id=resultado.paciente.id)
    else:
        form = ResultadoForm()
    return render(request, 'app/cargar_resultado.html', {'form': form})
    
def calcular_z_y_guardar(paciente_id, estudio_id, puntaje_bruto):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    estudio = get_object_or_404(Estudio, id=estudio_id)

    # Buscar la normativa correspondiente
    normativa = Normativa.objects.filter(
        estudio=estudio,
        sexo=paciente.sexo,
        edad_min__lte=paciente.edad(),
        edad_max__gte=paciente.edad(),
        educacion_min__lte=paciente.anios_estudio,
        educacion_max__gte=paciente.anios_estudio,
    ).first()

    if not normativa:
        raise ValueError("No se encontró normativa para este paciente")

    # Calcular puntuación Z
    z = round((puntaje_bruto - normativa.media) / normativa.desviacion, 2)

    # Guardar resultado
    resultado = Resultado.objects.create(
        paciente=paciente,
        estudio=estudio,
        puntaje_bruto=puntaje_bruto,
        media=normativa.media,
        desviacion=normativa.desviacion,
        puntuacion_z=z,
    )

    return resultado
    
def interpretar_desempeno(z):
    if z <= -2.5:
        return "Muy Bajo"
    elif z <= -1.5:
        return "Bajo"
    elif -1.5 < z < 1.5:
        return "Normal"
    elif z >= 2.5:
        return "Muy Alto"
    else:
        return "Levemente Superior o Inferior"


def determinar_normativa(estudio, sexo, edad, educacion):
    return Normativa.objects.filter(
        estudio=estudio,
        sexo=sexo,
        edad_min__lte=edad,
        edad_max__gte=edad,
        anios_estudio_min__lte=educacion,
        anios_estudio_max__gte=educacion
    ).first()


def arbol_genealogico2(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    def serializar(p):
        if not p:
            return None
        return {
            "id": p.id,
            "nombre": str(p),
            "padre": serializar(p.padre),
            "madre": serializar(p.madre),
            "conyuge": serializar(p.conyuge),
            "hijos": [
                {"id": h.id, "nombre": str(h)} for h in
                list(p.hijos_padre.all()) + list(p.hijos_madre.all())
            ]
        }

    datos = serializar(paciente)
    return render(request, 'app/arbol_genealogico2.html', {'paciente': paciente, 'datos': datos})


def arbol_genealogico(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)

    padre = paciente.padre
    madre = paciente.madre
    conyuge = paciente.conyuge

    hijos = Paciente.objects.filter(padre=paciente) | Paciente.objects.filter(madre=paciente)

    hermanos_q = Q()
    if paciente.padre:
        hermanos_q |= Q(padre=paciente.padre)
    if paciente.madre:
        hermanos_q |= Q(madre=paciente.madre)

    hermanos = Paciente.objects.filter(hermanos_q).exclude(id=paciente.id).distinct()

    contexto = {
        'paciente': paciente,
        'padre': padre,
        'madre': madre,
        'conyuge': conyuge,
        'hijos': hijos,
        'hermanos': hermanos,
    }
    return render(request, 'app/arbol_genealogico.html', contexto)
    

def cargar_estudios_json(request):
    if request.method == 'POST' and request.FILES['archivo_json']:
        archivo = request.FILES['archivo_json']
        datos = json.load(archivo)

        for item in datos:
            dni = item.get('dni')
            estudio_nombre = item.get('estudio')
            puntaje_bruto = item.get('puntaje_bruto')

            paciente = get_object_or_404(Paciente, dni=dni)
            estudio = get_object_or_404(Estudio, nombre=estudio_nombre)

            normativa = determinar_normativa(estudio, paciente.sexo, paciente.edad(), paciente.anios_estudio)

            if not normativa:
                messages.warning(request, f"No se encontró normativa para el estudio '{estudio_nombre}' del paciente {paciente.dni}")
                continue

            z = calcular_z(puntaje_bruto, normativa.media, normativa.desviacion)

            Resultado.objects.create(
                paciente=paciente,
                estudio=estudio,
                puntaje_bruto=puntaje_bruto,
                media=normativa.media,
                desviacion=normativa.desviacion,
                puntuacion_z=z
            )

        messages.success(request, "Datos cargados correctamente.")
        return redirect('app:index')

    return render(request, 'app/cargar_estudios_json.html')
    
def buscar_paciente(request):
    paciente = None
    if request.method == 'POST':
        form = BuscarPacienteForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            try:
                paciente = Paciente.objects.get(dni=dni)
               # return redirect('app:detalle_paciente', paciente_id=paciente.id)
            except Paciente.DoesNotExist:
                messages.error(request, "No se encontró un paciente con ese DNI.")
    else:
        form = BuscarPacienteForm()
    return render(request, 'app/buscar_paciente.html', {'form': form, 'paciente': paciente})


def editar_resultado(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id)
    paciente = resultado.paciente

    if request.method == 'POST':
        form = ResultadoForm(request.POST, instance=resultado)
        if form.is_valid():
            resultado = form.save(commit=False)
            normativa = determinar_normativa(
                resultado.estudio,
                paciente.sexo,
                paciente.edad(),
                paciente.años_educacion
            )
            if normativa:
                resultado.media = normativa.media
                resultado.desviacion = normativa.desviacion
                resultado.puntuacion_z = round((resultado.puntaje_bruto - normativa.media) / normativa.desviacion, 2)
                resultado.perfil_desempeno = interpretar_desempeno(resultado.puntuacion_z)
            resultado.save()
            messages.success(request, "Resultado actualizado correctamente.")
            return redirect('app:detalle_paciente', paciente_id=paciente.id)
    else:
        form = ResultadoForm(instance=resultado)

    return render(request, 'app/editar_resultado.html', {
        'form': form,
        'paciente': paciente,
        'resultado': resultado
    })

def eliminar_resultado(request, resultado_id):
    resultado = get_object_or_404(Resultado, id=resultado_id)
    paciente_id = resultado.paciente.id
    resultado.delete()
    messages.success(request, "Resultado eliminado correctamente.")
    return redirect('app:detalle_paciente', paciente_id=paciente_id)


def editar_relaciones(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = RelacionesForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('app:arbol_genealogico', paciente_id=paciente.id)
    else:
        form = RelacionesForm(instance=paciente)

    return render(request, 'app/editar_relaciones.html', {'form': form, 'paciente': paciente})

  
