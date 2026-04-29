# ============================================================
# menu.py - Menu interativo do sistema SteamPy
# ============================================================
# Menu principal que permite usuario interagir com o sistema
# 19 opcoes conforme especificado no PDF

from steampy import SteamPy


def menu(sistema):
    # Loop principal do menu
    # Exibe opcoes e executa acoes baseado na escolha do usuario

    while True:
        print(f"\n{'='*50}")
        print(f"       STEAMPY - Menu Principal")
        print(f"{'='*50}")
        # Exibe todas as 19 opcoes do menu
        print("  1.  Carregar catalogo")
        print("  2.  Listar jogos")
        print("  3.  Buscar jogo por nome")
        print("  4.  Filtrar por genero")
        print("  5.  Filtrar por console")
        print("  6.  Filtrar por nota minima")
        print("  7.  Ordenar catalogo")
        print("  8.  Adicionar jogo ao backlog")
        print("  9.  Ver backlog")
        print("  10. Jogar proximo do backlog")
        print("  11. Ver jogos recentes")
        print("  12. Retomar ultimo jogo")
        print("  13. Registrar tempo de jogo")
        print("  14. Ver historico completo")
        print("  15. Ver recomendacoes")
        print("  16. Ver ranking pessoal")
        print("  17. Ver dashboard")
        print("  18. Salvar backlog")
        print("  19. Sair")
        print(f"{'='*50}")

        opcao = input("  Escolha uma opcao: ").strip()

        # ---- opcao 1: carregar catalogo ----
        if opcao == '1':
            # Carrega o arquivo dataset.csv com todos os jogos
            sistema.carregar_jogos('dataset.csv')

        # ---- opcao 2: listar jogos ----
        elif opcao == '2':
            # Exibe lista completa de jogos do catalogo
            if len(sistema.catalogo) == 0:
                print("\n  Catalogo vazio. Carregue o dataset primeiro.")
            else:
                sistema.listar_jogos()

        # ---- opcao 3: buscar por nome ----
        elif opcao == '3':
            # Usuario digita parte do nome e sistema procura
            termo = input("  Digite o nome (ou parte do nome): ").strip()
            resultado = sistema.buscar_jogo_por_nome(termo)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado com '{termo}'.")
            else:
                print(f"\n  {len(resultado)} resultado(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        # ---- opcao 4: filtrar por genero ----
        elif opcao == '4':
            # Usuario digita genero e sistema filtra
            genero = input("  Digite o genero: ").strip()
            resultado = sistema.filtrar_por_genero(genero)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado com genero '{genero}'.")
            else:
                print(f"\n  {len(resultado)} jogo(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        # ---- opcao 5: filtrar por console ----
        elif opcao == '5':
            # Usuario digita console e sistema filtra
            console = input("  Digite o console: ").strip()
            resultado = sistema.filtrar_por_console(console)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado para o console '{console}'.")
            else:
                print(f"\n  {len(resultado)} jogo(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        # ---- opcao 6: filtrar por nota ----
        elif opcao == '6':
            # Usuario digita nota minima e sistema filtra
            try:
                nota = float(input("  Nota minima (ex: 7.5): "))
                resultado = sistema.filtrar_por_nota(nota)
                print(f"\n  {len(resultado)} jogo(s) com nota >= {nota}:")
                sistema.listar_jogos(resultado)
            except:
                print("\n  [ERRO] Nota invalida.")

        # ---- opcao 7: ordenar catalogo ----
        elif opcao == '7':
            # Usuario escolhe criterio de ordenacao
            print("\n  Ordenar por:")
            print("  1. Titulo")
            print("  2. Nota")
            print("  3. Vendas (Total)")
            print("  4. Vendas NA")
            print("  5. Vendas JP")
            print("  6. Vendas PAL")
            print("  7. Outras vendas")
            print("  8. Data")
            print("  9. Console")
            print("  10. Genero")
            sub = input("  Escolha: ").strip()

            # Mapeia escolha numerica para criterio de ordenacao
            mapa = {
                '1': 'titulo',
                '2': 'nota',
                '3': 'vendas',
                '4': 'na_sales',
                '5': 'jp_sales',
                '6': 'pal_sales',
                '7': 'other_sales',
                '8': 'data',
                '9': 'console',
                '10': 'genero'
            }

            if sub in mapa:
                criterio = mapa[sub]
                print(f"\n  Ordenando por {criterio}... (pode demorar em datasets grandes)")
                resultado = sistema.ordenar_jogos(criterio)
                sistema.listar_jogos(resultado)
            else:
                print("\n  Opcao invalida.")

        # ---- opcao 8: adicionar ao backlog ----
        elif opcao == '8':
            # Usuario digita ID do jogo para adicionar a fila
            try:
                id_jogo = int(input("  Digite o ID do jogo: "))
                sistema.adicionar_ao_backlog(id_jogo)
            except:
                print("\n  [ERRO] ID invalido.")

        # ---- opcao 9: ver backlog ----
        elif opcao == '9':
            # Exibe a fila de jogos a jogar
            sistema.mostrar_backlog()

        # ---- opcao 10: jogar proximo do backlog ----
        elif opcao == '10':
            # Remove proximo jogo da fila e inicia sessao
            sistema.jogar_proximo()

        # ---- opcao 11: ver jogos recentes ----
        elif opcao == '11':
            # Exibe pilha de jogos recentes
            sistema.mostrar_recentes()

        # ---- opcao 12: retomar ultimo jogo ----
        elif opcao == '12':
            # Retoma o ultimo jogo jogado (topo da pilha)
            sistema.retomar_ultimo_jogo()

        # ---- opcao 13: registrar tempo de jogo ----
        elif opcao == '13':
            # Usuario registra tempo jogado em um jogo especifico
            try:
                id_jogo = int(input("  Digite o ID do jogo: "))
                if id_jogo not in sistema.jogos_por_id:
                    print("\n  [ERRO] Jogo nao encontrado.")
                else:
                    tempo = float(input("  Quantas horas voce jogou? "))
                    jogo = sistema.jogos_por_id[id_jogo]
                    sistema.registrar_sessao(jogo, tempo)
            except:
                print("\n  [ERRO] Entrada invalida.")

        # ---- opcao 14: ver historico completo ----
        elif opcao == '14':
            # Exibe todas as sessoes registradas
            sistema.mostrar_historico()

        # ---- opcao 15: ver recomendacoes ----
        elif opcao == '15':
            # Gera recomendacoes personalizadas
            sistema.recomendar_jogos()

        # ---- opcao 16: ver ranking pessoal ----
        elif opcao == '16':
            # Exibe rankings: jogos, generos, consoles, etc
            sistema.gerar_ranking_pessoal()

        # ---- opcao 17: ver dashboard ----
        elif opcao == '17':
            # Exibe painel com estatisticas gerais
            sistema.exibir_dashboard()

        # ---- opcao 18: salvar backlog ----
        elif opcao == '18':
            # Salva backlog em arquivo
            sistema.salvar_tudo()

        # ---- opcao 19: sair ----
        elif opcao == '19':
            # Salva dados e fecha o programa
            print("\n  Salvando dados antes de sair...")
            sistema.salvar_tudo()
            print("\n  Ate mais!")
            break

        else:
            print("\n  [AVISO] Opcao invalida. Tente novamente.")

        input("\n  Pressione Enter para continuar...")
