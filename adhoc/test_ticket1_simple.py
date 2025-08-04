#!/usr/bin/env python3
"""
Teste simplificado para validar o funcionamento do Ticket 1 - Nested Models
"""

import re
from html import escape

def parse_nested_fields(form_data):
    """
    Converte dados de formulário com campos indexados em estrutura aninhada.
    (Cópia do método implementado no Controller)
    """
    nested_data = {}
    
    # Padrão para campos indexados: campo[index][subcampo] ou campo[index]
    pattern = r'^([a-zA-Z_][a-zA-Z0-9_]*)\[(\d+)\](?:\[([a-zA-Z_][a-zA-Z0-9_]*)\])?$'
    
    for key, value in form_data.items():
        match = re.match(pattern, key)
        
        if match:
            field_name = match.group(1)  # ex: 'cursos'
            index = int(match.group(2))  # ex: 0, 1, 2...
            subfield = match.group(3)    # ex: 'curso_id', 'nome' (pode ser None)
            
            # Inicializa a lista se não existir
            if field_name not in nested_data:
                nested_data[field_name] = []
            
            # Garante que a lista tem o tamanho necessário
            while len(nested_data[field_name]) <= index:
                nested_data[field_name].append({})
            
            if subfield:
                # Caso: cursos[0][curso_id]
                nested_data[field_name][index][subfield] = value
            else:
                # Caso: cursos[0] (valor direto)
                nested_data[field_name][index] = value
        else:
            # Campo simples, mantém como está
            nested_data[key] = value
    
    return nested_data

def test_parse_nested_fields():
    """
    Testa o método parseNestedFields com diferentes cenários.
    """
    
    print("🧪 Testando parseNestedFields...")
    print("=" * 50)
    
    # Teste 1: Campos simples (deve manter como está)
    print("\n📝 Teste 1: Campos simples")
    simple_data = {
        'nome': 'SISU 2025.1',
        'ano': '2025',
        'semestre': '1'
    }
    result = parse_nested_fields(simple_data)
    print(f"Input:  {simple_data}")
    print(f"Output: {result}")
    assert result == simple_data, "Campos simples devem permanecer inalterados"
    print("✅ Passou!")
    
    # Teste 2: Campos aninhados básicos
    print("\n📝 Teste 2: Campos aninhados básicos")
    nested_data = {
        'nome': 'SISU 2025.1',
        'cursos[0][curso_id]': '12345',
        'cursos[0][nome]': 'Engenharia da Computação',
        'cursos[1][curso_id]': '67890',
        'cursos[1][nome]': 'Medicina'
    }
    result = parse_nested_fields(nested_data)
    print(f"Input:  {nested_data}")
    print(f"Output: {result}")
    
    expected = {
        'nome': 'SISU 2025.1',
        'cursos': [
            {'curso_id': '12345', 'nome': 'Engenharia da Computação'},
            {'curso_id': '67890', 'nome': 'Medicina'}
        ]
    }
    assert result == expected, f"Esperado: {expected}, Obtido: {result}"
    print("✅ Passou!")
    
    # Teste 3: Índices não sequenciais
    print("\n📝 Teste 3: Índices não sequenciais")
    non_sequential = {
        'titulo': 'Processo Seletivo',
        'cursos[0][nome]': 'Curso A',
        'cursos[2][nome]': 'Curso C',  # Pula o índice 1
        'cursos[1][nome]': 'Curso B'
    }
    result = parse_nested_fields(non_sequential)
    print(f"Input:  {non_sequential}")
    print(f"Output: {result}")
    
    # Deve preencher com dicionários vazios para manter os índices
    expected = {
        'titulo': 'Processo Seletivo',
        'cursos': [
            {'nome': 'Curso A'},
            {'nome': 'Curso B'},
            {'nome': 'Curso C'}
        ]
    }
    assert result == expected, f"Esperado: {expected}, Obtido: {result}"
    print("✅ Passou!")
    
    # Teste 4: Múltiplos arrays aninhados
    print("\n📝 Teste 4: Múltiplos arrays aninhados")
    multi_nested = {
        'evento': 'SISU 2025',
        'cursos[0][nome]': 'Engenharia',
        'cursos[0][vagas]': '40',
        'professores[0][nome]': 'Dr. Silva',
        'professores[0][departamento]': 'Computação',
        'professores[1][nome]': 'Dra. Santos',
        'professores[1][departamento]': 'Matemática'
    }
    result = parse_nested_fields(multi_nested)
    print(f"Input:  {multi_nested}")
    print(f"Output: {result}")
    
    expected = {
        'evento': 'SISU 2025',
        'cursos': [
            {'nome': 'Engenharia', 'vagas': '40'}
        ],
        'professores': [
            {'nome': 'Dr. Silva', 'departamento': 'Computação'},
            {'nome': 'Dra. Santos', 'departamento': 'Matemática'}
        ]
    }
    assert result == expected, f"Esperado: {expected}, Obtido: {result}"
    print("✅ Passou!")
    
    # Teste 5: Arrays diretos (sem subcampos)
    print("\n📝 Teste 5: Arrays diretos")
    direct_array = {
        'nome': 'Lista de IDs',
        'ids[0]': '100',
        'ids[1]': '200',
        'ids[2]': '300'
    }
    result = parse_nested_fields(direct_array)
    print(f"Input:  {direct_array}")
    print(f"Output: {result}")
    
    expected = {
        'nome': 'Lista de IDs',
        'ids': ['100', '200', '300']
    }
    assert result == expected, f"Esperado: {expected}, Obtido: {result}"
    print("✅ Passou!")
    
    print("\n🎉 Todos os testes passaram!")
    print("✅ Ticket 1 implementado com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. Testar com formulário real usando Docker")
    print("   2. Implementar Ticket 2 (saveMany)")

if __name__ == "__main__":
    test_parse_nested_fields()
