#!/usr/bin/env python3
"""
Teste para criar edição com cursos e vagas via formulário POST.
"""

import requests
import json

def test_criar_edicao_com_vagas():
    """Testa criação de edição com cursos e vagas definidas."""
    
    # URL da aplicação
    base_url = "http://localhost:1080"
    create_url = f"{base_url}/app/edicao/create"
    
    # Dados do formulário
    form_data = {
        'nome': 'Teste com Vagas Automático',
        'ano': '2025',
        'semestre': '2',
        'data_inicio': '2025-08-15',
        'data_fim': '2025-08-30',
        'curso_2': 'on',  # Medicina
        'total_vagas_2': '100',
        'curso_3': 'on',  # Direito
        'total_vagas_3': '80'
    }
    
    print("=== TESTE: Criando edição com vagas ===")
    print(f"URL: {create_url}")
    print(f"Dados: {json.dumps(form_data, indent=2)}")
    
    try:
        # Enviar POST request
        response = requests.post(create_url, data=form_data, allow_redirects=False)
        
        print(f"\n=== RESPOSTA ===")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            print(f"✅ Redirecionamento para: {response.headers.get('Location')}")
            print("✅ Edição criada com sucesso!")
            
            # Extrair ID da edição criada se possível
            location = response.headers.get('Location', '')
            if '/view/' in location:
                edicao_id = location.split('/view/')[-1]
                print(f"✅ ID da edição criada: {edicao_id}")
                
                # Tentar acessar página de visualização
                view_url = f"{base_url}{location}"
                print(f"\n=== TESTANDO VISUALIZAÇÃO ===")
                print(f"URL: {view_url}")
                
                view_response = requests.get(view_url)
                print(f"Status Code: {view_response.status_code}")
                
                if view_response.status_code == 200:
                    content = view_response.text
                    if 'Medicina' in content and 'Direito' in content:
                        print("✅ Cursos aparecem na página de visualização!")
                    else:
                        print("❌ Cursos NÃO aparecem na página de visualização")
                        # Mostrar parte do conteúdo para debug
                        print(f"Conteúdo (primeiros 500 chars): {content[:500]}")
                else:
                    print(f"❌ Erro ao acessar página de visualização: {view_response.status_code}")
            
        elif response.status_code == 200:
            print("❌ Formulário retornado (possível erro de validação)")
            # Verificar se há mensagem de erro
            content = response.text
            if 'alert-danger' in content:
                print("❌ Erro encontrado na resposta")
                # Extrair mensagem de erro
                import re
                error_match = re.search(r'alert-danger[^>]*>([^<]+)', content)
                if error_match:
                    print(f"Erro: {error_match.group(1).strip()}")
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            print(f"Conteúdo: {response.text[:500]}")
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")

if __name__ == "__main__":
    test_criar_edicao_com_vagas()
