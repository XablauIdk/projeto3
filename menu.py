from steampy import SteamPy


def menu(sistema):

    while True:
        print(f"\n{'='*50}")
        print(f"       STEAMPY - Menu Principal")
        print(f"{'='*50}")
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

        if opcao == '1':
            sistema.carregar_jogos('dataset.csv')

        elif opcao == '2':
            if len(sistema.catalogo) == 0:
                print("\n  Catalogo vazio. Carregue o dataset primeiro.")
            else:
                sistema.listar_jogos()

        elif opcao == '3':
            termo = input("  Digite o nome (ou parte do nome): ").strip()
            resultado = sistema.buscar_jogo_por_nome(termo)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado com '{termo}'.")
            else:
                print(f"\n  {len(resultado)} resultado(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        elif opcao == '4':
            genero = input("  Digite o genero: ").strip()
            resultado = sistema.filtrar_por_genero(genero)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado com genero '{genero}'.")
            else:
                print(f"\n  {len(resultado)} jogo(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        elif opcao == '5':
            console = input("  Digite o console: ").strip()
            resultado = sistema.filtrar_por_console(console)
            if len(resultado) == 0:
                print(f"\n  Nenhum jogo encontrado para o console '{console}'.")
            else:
                print(f"\n  {len(resultado)} jogo(s) encontrado(s):")
                sistema.listar_jogos(resultado)

        elif opcao == '6':
            try:
                nota = float(input("  Nota minima (ex: 7.5): "))
                resultado = sistema.filtrar_por_nota(nota)
                print(f"\n  {len(resultado)} jogo(s) com nota >= {nota}:")
                sistema.listar_jogos(resultado)
            except:
                print("\n  [ERRO] Nota invalida.")

        elif opcao == '7':
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

        elif opcao == '8':
            try:
                id_jogo = int(input("  Digite o ID do jogo: "))
                sistema.adicionar_ao_backlog(id_jogo)
            except:
                print("\n  [ERRO] ID invalido.")

        elif opcao == '9':
            sistema.mostrar_backlog()

        elif opcao == '10':
            sistema.jogar_proximo()

        elif opcao == '11':
            sistema.mostrar_recentes()

        elif opcao == '12':
            sistema.retomar_ultimo_jogo()

        elif opcao == '13':
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

        elif opcao == '14':
            sistema.mostrar_historico()

        elif opcao == '15':
            sistema.recomendar_jogos()

        elif opcao == '16':
            sistema.gerar_ranking_pessoal()

        elif opcao == '17':
            sistema.exibir_dashboard()

        elif opcao == '18':
            sistema.salvar_tudo()

        elif opcao == '19':
            print("\n  Salvando dados antes de sair...")
            sistema.salvar_tudo()
            print("\n  Ate mais!")
            break

        else:
            print("\n  [AVISO] Opcao invalida. Tente novamente.")

        input("\n  Pressione Enter para continuar...")