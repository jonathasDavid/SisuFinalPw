    def create(self):
        """
        Método create SIMPLIFICADO para teste.
        """
        # Carregar cursos disponíveis
        try:
            from models.Curso import Curso
            cursos_disponiveis = Curso.all()
            print(f"Cursos disponíveis: {len(cursos_disponiveis)}")
        except Exception as e:
            print(f"Erro ao carregar cursos: {e}")
            cursos_disponiveis = []

        if self.form.data:
            print("=== PROCESSAMENTO DE FORM SIMPLIFICADO ===")
            
            # Extrair dados básicos
            nome = self.form.get('nome', '')
            ano = self.form.get('ano', 2025)
            semestre = self.form.get('semestre', 1)
            
            print(f"Dados básicos: {nome} ({ano}.{semestre})")
            
            # Criar edição
            from models.Edicao import Edicao
            edicao = Edicao()
            edicao.nome = nome
            edicao.ano = int(ano)
            edicao.semestre = int(semestre)
            edicao.data_inicio = self.form.get('data_inicio', None)
            edicao.data_fim = self.form.get('data_fim', None)
            
            # Encontrar cursos selecionados
            cursos_selecionados = []
            for key, value in self.form.data.items():
                if key.startswith('curso_') and value == 'on':
                    curso_id = int(key.replace('curso_', ''))
                    print(f"Curso selecionado: {curso_id}")
                    
                    # Dados fixos para teste
                    cursos_selecionados.append({
                        'curso_id': curso_id,
                        'vagas_ac': 25,
                        'vagas_ppi_br': 12,
                        'vagas_publica_br': 8,
                        'vagas_ppi_publica': 3,
                        'vagas_publica': 2,
                        'vagas_deficientes': 0
                    })
            
            print(f"Total de cursos selecionados: {len(cursos_selecionados)}")
            
            # Salvar
            error_message = None
            try:
                if cursos_selecionados:
                    print("Tentando salvar com cursos...")
                    if edicao.save_with_cursos_selecionados(cursos_selecionados):
                        print(f"✅ Sucesso! Edição ID: {edicao.id}")
                        self.session['flash'] = f'Edição "{edicao.nome}" criada com {len(cursos_selecionados)} cursos!'
                        self.redirectPage('index')
                        return
                    else:
                        error_message = "Erro ao salvar edição com cursos"
                        print("❌ Falha no save_with_cursos_selecionados")
                else:
                    print("Tentando salvar sem cursos...")
                    if edicao.save():
                        print(f"✅ Sucesso! Edição ID: {edicao.id}")
                        self.session['flash'] = f'Edição "{edicao.nome}" criada!'
                        self.redirectPage('index')
                        return
                    else:
                        error_message = "Erro ao salvar edição"
                        print("❌ Falha no save()")
                        
            except Exception as e:
                error_message = f"Erro interno: {e}"
                print(f"❌ Exception: {e}")
                import traceback
                traceback.print_exc()

            # Se chegou aqui, houve erro
            template = self.env.get_template("create_test.html")
            self.data = template.render(
                cursos_disponiveis=cursos_disponiveis,
                error_message=error_message,
                nome=nome,
                ano=ano,
                semestre=semestre
            )
        else:
            # Formulário não submetido, exibir form vazio
            template = self.env.get_template("create_test.html")
            self.data = template.render(
                cursos_disponiveis=cursos_disponiveis,
                error_message=None
            )
