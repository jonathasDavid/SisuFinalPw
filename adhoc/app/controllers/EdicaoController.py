import sys
sys.path.append('./app')
from jinja2 import Environment, FileSystemLoader
from models.Edicao import Edicao
from models.Curso import Curso
from controllers.Controller import Controller
import os


class EdicaoController(Controller):
    """
    Controller para gerenciar edições do SISU com cursos associados.
    """

    def create(self):
        """
        Criar nova edição com cursos existentes selecionados.
        Busca cursos disponíveis no sistema para associação.
        """
        method = self.environ["REQUEST_METHOD"]
        print(f"=== EDICAO CREATE - MÉTODO: {method} ===")
        
        template = self.env.get_template("create_test.html")
        edicao = Edicao()
        
        # Buscar todos os cursos disponíveis no sistema para seleção
        try:
            cursos_disponiveis = Curso.todos_cursos()
            print(f"✅ Cursos encontrados: {len(cursos_disponiveis)}")
            for curso in cursos_disponiveis:
                # Debug para verificar encoding
                nome_curso = curso.nome
                print(f"- ID: {curso.id}, Nome: {repr(nome_curso)} ({nome_curso})")
                
                # Tenta corrigir encoding se necessário
                if '?????' in str(nome_curso) or '?' in str(nome_curso):
                    try:
                        # Tenta decodificar se está com problema de encoding
                        nome_curso = nome_curso.encode('latin1').decode('utf-8')
                        curso.nome = nome_curso
                        print(f"  -> Nome corrigido: {nome_curso}")
                    except:
                        print(f"  -> Não foi possível corrigir encoding")
        except Exception as e:
            print(f"❌ Erro ao buscar cursos: {e}")
            cursos_disponiveis = []
        
        if method == "POST":
            # Processa formulário com cursos selecionados
            form_data = self.loadNestedForm(edicao)
            
            # Preenche os campos da edição com os dados do formulário
            edicao.nome = form_data.get('nome', '')
            edicao.ano = form_data.get('ano', '')
            edicao.semestre = form_data.get('semestre', '')
            
            # Tratar datas vazias para evitar erro SQL
            data_inicio = form_data.get('data_inicio', '')
            data_fim = form_data.get('data_fim', '')
            
            edicao.data_inicio = data_inicio if data_inicio and data_inicio.strip() else None
            edicao.data_fim = data_fim if data_fim and data_fim.strip() else None
            
            # Preservar dados dos cursos selecionados para reexibir em caso de erro
            cursos_selecionados_form = {}
            vagas_preenchidas = {}
            
            # Extrai cursos selecionados e suas configurações de vagas
            cursos_selecionados = []
            cursos_marcados = []  # Debug: cursos que foram marcados no checkbox
            
            print("=== DEBUG: Processando formulário ===")
            print(f"Dados recebidos: {list(form_data.keys())}")
            
            for key, value in form_data.items():
                if key.startswith('curso_') and value == 'on':
                    curso_id = key.replace('curso_', '')
                    cursos_marcados.append(curso_id)
                    cursos_selecionados_form[curso_id] = True
                    print(f"Curso marcado: {curso_id}")
                    
                    # Busca dados do curso original
                    curso_original = None
                    for curso in cursos_disponiveis:
                        if str(curso.id) == curso_id:
                            curso_original = curso
                            break
                    
                    if curso_original:
                        # Busca o total de vagas para este curso
                        total_vagas_key = f'total_vagas_{curso_id}'
                        total_vagas = form_data.get(total_vagas_key)
                        
                        print(f"Total de vagas para curso {curso_id}: {total_vagas}")
                        
                        if total_vagas and str(total_vagas).strip():
                            try:
                                total_vagas_int = int(total_vagas)
                                if total_vagas_int > 0:
                                    # Calcular distribuição automática usando o modelo correto
                                    distribuicao = Curso.calcular_distribuicao_vagas(total_vagas_int)
                                    
                                    # Criar dados do curso com a distribuição calculada
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
                                    
                                    # Preservar total de vagas preenchido para reexibir em caso de erro
                                    vagas_preenchidas[curso_id] = {
                                        'total_vagas': total_vagas,
                                    }
                                    
                                    print(f"Curso {curso_id} ({curso_original.nome}): {total_vagas_int} vagas totais")
                                    print(f"  Distribuição calculada:")
                                    for modalidade, qtd in distribuicao.items():
                                        print(f"    - {modalidade}: {qtd}")
                                    
                                    cursos_selecionados.append(vagas_data)
                                else:
                                    print(f"Curso {curso_id}: total de vagas inválido ({total_vagas_int})")
                            except (ValueError, TypeError) as e:
                                print(f"Erro ao processar total de vagas para curso {curso_id}: {e}")
                        else:
                            print(f"Curso {curso_id} marcado mas sem total de vagas definido")
                        
                        # Preservar total de vagas mesmo se inválido (para reexibir)
                        if curso_id not in vagas_preenchidas:
                            vagas_preenchidas[curso_id] = {
                                'total_vagas': total_vagas or '',
                            }
            
            print(f"=== RESULTADO ===")
            print(f"Cursos marcados: {len(cursos_marcados)} - {cursos_marcados}")
            print(f"Cursos com vagas: {len(cursos_selecionados)}")
            
            # Mudança na lógica: permitir criar edição apenas com cursos marcados, mesmo sem vagas
            # Isso porque o usuário pode querer criar a edição e definir vagas depois
            error_message = None
            
            if edicao.validate():
                if cursos_marcados:  # Se há cursos marcados (independente de terem vagas)
                    # Se há cursos com vagas definidas, salva normalmente
                    if cursos_selecionados:
                        print(f"=== SALVANDO EDIÇÃO COM CURSOS ===")
                        print(f"Cursos selecionados: {len(cursos_selecionados)}")
                        for curso_data in cursos_selecionados:
                            print(f"  - Curso {curso_data['curso_id']}: {curso_data.get('total_vagas', 'N/A')} vagas")
                            
                        if edicao.save_with_cursos_selecionados(cursos_selecionados):
                            print(f"✅ Edição salva com sucesso! ID: {edicao.id}")
                            self.session['flash'] = f'Edição "{edicao.nome}" criada com {len(cursos_selecionados)} curso(s) e vagas definidas!'
                            self.redirectPage('index')
                        else:
                            print(f"❌ Erro ao salvar edição com cursos")
                            error_message = f"Erro ao salvar edição com cursos. Erro: {getattr(edicao, 'error', 'Erro desconhecido')}"
                    else:
                        # Se há cursos marcados mas sem vagas, salva apenas a edição
                        if edicao.save():
                            self.session['flash'] = f'Edição "{edicao.nome}" criada! Você pode adicionar cursos e vagas posteriormente.'
                            self.redirectPage('index')
                        else:
                            error_message = "Erro ao salvar edição"
                else:
                    # Permite criar edição sem cursos também
                    if edicao.save():
                        self.session['flash'] = f'Edição "{edicao.nome}" criada! Você pode adicionar cursos posteriormente.'
                        self.redirectPage('index')
                    else:
                        error_message = "Erro ao salvar edição"
        
        # Passar dados preservados para o template
        print(f"🎨 Renderizando template create.html:")
        print(f"  - cursos_disponiveis: {len(cursos_disponiveis) if cursos_disponiveis else 0}")
        print(f"  - cursos_selecionados_form: {locals().get('cursos_selecionados_form', {})}")
        print(f"  - vagas_preenchidas: {locals().get('vagas_preenchidas', {})}")
        print(f"  - error_message: {locals().get('error_message', None)}")
        
        self.data = template.render(
            edicao=edicao,
            cursos_disponiveis=cursos_disponiveis,
            cursos_selecionados_form=locals().get('cursos_selecionados_form', {}),
            vagas_preenchidas=locals().get('vagas_preenchidas', {}),
            error_message=locals().get('error_message', None)
        )

    def update(self, id):
        """
        Atualizar edição existente com cursos.
        """
        method = self.environ["REQUEST_METHOD"]
        template = self.env.get_template("update.html")
        edicao = Edicao.find(id[0])
        
        if not edicao:
            self.notFound()
            return
        
        if method == "POST":
            # Processa formulário
            form_data = self.loadNestedForm(edicao)
            
            if edicao.validate():
                if edicao.save():
                    self.session['flash'] = f'Edição "{edicao.nome}" atualizada!'
                    self.redirectPage('view', {'id': edicao.id})
        
        self.data = template.render(edicao=edicao)

    def view(self, id):
        """
        Visualizar edição com seus cursos associados.
        """
        edicao = Edicao.find(id[0])
        if not edicao:
            self.notFound()
            return
        
        print(f"=== DEBUG VIEW SIMPLIFICADO: Edição {edicao.id} ===")
        
        # TESTE 1: Tentar buscar EdicaoCursos diretamente
        edicao_cursos = []
        try:
            from models.EdicaoCurso import EdicaoCurso
            from models.Curso import Curso
            print("✅ Importação EdicaoCurso e Curso OK")
            
            # Buscar todos os EdicaoCurso desta edição usando query builder
            from orator import DatabaseManager
            db = EdicaoCurso.get_connection_resolver().connection()
            
            # Consulta direta
            query_result = db.table('edicao_cursos').where('edicao_id', edicao.id).get()
            print(f"EdicaoCursos encontrados via query: {len(query_result)}")
            
            for row in query_result:
                print(f"  - EdicaoCurso ID: {row.id}, Curso ID: {row.curso_id}")
                
                # Buscar curso usando o ID da tabela cursos
                curso = Curso.find(row.curso_id)
                if curso:
                    print(f"    ✅ Curso encontrado: {curso.nome}")
                    
                    # Criar mock do EdicaoCurso para o template
                    mock_edicao_curso = type('MockEdicaoCurso', (), {
                        'id': row.id,
                        'edicao_id': row.edicao_id,
                        'curso_id': row.curso_id,
                        'vagas_ac': row.vagas_ac or 0,
                        'vagas_ppi_br': row.vagas_ppi_br or 0,
                        'vagas_publica_br': row.vagas_publica_br or 0,
                        'vagas_ppi_publica': row.vagas_ppi_publica or 0,
                        'vagas_publica': row.vagas_publica or 0,
                        'vagas_deficientes': row.vagas_deficientes or 0,
                    })()
                    
                    edicao_cursos.append({
                        'curso': curso,
                        'configuracao': mock_edicao_curso
                    })
                else:
                    print(f"    ❌ Curso ID {row.curso_id} não encontrado")
            
            print(f"Total processado: {len(edicao_cursos)}")
            
        except Exception as e:
            print(f"❌ Erro ao buscar EdicaoCursos: {e}")
            import traceback
            traceback.print_exc()
        
        # Mensagem flash se houver
        message = ""
        if 'flash' in self.session:
            message = self.session['flash']
            self.session['flash'] = ""
        
        template = self.env.get_template("view.html")
        print(f"🎨 Renderizando template view.html:")
        print(f"  - edicao.id: {edicao.id}")
        print(f"  - edicao.nome: {edicao.nome}")
        print(f"  - edicao_cursos tipo: {type(edicao_cursos)}")
        print(f"  - edicao_cursos length: {len(edicao_cursos)}")
        print(f"  - edicao_cursos dados: {edicao_cursos}")
        print(f"  - message: {repr(message)}")
        
        self.data = template.render(
            edicao=edicao, 
            edicao_cursos=edicao_cursos, 
            message=message
        )

    def debug(self):
        """
        Página para mostrar como os dados aninhados foram processados.
        """
        debug_data = self.session.get('debug_data', {})
        template = self.env.get_template("debug.html")
        self.data = template.render(debug_data=debug_data)

    def index(self):
        """
        Lista edições.
        """
        try:
            edicoes = Edicao.all()
        except Exception as e:
            print(f"Erro ao buscar edições: {e}")
            edicoes = []
        
        template = self.env.get_template("index.html")
        # Capturar mensagem flash da sessão
        flash_message = self.session.get('flash')
        if flash_message:
            del self.session['flash']  # Remove após usar
        
        self.data = template.render(
            edicoes=edicoes,
            session={'flash': flash_message} if flash_message else {}
        )

    def delete(self, id):
        """
        Excluir edição e seus cursos associados.
        """
        edicao = Edicao.find(id[0])
        if not edicao:
            self.session['flash'] = 'Edição não encontrada!'
            self.redirectPage('index')
            return
        
        try:
            # Deletar cursos associados primeiro (CASCADE deve fazer isso automaticamente)
            from models.EdicaoCurso import EdicaoCurso
            EdicaoCurso.where('edicao_id', edicao.id).delete()
            
            # Guardar nome para mensagem
            nome_edicao = edicao.nome
            
            # Deletar a edição
            if edicao.delete():
                self.session['flash'] = f'Edição "{nome_edicao}" excluída com sucesso!'
            else:
                self.session['flash'] = 'Erro ao excluir a edição!'
                
        except Exception as e:
            print(f"Erro ao excluir edição: {e}")
            self.session['flash'] = f'Erro ao excluir edição: {str(e)}'
        
        self.redirectPage('index')
