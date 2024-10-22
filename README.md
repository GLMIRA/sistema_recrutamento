# sistema_recrutamento
Sistema de recrutamento para uma empresa 

candidato/<int:id_candidato>/experiencia/<id_experiencia> --> detalhe de experiencia
candidato/<int:id_candidato>/experiencia/ --> lista de experiencias
candidato/<int:id_candidato>/experiencia/criar/ --> criar experiencia


get_object_or_404(Experiencia, candidate=id_candidato, id=id_experiencia)
get_list_or_404(Experiencia, candidate=id_candidato)