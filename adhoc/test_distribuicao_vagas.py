#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste da função de distribuição automática de vagas
"""

import sys
sys.path.append('./app')

from models.CursoBase import CursoBase

def testar_distribuicao():
    """
    Testa a função de distribuição com diferentes valores
    """
    print("🧪 Testando distribuição automática de vagas\n")
    
    casos_teste = [10, 20, 50, 100, 37, 1, 2, 3]
    
    for total in casos_teste:
        print(f"📊 Total de vagas: {total}")
        try:
            distribuicao = CursoBase.calcular_distribuicao_vagas(total)
            
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
            resultado = CursoBase.calcular_distribuicao_vagas(valor)
            print(f"   ❌ Valor {valor} deveria ter dado erro!")
        except ValueError as e:
            print(f"   ✅ Valor {valor}: {e}")
        except Exception as e:
            print(f"   ⚠️  Valor {valor}: Erro inesperado: {e}")

if __name__ == "__main__":
    testar_distribuicao()
