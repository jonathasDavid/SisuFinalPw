#!/usr/bin/env python3
"""
Teste para validar o funcionamento do Ticket 1 - Nested Models
"""

import sys
import os

# Adiciona o diretório app ao path
app_path = os.path.join(os.path.dirname(__file__), 'app')
sys.path.insert(0, app_path)

from controllers.Controller import Controller

def test_parse_nested_fields():
    """
    Testa o método parseNestedFields com diferentes cenários.
    """
    
    # Mock do environment para criar instância do Controller
    mock_env = {
        'session': {},
        'PATH_INFO': '/app/test/test'
    }
    
    controller = Controller(mock_env)
    
    print("🧪 Testando parseNestedFields...")
    print("=" * 50)
    
    # Teste 1: Campos simples (deve manter como está)
    print("\n📝 Teste 1: Campos simples")
    simple_data = {
        'nome': 'SISU 2025.1',
        'ano': '2025',
        'semestre': '1'
    }
    result = controller.parseNestedFields(simple_data)
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
    result = controller.parseNestedFields(nested_data)
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
    result = controller.parseNestedFields(non_sequential)
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
    result = controller.parseNestedFields(multi_nested)
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
    result = controller.parseNestedFields(direct_array)
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

if __name__ == "__main__":
    test_parse_nested_fields()
