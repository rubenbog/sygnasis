from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('listar/', views.listar_pacientes, name='listar_pacientes'),
    path('cargar/', views.cargar_paciente, name='cargar_paciente'),
    path('resultado/cargar/', views.cargar_resultado, name='cargar_resultado'),
    path('estudios/cargar_json/', views.cargar_estudios_json, name='cargar_estudios_json'),
    path('buscar/', views.buscar_paciente, name='buscar_paciente'),
    path('arbol/<int:paciente_id>/', views.arbol_genealogico, name='arbol_genealogico'),
    path('<int:paciente_id>/arbol/', views.arbol_genealogico, name='arbol_genealogico'),
    path('<int:paciente_id>/', views.detalle_paciente, name='detalle_paciente'),
    path('<int:paciente_id>/resultado/', views.agregar_resultado, name='agregar_resultado'),
    path('resultado/<int:resultado_id>/editar/', views.editar_resultado, name='editar_resultado'),
    path('normativas/', views.listar_normativas, name='listar_normativas'),
    path('normativas/nueva/', views.agregar_normativa, name='agregar_normativa'),
    path('normativas/<int:normativa_id>/editar/', views.editar_normativa, name='editar_normativa'),
    path('resultado/<int:resultado_id>/eliminar/', views.eliminar_resultado, name='eliminar_resultado'),
    path('<int:paciente_id>/editar_relaciones/', views.editar_relaciones, name='editar_relaciones'),
    path('<int:paciente_id>/diagnostico/', views.agregar_diagnostico, name='agregar_diagnostico'),
    path('<int:paciente_id>/sintoma/', views.agregar_sintoma, name='agregar_sintoma'),
    path('<int:paciente_id>/comorbilidad/', views.agregar_comorbilidad, name='agregar_comorbilidad'),
    path('<int:paciente_id>/informe/', views.agregar_informe, name='agregar_informe'),
    path('<int:paciente_id>/medicacion/', views.agregar_medicacion, name='agregar_medicacion'),
    path('editar/<int:paciente_id>/', views.editar_paciente, name='editar_paciente'),
    path('eliminar/<int:paciente_id>/', views.eliminar_paciente, name='eliminar_paciente'),
    path('diagnostico/<int:diagnostico_id>/editar/', views.editar_diagnostico, name='editar_diagnostico'),
    path('diagnostico/<int:diagnostico_id>/eliminar/', views.eliminar_diagnostico, name='eliminar_diagnostico'),
    path('sintomas/<int:sintoma_id>/editar/', views.editar_sintomas, name='editar_sintomas'),
    path('sintomas/<int:sintoma_id>/eliminar/', views.eliminar_sintomas, name='eliminar_sintomas'),
    path('comorbilidad/<int:comorbilidad_id>/editar/', views.editar_comorbilidad, name='editar_comorbilidad'),
    path('comorbilidad/<int:comorbilidad_id>/eliminar/', views.eliminar_comorbilidad, name='eliminar_comorbilidad'),
    path('informe/<int:informe_id>/editar/', views.editar_informe, name='editar_informe'),
    path('informe/<int:informe_id>/eliminar/', views.eliminar_informe, name='eliminar_informe'),
    path('medicacion/<int:medicacion_id>/editar/', views.editar_medicacion, name='editar_medicacion'),
    path('medicacion/<int:medicacion_id>/eliminar/', views.eliminar_medicacion, name='eliminar_medicacion'),


]
