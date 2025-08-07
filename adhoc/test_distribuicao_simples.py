#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste simples da lógica de distribuição de vagas
"""

def calcular_distribuicao_vagas(total_vagas):
    """
    Calcula a distribuição automática de vagas conforme os critérios do SISU.
    
    Lógica de Negócio:
    - 50% das vagas vão para Ampla Concorrência
    - 50% das vagas vão para sistemas de cotas, distribuídas assim:
      * 25%: PPI + Escola Pública + Baixa Renda
      * 25%: Escola Pública + Baixa Renda  
      * 20%: PPI + Escola Pública
      * 20%: Escola Pública
      * 10%: Pessoas com Deficiência
    
    Args:
        total_vagas (int): Total de vagas do curso
        
    Returns:
        dict: Distribuição das vagas por modalidade
    """
    if not isinstance(total_vagas, int) or total_vagas <= 0:
        raise ValueError("Total de vagas deve ser um número inteiro positivo")
    
    # Calcular 50% para ampla concorrência (arredondando para baixo)
    vagas_ac = total_vagas // 2
    
    # Os 50% restantes (ou mais, se total for ímpar) vão para cotas
    vagas_cotas = total_vagas - vagas_ac
    
    # Distribuição dentro das cotas (percentuais sobre as vagas de cota)
    # 25% = 0.25, 20% = 0.20, 10% = 0.10
    vagas_ppi_br = int(vagas_cotas * 0.25)          # 25%
    vagas_publica_br = int(vagas_cotas * 0.25)      # 25% 
    vagas_ppi_publica = int(vagas_cotas * 0.20)     # 20%
    vagas_publica = int(vagas_cotas * 0.20)         # 20%
    vagas_deficientes = int(vagas_cotas * 0.10)     # 10%
    
    # Calcular vagas já distribuídas nas cotas
    vagas_cotas_distribuidas = (vagas_ppi_br + vagas_publica_br + 
                               vagas_ppi_publica + vagas_publica + vagas_deficientes)
    
    # Se houver diferença (devido a arredondamentos), ajustar a categoria de deficientes
    diferenca = vagas_cotas - vagas_cotas_distribuidas
    vagas_deficientes += diferenca
    
    # Garantir que nenhuma categoria tenha valor negativo
    vagas_deficientes = max(0, vagas_deficientes)
    
    distribuicao = {
        'vagas_ac': vagas_ac,
        'vagas_ppi_br': vagas_ppi_br,
        'vagas_publica_br': vagas_publica_br,
        'vagas_ppi_publica': vagas_ppi_publica,
        'vagas_publica': vagas_publica,
        'vagas_deficientes': vagas_deficientes
    }
    
    # Verificação final: a soma deve ser igual ao total
    soma_verificacao = sum(distribuicao.values())
    if soma_verificacao != total_vagas:
        # Se ainda há diferença, ajustar ampla concorrência
        diferenca_final = total_vagas - soma_verificacao
        distribuicao['vagas_ac'] += diferenca_final
    
    return distribuicao

def testar_distribuicao():
    """
    Testa a função de distribuição com diferentes valores
    """
    print("🧪 Testando distribuição automática de vagas\n")
    
    casos_teste = [10, 20, 50, 100, 37, 1, 2, 3]
    
    for total in casos_teste:
        print(f"📊 Total de vagas: {total}")
        try:
            distribuicao = calcular_distribuicao_vagas(total)
            
            # Verificar se a soma está correta
            soma = sum(distribuicao.values())
            
            print(f"   • Ampla Concorrência: {distribuicao['vagas_ac']}")
            print(f"   • PPI + EP + BR: {distribuicao['vagas_ppi_br']}")
            print(f"   • EP + BR: {distribuicao['vagas_publica_br']}")
            print(f"   • PPI + EP: {distribuicao['vagas_ppi_publica']}")
            print(f"   • EP: {distribuicao['vagas_publica']}")
            print(f"   • PcD: {distribuicao['vagas_deficientes']}")
            print(f"   ✅ Soma: {soma} (OK: {soma == total})")
            
            if soma != total:
                print(f"   ❌ ERRO: Soma {soma} != Total {total}")
            
            print()
            
        except Exception as e:
            print(f"   ❌ ERRO: {e}\n")
    
    # Teste com valores inválidos
    print("🚫 Testando valores inválidos:")
    valores_invalidos = [0, -5, 'abc', None, 3.14]
    
    for valor in valores_invalidos:
        try:
            resultado = calcular_distribuicao_vagas(valor)
            print(f"   ❌ Valor {valor} deveria ter dado erro!")
        except ValueError as e:
            print(f"   ✅ Valor {valor}: {e}")
        except Exception as e:
            print(f"   ⚠️  Valor {valor}: Erro inesperado: {e}")

if __name__ == "__main__":
    testar_distribuicao()
