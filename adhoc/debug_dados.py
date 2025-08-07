#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug: Verificar se os dados estão sendo salvos corretamente
"""

import sys
sys.path.append('./app')

try:
    from models.Edicao import Edicao
    from models.EdicaoCurso import EdicaoCurso
    from models.Curso import Curso
    
    print("🔍 DEBUGGING: Verificando dados no banco")
    print("=" * 60)
    
    # Listar todas as edições
    print("\n📋 EDIÇÕES EXISTENTES:")
    try:
        edicoes = Edicao.all()
        if edicoes:
            for edicao in edicoes:
                print(f"  • ID: {edicao.id}, Nome: {edicao.nome}, Ano: {edicao.ano}, Semestre: {edicao.semestre}")
        else:
            print("  (Nenhuma edição encontrada)")
    except Exception as e:
        print(f"  ❌ Erro ao buscar edições: {e}")
    
    # Listar todos os cursos
    print("\n🎓 CURSOS EXISTENTES:")
    try:
        cursos = Curso.all()
        if cursos:
            for curso in cursos:
                print(f"  • ID: {curso.id}, Nome: {curso.nome}")
        else:
            print("  (Nenhum curso encontrado)")
    except Exception as e:
        print(f"  ❌ Erro ao buscar cursos: {e}")
    
    # Listar todas as associações EdicaoCurso
    print("\n🔗 ASSOCIAÇÕES EDIÇÃO-CURSO:")
    try:
        edicao_cursos = EdicaoCurso.all()
        if edicao_cursos:
            for ec in edicao_cursos:
                total_vagas = ec.total_vagas() if hasattr(ec, 'total_vagas') else 'N/A'
                print(f"  • Edição: {ec.edicao_id}, Curso: {ec.curso_id}, Total Vagas: {total_vagas}")
                print(f"    - AC: {ec.vagas_ac}, PPI+BR: {ec.vagas_ppi_br}, PUB+BR: {ec.vagas_publica_br}")
                print(f"    - PPI+PUB: {ec.vagas_ppi_publica}, PUB: {ec.vagas_publica}, PCD: {ec.vagas_deficientes}")
        else:
            print("  (Nenhuma associação encontrada)")
    except Exception as e:
        print(f"  ❌ Erro ao buscar associações: {e}")
        
    # Teste específico: buscar cursos de uma edição
    print("\n🧪 TESTE: Buscar cursos da edição mais recente")
    try:
        edicoes = Edicao.all()
        if edicoes:
            ultima_edicao = edicoes[-1]  # Pegar a última edição
            print(f"Testando edição: {ultima_edicao.nome} (ID: {ultima_edicao.id})")
            
            # Simular a lógica do controller view
            edicao_cursos_query = EdicaoCurso()
            edicao_cursos_raw = edicao_cursos_query.where('edicao_id', ultima_edicao.id).get()
            
            print(f"EdicaoCursos encontrados: {len(edicao_cursos_raw)}")
            
            edicao_cursos = []
            for edicao_curso in edicao_cursos_raw:
                curso = Curso.find(edicao_curso.curso_id)
                if curso:
                    edicao_cursos.append({
                        'curso': curso,
                        'configuracao': edicao_curso
                    })
                    print(f"  ✅ Curso: {curso.nome} - {edicao_curso.total_vagas()} vagas")
                else:
                    print(f"  ❌ Curso ID {edicao_curso.curso_id} não encontrado")
            
            print(f"Total de cursos válidos: {len(edicao_cursos)}")
        else:
            print("Nenhuma edição para testar")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de que a aplicação está configurada corretamente")
except Exception as e:
    print(f"❌ Erro geral: {e}")
    import traceback
    traceback.print_exc()
