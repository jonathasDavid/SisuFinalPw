#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste manual das funcionalidades implementadas
"""

def simular_criacao_edicao():
    """
    Simula o processo de criação de uma edição com cursos
    """
    print("🧪 TESTE MANUAL - SIMULAÇÃO DE CRIAÇÃO DE EDIÇÃO")
    print("=" * 60)
    
    # Simular dados do formulário
    form_data = {
        'nome': 'SISU 2025.1 - Teste',
        'ano': '2025',
        'semestre': '1',
        'data_inicio': '2025-01-15',
        'data_fim': '2025-02-28',
        'curso_1': 'on',  # Medicina selecionada
        'total_vagas_1': '40',
        'curso_5': 'on',  # Direito selecionado  
        'total_vagas_5': '80',
        'curso_12': 'on', # Engenharia selecionada
        'total_vagas_12': '60'
    }
    
    print("📝 DADOS DO FORMULÁRIO:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Simular processamento do controller
    print("\n🔄 PROCESSAMENTO DO CONTROLLER:")
    
    cursos_selecionados = []
    cursos_marcados = []
    
    # Função de distribuição (cópia da implementada)
    def calcular_distribuicao_vagas(total_vagas):
        vagas_ac = total_vagas // 2
        vagas_cotas = total_vagas - vagas_ac
        
        vagas_ppi_br = int(vagas_cotas * 0.25)
        vagas_publica_br = int(vagas_cotas * 0.25)
        vagas_ppi_publica = int(vagas_cotas * 0.20)
        vagas_publica = int(vagas_cotas * 0.20)
        vagas_deficientes = int(vagas_cotas * 0.10)
        
        diferenca = vagas_cotas - (vagas_ppi_br + vagas_publica_br + vagas_ppi_publica + vagas_publica + vagas_deficientes)
        vagas_deficientes += diferenca
        vagas_deficientes = max(0, vagas_deficientes)
        
        distribuicao = {
            'vagas_ac': vagas_ac,
            'vagas_ppi_br': vagas_ppi_br,
            'vagas_publica_br': vagas_publica_br,
            'vagas_ppi_publica': vagas_ppi_publica,
            'vagas_publica': vagas_publica,
            'vagas_deficientes': vagas_deficientes
        }
        
        soma = sum(distribuicao.values())
        if soma != total_vagas:
            diferenca_final = total_vagas - soma
            distribuicao['vagas_ac'] += diferenca_final
        
        return distribuicao
    
    # Processar cursos selecionados
    for key, value in form_data.items():
        if key.startswith('curso_') and value == 'on':
            curso_id = key.replace('curso_', '')
            cursos_marcados.append(curso_id)
            
            total_vagas_key = f'total_vagas_{curso_id}'
            total_vagas = form_data.get(total_vagas_key)
            
            if total_vagas and str(total_vagas).strip():
                try:
                    total_vagas_int = int(total_vagas)
                    if total_vagas_int > 0:
                        distribuicao = calcular_distribuicao_vagas(total_vagas_int)
                        
                        vagas_data = {
                            'curso_id': curso_id,
                            'total_vagas': total_vagas_int,
                            'vagas_ac': distribuicao['vagas_ac'],
                            'vagas_ppi_br': distribuicao['vagas_ppi_br'],
                            'vagas_publica_br': distribuicao['vagas_publica_br'],
                            'vagas_ppi_publica': distribuicao['vagas_ppi_publica'],
                            'vagas_publica': distribuicao['vagas_publica'],
                            'vagas_deficientes': distribuicao['vagas_deficientes'],
                        }
                        
                        cursos_selecionados.append(vagas_data)
                        print(f"  ✅ Curso {curso_id}: {total_vagas_int} vagas processadas")
                        
                except (ValueError, TypeError) as e:
                    print(f"  ❌ Erro no curso {curso_id}: {e}")
    
    print(f"\n📊 RESULTADO DO PROCESSAMENTO:")
    print(f"  Cursos marcados: {len(cursos_marcados)}")
    print(f"  Cursos com vagas válidas: {len(cursos_selecionados)}")
    
    # Simular dados que seriam salvos
    print(f"\n💾 DADOS QUE SERIAM SALVOS:")
    print(f"  EDIÇÃO:")
    print(f"    - nome: {form_data['nome']}")
    print(f"    - ano: {form_data['ano']}")
    print(f"    - semestre: {form_data['semestre']}")
    print(f"    - data_inicio: {form_data['data_inicio']}")
    print(f"    - data_fim: {form_data['data_fim']}")
    
    print(f"\n  EDICAO_CURSOS:")
    for i, curso_data in enumerate(cursos_selecionados, 1):
        print(f"    Registro {i}:")
        print(f"      - edicao_id: [ID_DA_EDICAO]")
        print(f"      - curso_id: {curso_data['curso_id']}")
        print(f"      - vagas_ac: {curso_data['vagas_ac']}")
        print(f"      - vagas_ppi_br: {curso_data['vagas_ppi_br']}")
        print(f"      - vagas_publica_br: {curso_data['vagas_publica_br']}")
        print(f"      - vagas_ppi_publica: {curso_data['vagas_ppi_publica']}")
        print(f"      - vagas_publica: {curso_data['vagas_publica']}")
        print(f"      - vagas_deficientes: {curso_data['vagas_deficientes']}")
        total = sum([curso_data['vagas_ac'], curso_data['vagas_ppi_br'], 
                    curso_data['vagas_publica_br'], curso_data['vagas_ppi_publica'],
                    curso_data['vagas_publica'], curso_data['vagas_deficientes']])
        print(f"      - TOTAL: {total} vagas")
        print()
    
    return cursos_selecionados

def simular_view_edicao(cursos_selecionados):
    """
    Simula como seria a visualização da edição
    """
    print("🔍 TESTE MANUAL - SIMULAÇÃO DE VISUALIZAÇÃO")
    print("=" * 60)
    
    # Simular dados como apareceriam na view
    cursos_nomes = {
        '1': 'Medicina',
        '5': 'Direito',
        '12': 'Engenharia Civil'
    }
    
    edicao_cursos = []
    for curso_data in cursos_selecionados:
        curso_id = curso_data['curso_id']
        nome_curso = cursos_nomes.get(curso_id, f'Curso {curso_id}')
        
        # Simular estrutura que seria passada para o template
        mock_ec = {
            'curso': {
                'id': curso_id,
                'nome': nome_curso
            },
            'configuracao': {
                'vagas_ac': curso_data['vagas_ac'],
                'vagas_ppi_br': curso_data['vagas_ppi_br'],
                'vagas_publica_br': curso_data['vagas_publica_br'],
                'vagas_ppi_publica': curso_data['vagas_ppi_publica'],
                'vagas_publica': curso_data['vagas_publica'],
                'vagas_deficientes': curso_data['vagas_deficientes'],
                'total_vagas': lambda: sum([
                    curso_data['vagas_ac'], curso_data['vagas_ppi_br'],
                    curso_data['vagas_publica_br'], curso_data['vagas_ppi_publica'],
                    curso_data['vagas_publica'], curso_data['vagas_deficientes']
                ])
            }
        }
        edicao_cursos.append(mock_ec)
    
    print(f"📋 EDIÇÃO: SISU 2025.1 - Teste")
    print(f"📊 Total de cursos: {len(edicao_cursos)}")
    total_vagas_geral = sum([ec['configuracao']['total_vagas']() for ec in edicao_cursos])
    print(f"📊 Total de vagas: {total_vagas_geral}")
    
    print(f"\n🎓 CURSOS OFERECIDOS:")
    print("-" * 60)
    for ec in edicao_cursos:
        curso = ec['curso']
        config = ec['configuracao']
        total = config['total_vagas']()
        
        print(f"ID: {curso['id']} | {curso['nome']} | {total} vagas")
        
        modalidades = []
        if config['vagas_ac'] > 0:
            modalidades.append(f"AC: {config['vagas_ac']}")
        if config['vagas_ppi_br'] > 0:
            modalidades.append(f"PPI+BR: {config['vagas_ppi_br']}")
        if config['vagas_publica_br'] > 0:
            modalidades.append(f"PUB+BR: {config['vagas_publica_br']}")
        if config['vagas_ppi_publica'] > 0:
            modalidades.append(f"PPI+PUB: {config['vagas_ppi_publica']}")
        if config['vagas_publica'] > 0:
            modalidades.append(f"PUB: {config['vagas_publica']}")
        if config['vagas_deficientes'] > 0:
            modalidades.append(f"PCD: {config['vagas_deficientes']}")
        
        print(f"  Modalidades: {' | '.join(modalidades)}")
        print()

def verificar_problemas_potenciais():
    """
    Lista problemas potenciais identificados
    """
    print("🚨 PROBLEMAS POTENCIAIS IDENTIFICADOS:")
    print("=" * 60)
    
    problemas = [
        {
            'problema': 'Campo total_vagas não funciona',
            'causa_possivel': 'JavaScript não está executando calcularDistribuicao()',
            'solucao': 'Verificar se há erros no console do navegador'
        },
        {
            'problema': 'Cursos não aparecem na view',
            'causa_possivel': 'Dados não estão sendo salvos na tabela edicao_cursos',
            'solucao': 'Verificar logs do controller e do save_with_cursos_selecionados()'
        },
        {
            'problema': 'Erro de módulo orator',
            'causa_possivel': 'Ambiente Python não configurado',
            'solucao': 'Instalar dependências: pip install -r requirements.txt'
        },
        {
            'problema': 'Template view.html com estrutura inconsistente',
            'causa_possivel': 'Tag <td> duplicada ou mal formada',
            'solucao': 'Corrigir estrutura HTML da tabela (já corrigido)'
        }
    ]
    
    for i, p in enumerate(problemas, 1):
        print(f"{i}. {p['problema']}")
        print(f"   Causa possível: {p['causa_possivel']}")
        print(f"   Solução: {p['solucao']}")
        print()

if __name__ == "__main__":
    print("🧪 TESTE MANUAL COMPLETO - FUNCIONALIDADE DE DISTRIBUIÇÃO AUTOMÁTICA")
    print("🎯 Verificando se a implementação está funcionando corretamente")
    print("=" * 80)
    
    # Simular criação
    cursos_selecionados = simular_criacao_edicao()
    
    print("\n" + "=" * 80)
    
    # Simular visualização
    simular_view_edicao(cursos_selecionados)
    
    print("\n" + "=" * 80)
    
    # Listar problemas potenciais
    verificar_problemas_potenciais()
    
    print("=" * 80)
    print("✅ TESTE MANUAL CONCLUÍDO!")
    print("💡 Use este teste para verificar se a lógica está correta.")
    print("🔧 Para problemas reais, verifique os logs do servidor.")
    print("=" * 80)
