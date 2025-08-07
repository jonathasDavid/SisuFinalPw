#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

from app.models.EdicaoCurso import EdicaoCurso
from app.models.Edicao import Edicao
from app.models.Curso import Curso

print("=== TESTE DADOS PARA VIEW ===")

# Verificar edições
print("\n1. EDIÇÕES:")
try:
    edicoes = Edicao.all()
    print(f"Total de edições: {len(edicoes)}")
    for e in edicoes[:3]:
        print(f"  - ID {e.id}: {e.nome} ({e.ano}.{e.semestre})")
except Exception as ex:
    print(f"Erro ao buscar edições: {ex}")

# Verificar EdicaoCursos
print("\n2. EDICAO_CURSOS:")
try:
    ecs = EdicaoCurso.all()
    print(f"Total de EdicaoCursos: {len(ecs)}")
    for ec in ecs[:5]:
        print(f"  - EC ID {ec.id}: Edição {ec.edicao_id}, Curso {ec.curso_id}")
        print(f"    Vagas: AC={ec.vagas_ac}, PPI+BR={ec.vagas_ppi_br}, Total={ec.total_vagas()}")
except Exception as ex:
    print(f"Erro ao buscar EdicaoCursos: {ex}")

# Verificar cursos
print("\n3. CURSOS:")
try:
    cursos = Curso.all()
    print(f"Total de cursos: {len(cursos)}")
    for c in cursos[:3]:
        print(f"  - ID {c.id}: {c.nome}")
except Exception as ex:
    print(f"Erro ao buscar cursos: {ex}")

# Testar a lógica específica do view method
print("\n4. TESTE LÓGICA VIEW (Edição ID 1):")
try:
    edicao = Edicao.find(1)
    if edicao:
        print(f"Edição encontrada: {edicao.nome}")
        
        # Buscar EdicaoCursos desta edição
        edicao_cursos_query = EdicaoCurso()
        edicao_cursos_raw = edicao_cursos_query.where('edicao_id', edicao.id).get()
        print(f"EdicaoCursos encontrados para edição {edicao.id}: {len(edicao_cursos_raw)}")
        
        edicao_cursos = []
        for edicao_curso in edicao_cursos_raw:
            print(f"  - EdicaoCurso ID: {edicao_curso.id}, Curso ID: {edicao_curso.curso_id}")
            
            # Buscar o curso correspondente
            curso = Curso.find(edicao_curso.curso_id)
            if curso:
                print(f"    Curso encontrado: {curso.nome}")
                edicao_cursos.append({
                    'curso': curso,
                    'configuracao': edicao_curso
                })
            else:
                print(f"    ❌ Curso ID {edicao_curso.curso_id} não encontrado")
        
        print(f"Total de cursos válidos para view: {len(edicao_cursos)}")
        
    else:
        print("❌ Edição ID 1 não encontrada")
        
except Exception as ex:
    print(f"Erro no teste view: {ex}")
    import traceback
    traceback.print_exc()
