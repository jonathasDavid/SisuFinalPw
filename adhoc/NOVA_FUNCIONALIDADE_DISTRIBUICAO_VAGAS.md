# 🎯 Nova Funcionalidade: Distribuição Automática de Vagas SISU

## 📋 Resumo das Mudanças

A interface de criação de edições SISU foi completamente reformulada para implementar a **distribuição automática de vagas** conforme os critérios oficiais do SISU.

## 🔄 Antes vs. Depois

### ❌ ANTES (Interface Manual)
- O usuário precisava inserir manualmente o número de vagas para cada modalidade/cota
- 6 campos separados para preencher por curso
- Risco de erros de cálculo
- Processo demorado e propenso a inconsistências

### ✅ AGORA (Distribuição Automática)
- O usuário insere apenas o **total de vagas** do curso
- O sistema calcula automaticamente a distribuição conforme os percentuais oficiais
- Interface simplificada e intuitiva
- Garantia de que os cálculos estão corretos

## 🎯 Como Funciona

### 1. Lógica de Distribuição
```
📊 Total de Vagas: 100 (exemplo)

🔄 Divisão Principal:
• 50% → Ampla Concorrência = 50 vagas
• 50% → Sistema de Cotas = 50 vagas

📋 Distribuição das Cotas (50 vagas):
• 25% → PPI + EP + BR = 12 vagas
• 25% → EP + BR = 12 vagas  
• 20% → PPI + EP = 10 vagas
• 20% → EP = 10 vagas
• 10% → PcD = 6 vagas (ajustado para completar)

✅ Total: 50 + 12 + 12 + 10 + 10 + 6 = 100 vagas
```

### 2. Interface Nova
```html
<!-- Campo Único para Total -->
<input type="number" name="total_vagas_123" placeholder="Ex: 50">

<!-- Distribuição Calculada (Read-only) -->
<div class="distribuicao-calculada">
  <input readonly name="vagas_ac_123" value="25">      <!-- AC -->
  <input readonly name="vagas_ppi_br_123" value="6">   <!-- PPI+EP+BR -->
  <input readonly name="vagas_publica_br_123" value="6"> <!-- EP+BR -->
  <input readonly name="vagas_ppi_publica_123" value="5"> <!-- PPI+EP -->
  <input readonly name="vagas_publica_123" value="5">   <!-- EP -->
  <input readonly name="vagas_deficientes_123" value="3"> <!-- PcD -->
</div>
```

## 🛠️ Implementação Técnica

### 1. Função Principal
```python
@staticmethod
def calcular_distribuicao_vagas(total_vagas):
    """
    Calcula distribuição automática conforme critérios SISU
    """
    # 50% Ampla Concorrência
    vagas_ac = total_vagas // 2
    vagas_cotas = total_vagas - vagas_ac
    
    # Distribuição das cotas
    vagas_ppi_br = int(vagas_cotas * 0.25)      # 25%
    vagas_publica_br = int(vagas_cotas * 0.25)  # 25%
    vagas_ppi_publica = int(vagas_cotas * 0.20) # 20%
    vagas_publica = int(vagas_cotas * 0.20)     # 20%
    vagas_deficientes = int(vagas_cotas * 0.10) # 10%
    
    # Ajuste para arredondamentos
    diferenca = vagas_cotas - (vagas_ppi_br + vagas_publica_br + 
                              vagas_ppi_publica + vagas_publica + vagas_deficientes)
    vagas_deficientes += diferenca
    
    return {
        'vagas_ac': vagas_ac,
        'vagas_ppi_br': vagas_ppi_br,
        'vagas_publica_br': vagas_publica_br,
        'vagas_ppi_publica': vagas_ppi_publica,
        'vagas_publica': vagas_publica,
        'vagas_deficientes': vagas_deficientes
    }
```

### 2. JavaScript Frontend
```javascript
function calcularDistribuicao(cursoId) {
    const totalVagas = parseInt(document.querySelector(`input[name="total_vagas_${cursoId}"]`).value);
    
    if (totalVagas > 0) {
        const distribuicao = calcularDistribuicaoVagas(totalVagas);
        
        // Preencher campos calculados
        document.querySelector(`input[name="vagas_ac_${cursoId}"]`).value = distribuicao.vagas_ac;
        document.querySelector(`input[name="vagas_ppi_ep_br_${cursoId}"]`).value = distribuicao.vagas_ppi_br;
        // ... outros campos
        
        // Mostrar distribuição
        document.getElementById(`distribuicao-${cursoId}`).style.display = 'block';
    }
}
```

### 3. Processamento Backend
```python
# No EdicaoController.create()
total_vagas_key = f'total_vagas_{curso_id}'
total_vagas = form_data.get(total_vagas_key)

if total_vagas and int(total_vagas) > 0:
    from models.CursoBase import CursoBase
    
    # Calcular distribuição automática
    distribuicao = CursoBase.calcular_distribuicao_vagas(int(total_vagas))
    
    # Usar distribuição para salvar
    vagas_data = {
        'curso_id': curso_id,
        'total_vagas': int(total_vagas),
        'vagas_ac': distribuicao['vagas_ac'],
        'vagas_ppi_br': distribuicao['vagas_ppi_br'],
        # ... outros campos
    }
```

## 🧪 Exemplos de Teste

### Teste 1: 100 vagas
```
Total: 100
• AC: 50 (50%)
• PPI+EP+BR: 12 (25% de 50)
• EP+BR: 12 (25% de 50)  
• PPI+EP: 10 (20% de 50)
• EP: 10 (20% de 50)
• PcD: 6 (10% de 50)
Soma: 50+12+12+10+10+6 = 100 ✅
```

### Teste 2: 37 vagas
```
Total: 37
• AC: 18 (37÷2)
• Cotas: 19 (37-18)
• PPI+EP+BR: 4 (25% de 19)
• EP+BR: 4 (25% de 19)
• PPI+EP: 3 (20% de 19)
• EP: 3 (20% de 19)
• PcD: 5 (10% de 19 + ajuste)
Soma: 18+4+4+3+3+5 = 37 ✅
```

## 📁 Arquivos Modificados

1. **`models/CursoBase.py`** - Função `calcular_distribuicao_vagas()`
2. **`views/edicao/create.html`** - Nova interface simplificada
3. **`controllers/EdicaoController.py`** - Processamento do novo campo
4. **`test_distribuicao_simples.py`** - Testes da função

## 🎉 Benefícios

1. **Simplicidade**: Um campo vs. seis campos
2. **Precisão**: Cálculos automáticos e corretos
3. **Consistência**: Sempre seguindo os critérios oficiais
4. **Velocidade**: Processo muito mais rápido
5. **Transparência**: Usuário vê exatamente como foi calculado
6. **Flexibilidade**: Funciona com qualquer número de vagas

## 🔧 Como Usar

1. Acesse "Criar Nova Edição"
2. Preencha dados da edição (nome, ano, semestre)
3. Marque os cursos desejados
4. Para cada curso marcado:
   - Digite o **total de vagas** no campo único
   - A distribuição aparecerá automaticamente
5. Clique em "Criar Edição"

Pronto! O sistema calculará e salvará a distribuição automaticamente.
