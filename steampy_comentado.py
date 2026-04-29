# ============================================================
# steampy.py - Classe principal do sistema SteamPy
# ============================================================
# Classe SteamPy: gerencia todo o sistema de jogos
# Responsabilidades:
# - Carregar e armazenar catalogo de jogos
# - Gerenciar backlog (fila de jogos a jogar)
# - Gerenciar recentes (pilha de jogos jogados)
# - Registrar sessoes e historico
# - Gerar recomendacoes
# - Criar rankings e dashboard
# - Salvar e carregar dados em arquivos

import csv
import os

from modelos import Jogo, SessaoJogo
from estruturas import FilaBacklog, PilhaRecentes


class SteamPy:
    # Classe principal que controla toda a plataforma

    def __init__(self):
        # Inicializa o sistema SteamPy com estruturas vazias

        self.catalogo = []          # lista de objetos Jogo carregados do dataset
        self.jogos_por_id = {}      # dicionario id -> Jogo para acesso rapido
        self.backlog = FilaBacklog()  # fila de jogos a jogar
        self.recentes = PilhaRecentes()  # pilha de jogos recentes
        self.historico = []         # lista de SessaoJogo (todas as sessoes)
        self.tempos_por_jogo = {}   # dicionario id -> tempo total acumulado de cada jogo

    # --------------------------------------------------------
    # CARREGAR JOGOS
    # --------------------------------------------------------

    def carregar_jogos(self, nome_arquivo):
        # Carrega os jogos do arquivo dataset.csv
        # - Abre o arquivo
        # - Le linha por linha
        # - Converte cada linha em um objeto Jogo
        # - Armazena em lista e dicionario para acesso rapido
        # Parametro: nome_arquivo - caminho do arquivo CSV

        if not os.path.exists(nome_arquivo):
            print(f"[ERRO] Arquivo '{nome_arquivo}' nao encontrado!")
            return

        self.catalogo = []  # Limpa catalogo anterior
        self.jogos_por_id = {}  # Limpa dicionario anterior
        contador = 0  # Contador de IDs

        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)  # Le o CSV com cabecalho
                for linha in leitor:
                    try:
                        contador += 1

                        # Converte campo critic_score para float, com tratamento de erro
                        try:
                            nota = float(linha.get('critic_score', 0) or 0)
                        except:
                            nota = 0.0

                        # Converte vendas totais para float
                        try:
                            total = float(linha.get('total_sales', 0) or 0)
                        except:
                            total = 0.0

                        # Converte vendas NA (America do Norte) para float
                        try:
                            na = float(linha.get('na_sales', 0) or 0)
                        except:
                            na = 0.0

                        # Converte vendas JP (Japao) para float
                        try:
                            jp = float(linha.get('jp_sales', 0) or 0)
                        except:
                            jp = 0.0

                        # Converte vendas PAL (Europa) para float
                        try:
                            pal = float(linha.get('pal_sales', 0) or 0)
                        except:
                            pal = 0.0

                        # Converte outras vendas para float
                        try:
                            other = float(linha.get('other_sales', 0) or 0)
                        except:
                            other = 0.0

                        # Cria um novo objeto Jogo com os dados da linha
                        jogo = Jogo(
                            id=contador,  # ID sequencial
                            titulo=linha.get('title', 'Desconhecido').strip(),
                            console=linha.get('console', '').strip(),
                            genero=linha.get('genre', '').strip(),
                            publisher=linha.get('publisher', '').strip(),
                            developer=linha.get('developer', '').strip(),
                            critic_score=nota,
                            total_sales=total,
                            na_sales=na,
                            jp_sales=jp,
                            pal_sales=pal,
                            other_sales=other,
                            release_date=linha.get('release_date', '').strip()
                        )

                        # Adiciona o jogo na lista e no dicionario
                        self.catalogo.append(jogo)
                        self.jogos_por_id[contador] = jogo

                    except Exception:
                        continue  # Pula linhas com erro

            print(f"\n{len(self.catalogo)} jogos carregados com sucesso!")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel abrir o arquivo: {e}")

    # --------------------------------------------------------
    # LISTAGEM E BUSCA
    # --------------------------------------------------------

    def listar_jogos(self, lista=None):
        # Exibe uma lista de jogos de forma paginada
        # Mostra 30 jogos por pagina para facilitar leitura

        if lista is None:
            lista = self.catalogo  # Usa catalogo completo se nao informado

        if len(lista) == 0:
            print("\nNenhum jogo para mostrar.")
            return

        total = len(lista)  # Total de jogos a exibir
        pagina = 30       # Quantos jogos mostrar por vez
        inicio = 0        # Indice de inicio da pagina atual

        while inicio < total:
            fim = inicio + pagina  # Calcula fim da pagina
            if fim > total:
                fim = total

            # Exibe cabecalho da tabela com informacoes do jogo
            print(f"\n{'='*100}")
            print(f"{'ID':<5} {'Titulo':<28} {'Cons':<6} {'Nota':<5} {'Tot':<6} {'NA':<6} {'JP':<6} {'PAL':<6} {'Out':<6} {'Data':<10}")
            print(f"{'='*100}")

            # Exibe os jogos da pagina atual formatados em colunas
            for jogo in lista[inicio:fim]:
                titulo_curto = jogo.titulo[:26] if len(jogo.titulo) > 26 else jogo.titulo
                print(f"{jogo.id:<5} {titulo_curto:<28} {jogo.console:<6} "
                      f"{jogo.critic_score:<5.1f} {jogo.total_sales:<6.2f} "
                      f"{jogo.na_sales:<6.2f} {jogo.jp_sales:<6.2f} "
                      f"{jogo.pal_sales:<6.2f} {jogo.other_sales:<6.2f} "
                      f"{jogo.release_date:<10}")

            print(f"{'='*100}")
            print(f"Mostrando {inicio+1} a {fim} de {total} jogo(s)")

            # Se ainda tem mais jogos, pergunta se quer continuar
            if fim < total:
                continuar = input("  Ver proximos 30? (s/n): ").strip().lower()
                if continuar != 's':
                    break

            inicio += pagina  # Passa para proxima pagina

    def buscar_jogo_por_nome(self, termo):
        # Busca jogos pelo nome (busca parcial, nao precisa ser exato)
        # Retorna lista de todos os jogos que contem o termo no titulo

        resultado = []
        termo_lower = termo.lower()  # Converte para minuscula (case-insensitive)
        for jogo in self.catalogo:
            # Verifica se o termo esta contido no titulo
            if termo_lower in jogo.titulo.lower():
                resultado.append(jogo)
        return resultado

    # --------------------------------------------------------
    # FILTROS
    # --------------------------------------------------------

    def filtrar_por_genero(self, genero):
        # Filtra e retorna todos os jogos de um genero especifico
        resultado = []
        genero_lower = genero.lower()
        for jogo in self.catalogo:
            if genero_lower in jogo.genero.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_console(self, console):
        # Filtra e retorna todos os jogos de uma plataforma especifica
        resultado = []
        console_lower = console.lower()
        for jogo in self.catalogo:
            if console_lower in jogo.console.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_nota(self, nota_minima):
        # Filtra jogos com nota critica igual ou acima do valor informado
        resultado = []
        for jogo in self.catalogo:
            if jogo.critic_score >= nota_minima:
                resultado.append(jogo)
        return resultado

    def filtrar_por_vendas(self, vendas_minimas):
        # Filtra jogos com vendas totais acima do valor informado (em milhoes)
        resultado = []
        for jogo in self.catalogo:
            if jogo.total_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_publisher(self, publisher):
        # Filtra jogos publicados por uma empresa especifica
        resultado = []
        pub_lower = publisher.lower()
        for jogo in self.catalogo:
            if pub_lower in jogo.publisher.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_na_sales(self, vendas_minimas):
        # Filtra jogos com vendas minimas na America do Norte
        resultado = []
        for jogo in self.catalogo:
            if jogo.na_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_jp_sales(self, vendas_minimas):
        # Filtra jogos com vendas minimas no Japao
        resultado = []
        for jogo in self.catalogo:
            if jogo.jp_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_pal_sales(self, vendas_minimas):
        # Filtra jogos com vendas minimas na Europa (regiao PAL)
        resultado = []
        for jogo in self.catalogo:
            if jogo.pal_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_other_sales(self, vendas_minimas):
        # Filtra jogos com outras vendas minimas
        resultado = []
        for jogo in self.catalogo:
            if jogo.other_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_ano(self, ano):
        # Filtra jogos lancados em um ano especifico
        resultado = []
        ano_str = str(ano)
        for jogo in self.catalogo:
            if jogo.release_date.startswith(ano_str):
                resultado.append(jogo)
        return resultado

    # --------------------------------------------------------
    # ORDENACAO
    # --------------------------------------------------------

    def ordenar_jogos(self, criterio):
        # Ordena a lista de jogos por um criterio especificado
        # Usa Bubble Sort (algoritmo simples de ordenacao)
        # Retorna nova lista ordenada sem alterar catalogo original

        lista = list(self.catalogo)  # Faz copia para nao alterar catalogo original
        n = len(lista)

        # Ordena por titulo em ordem alfabetica crescente
        if criterio == "titulo":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].titulo.lower() > lista[j+1].titulo.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por nota em ordem decrescente (maior nota primeiro)
        elif criterio == "nota":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].critic_score < lista[j+1].critic_score:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por vendas totais em ordem decrescente
        elif criterio == "vendas":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].total_sales < lista[j+1].total_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por vendas NA em ordem decrescente
        elif criterio == "na_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].na_sales < lista[j+1].na_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por vendas JP em ordem decrescente
        elif criterio == "jp_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].jp_sales < lista[j+1].jp_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por vendas PAL em ordem decrescente
        elif criterio == "pal_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].pal_sales < lista[j+1].pal_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por outras vendas em ordem decrescente
        elif criterio == "other_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].other_sales < lista[j+1].other_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por data de lancamento em ordem crescente
        elif criterio == "data":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].release_date > lista[j+1].release_date:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por console em ordem alfabetica crescente
        elif criterio == "console":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].console.lower() > lista[j+1].console.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        # Ordena por genero em ordem alfabetica crescente
        elif criterio == "genero":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].genero.lower() > lista[j+1].genero.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        else:
            print("[AVISO] Criterio de ordenacao invalido.")
            return self.catalogo

        return lista

    # --------------------------------------------------------
    # BACKLOG (FILA)
    # --------------------------------------------------------

    def adicionar_ao_backlog(self, id_jogo):
        # Adiciona um jogo ao backlog (fila de jogos a jogar)
        # Funciona como FIFO - primeiro a entrar, primeiro a sair

        if id_jogo not in self.jogos_por_id:
            print(f"\n[ERRO] Jogo com ID {id_jogo} nao encontrado.")
            return

        jogo = self.jogos_por_id[id_jogo]

        # Verifica se jogo ja esta no backlog para evitar duplicatas
        for j in self.backlog.mostrar():
            if j.id == id_jogo:
                print(f"\n[AVISO] '{jogo.titulo}' ja esta no backlog!")
                return

        # Adiciona o jogo no final da fila
        self.backlog.enqueue(jogo)
        print(f"\n'{jogo.titulo}' adicionado ao backlog!")

    def mostrar_backlog(self):
        # Exibe todos os jogos no backlog em ordem FIFO
        # Mostra quantos jogos estao esperando para serem jogados

        lista = self.backlog.mostrar()
        if len(lista) == 0:
            print("\nBacklog vazio.")
            return

        print(f"\n{'='*50}")
        print(f"  BACKLOG ({self.backlog.tamanho()} jogo(s))")
        print(f"{'='*50}")
        posicao = 1
        for jogo in lista:
            print(f"  {posicao}. {jogo.titulo} | {jogo.console}")
            posicao += 1
        print(f"{'='*50}")

    def jogar_proximo(self):
        # Remove o proximo jogo da fila e inicia uma sessao de jogo
        # Usuario informa quantas horas jogou

        if self.backlog.is_empty():
            print("\nBacklog vazio! Adicione jogos primeiro.")
            return

        # Retira o primeiro jogo da fila (FIFO)
        jogo = self.backlog.dequeue()
        print(f"\nJogando: {jogo.titulo} | {jogo.console}")

        # Pede para usuario informar tempo jogado
        try:
            tempo = float(input("  Quantas horas voce jogou? "))
        except:
            tempo = 1.0  # Valor padrao se usuario nao digitar numero valido

        # Registra a sessao
        self.registrar_sessao(jogo, tempo)

    def salvar_backlog(self):
        # Salva o backlog em arquivo para persistencia de dados
        # Formato: id;titulo;console

        try:
            with open('backlog.txt', 'w', encoding='utf-8') as f:
                for jogo in self.backlog.mostrar():
                    f.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")
            print("\nBacklog salvo em 'backlog.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar o backlog: {e}")

    def carregar_backlog(self):
        # Carrega o backlog do arquivo backlog.txt (se existir)
        # Reconstroi a fila com os jogos que o usuario havia salvo

        if not os.path.exists('backlog.txt'):
            return

        try:
            with open('backlog.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            carregados = 0
            for linha in linhas:
                linha = linha.strip()
                if linha == '':
                    continue
                partes = linha.split(';')
                if len(partes) >= 1:
                    try:
                        id_jogo = int(partes[0])
                        if id_jogo in self.jogos_por_id:
                            ja_tem = False
                            for j in self.backlog.mostrar():
                                if j.id == id_jogo:
                                    ja_tem = True
                                    break
                            if not ja_tem:
                                self.backlog.enqueue(self.jogos_por_id[id_jogo])
                                carregados += 1
                    except:
                        continue

            if carregados > 0:
                print(f"Backlog carregado: {carregados} jogo(s).")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel carregar o backlog: {e}")

    # --------------------------------------------------------
    # SESSOES E HISTORICO
    # --------------------------------------------------------

    def registrar_sessao(self, jogo, tempo):
        # Registra uma sessao de jogo do usuario
        # Atualiza tempo total acumulado do jogo
        # Adiciona jogo aos recentes para acesso rapido

        # Cria nova sessao
        sessao = SessaoJogo(jogo, tempo)
        self.historico.append(sessao)  # Adiciona ao historico completo

        # Atualiza tempo total acumulado deste jogo
        if jogo.id in self.tempos_por_jogo:
            self.tempos_por_jogo[jogo.id] += tempo
        else:
            self.tempos_por_jogo[jogo.id] = tempo

        # Adiciona jogo a pilha de recentes (para retomar depois)
        self.recentes.push(jogo)

        # Exibe confirmacao ao usuario
        print(f"\n  Sessao registrada!")
        print(f"  Status: {sessao.status}")
        print(f"  Tempo total em '{jogo.titulo}': {self.tempos_por_jogo[jogo.id]:.1f}h")

    def mostrar_historico(self):
        # Exibe o historico completo de todas as sessoes registradas
        # Mostra cada sessao com detalhes

        if len(self.historico) == 0:
            print("\nNenhuma sessao registrada ainda.")
            return

        print(f"\n{'='*70}")
        print(f"  HISTORICO COMPLETO ({len(self.historico)} sessao(oes))")
        print(f"{'='*70}")
        for i, sessao in enumerate(self.historico):
            print(f"  {i+1}. {sessao}")
        print(f"{'='*70}")

    def salvar_historico(self):
        # Salva o historico em arquivo para persistencia
        # Preserva todas as sessoes registradas
        # Formato: titulo;tempo_sessao;tempo_total;status

        try:
            with open('historico_jogo.txt', 'w', encoding='utf-8') as f:
                for sessao in self.historico:
                    # Pega o tempo total acumulado do jogo
                    tempo_total = self.tempos_por_jogo.get(sessao.jogo.id, sessao.tempo_jogado)
                    f.write(f"{sessao.jogo.titulo};{sessao.tempo_jogado};"
                            f"{tempo_total};{sessao.status}\n")
            print("\nHistorico salvo em 'historico_jogo.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar o historico: {e}")

    def carregar_historico(self):
        # Carrega o historico do arquivo historico_jogo.txt (se existir)
        # Reconstroi o historico com as sessoes que o usuario havia jogado

        if not os.path.exists('historico_jogo.txt'):
            return

        try:
            with open('historico_jogo.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            # Cria dicionario de titulo -> jogo para busca mais rapida
            jogos_por_titulo = {}
            for jogo in self.catalogo:
                jogos_por_titulo[jogo.titulo] = jogo

            carregados = 0
            for linha in linhas:
                linha = linha.strip()
                if linha == '':
                    continue
                # Formato esperado: titulo;tempo_sessao;tempo_total;status
                partes = linha.split(';')
                if len(partes) >= 3:
                    try:
                        titulo = partes[0]
                        tempo_sessao = float(partes[1])
                        tempo_total = float(partes[2])
                        status = partes[3] if len(partes) >= 4 else 'Iniciado'

                        # Busca o jogo pelo titulo
                        if titulo in jogos_por_titulo:
                            jogo = jogos_por_titulo[titulo]
                            sessao = SessaoJogo(jogo, tempo_sessao)
                            sessao.status = status

                            self.historico.append(sessao)

                            # Restaura o tempo total acumulado salvo
                            self.tempos_por_jogo[jogo.id] = tempo_total

                            carregados += 1
                    except:
                        continue

            if carregados > 0:
                print(f"Historico carregado: {carregados} sessao(oes).")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel carregar o historico: {e}")

    # --------------------------------------------------------
    # RECENTES (PILHA)
    # --------------------------------------------------------

    def mostrar_recentes(self):
        # Exibe os jogos recentes em ordem LIFO (mais recente primeiro)
        # Facilita o retorno rapido aos ultimos jogos jogados

        lista = self.recentes.mostrar()
        if len(lista) == 0:
            print("\nNenhum jogo recente ainda.")
            return

        print(f"\n{'='*50}")
        print(f"  JOGOS RECENTES ({self.recentes.tamanho()} jogo(s))")
        print(f"{'='*50}")
        for i, jogo in enumerate(lista):
            print(f"  {i+1}. {jogo.titulo} | {jogo.console}")
        print(f"{'='*50}")

    def retomar_ultimo_jogo(self):
        # Retoma o ultimo jogo jogado (topo da pilha)
        # Usuario pode registrar mais tempo jogado neste jogo

        jogo = self.recentes.topo()
        if jogo is None:
            print("\nNenhum jogo recente para retomar.")
            return

        print(f"\nRetomando: {jogo.titulo} | {jogo.console}")
        try:
            tempo = float(input("  Quantas horas voce jogou agora? "))
        except:
            tempo = 1.0

        # Registra nova sessao para continuar o jogo
        self.registrar_sessao(jogo, tempo)

    def salvar_recentes(self):
        # Salva os jogos recentes em arquivo para persistencia
        # Preserva a ordem da pilha
        # Formato: id;titulo;console

        try:
            with open('recentes.txt', 'w', encoding='utf-8') as f:
                lista_interna = self.recentes._pilha
                for jogo in lista_interna:
                    f.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")
            print("\nRecentes salvos em 'recentes.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar os recentes: {e}")

    def carregar_recentes(self):
        # Carrega os jogos recentes do arquivo recentes.txt (se existir)
        # Reconstroi a pilha com os ultimos jogos que o usuario havia jogado

        if not os.path.exists('recentes.txt'):
            return

        try:
            with open('recentes.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            carregados = 0
            for linha in linhas:
                linha = linha.strip()
                if linha == '':
                    continue
                partes = linha.split(';')
                if len(partes) >= 1:
                    try:
                        id_jogo = int(partes[0])
                        if id_jogo in self.jogos_por_id:
                            self.recentes.push(self.jogos_por_id[id_jogo])
                            carregados += 1
                    except:
                        continue

            if carregados > 0:
                print(f"Recentes carregados: {carregados} jogo(s).")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel carregar os recentes: {e}")

    # --------------------------------------------------------
    # RECOMENDACOES
    # --------------------------------------------------------

    def recomendar_jogos(self):
        # Gera recomendacoes personalizadas baseado no historico do usuario
        # Considera: genero favorito, console favorito, nota minima
        # Evita sugerir jogos ja jogados ou no backlog

        if len(self.historico) == 0:
            print("\nJogue alguns jogos primeiro para receber recomendacoes!")
            return

        # PASSO 1: Analisa o historico do usuario
        # Conta quantas vezes cada genero e console foi jogado
        contagem_genero = {}
        contagem_console = {}
        for sessao in self.historico:
            g = sessao.jogo.genero
            c = sessao.jogo.console
            if g in contagem_genero:
                contagem_genero[g] += 1
            else:
                contagem_genero[g] = 1
            if c in contagem_console:
                contagem_console[c] += 1
            else:
                contagem_console[c] = 1

        # PASSO 2: Identifica genero e console favoritos
        # Genero favorito: aquele que mais aparece no historico
        genero_fav = ''
        maior = 0
        for g, qtd in contagem_genero.items():
            if qtd > maior:
                maior = qtd
                genero_fav = g

        # Console favorito: aquele que mais aparece no historico
        console_fav = ''
        maior = 0
        for c, qtd in contagem_console.items():
            if qtd > maior:
                maior = qtd
                console_fav = c

        # PASSO 3: Cria lista de IDs para evitar recomendacoes repetidas
        # IDs dos jogos ja jogados (nao recomenda)
        ids_jogados = {}
        for sessao in self.historico:
            ids_jogados[sessao.jogo.id] = True

        # IDs dos jogos no backlog (nao recomenda)
        ids_backlog = {}
        for j in self.backlog.mostrar():
            ids_backlog[j.id] = True

        print(f"\n{'='*60}")
        print(f"  RECOMENDACOES PERSONALIZADAS")
        print(f"{'='*60}")
        print(f"  Criterios utilizados:")
        print(f"  - Genero favorito : {genero_fav}")
        print(f"  - Console favorito: {console_fav}")
        print(f"  - Nota minima     : 8.0")
        print(f"  - Excluindo jogos ja jogados e no backlog")
        print(f"{'='*60}")

        recomendados = []

        # PASSO 4: Recomendacoes em 3 niveis de relevancia
        # 1a passagem: genero FAVORITO + console FAVORITO + nota >= 8
        # (Mais relevante - combina preferencias)
        for jogo in self.catalogo:
            if jogo.id in ids_jogados:
                continue
            if jogo.id in ids_backlog:
                continue
            if (jogo.genero == genero_fav and
                    jogo.console == console_fav and
                    jogo.critic_score >= 8):
                recomendados.append(jogo)

        # 2a passagem: mesmo genero FAVORITO + nota >= 8 (qualquer console)
        # (Menos especifico que a primeira)
        if len(recomendados) < 5:
            for jogo in self.catalogo:
                if jogo.id in ids_jogados:
                    continue
                if jogo.id in ids_backlog:
                    continue
                ja_tem = False
                for r in recomendados:
                    if r.id == jogo.id:
                        ja_tem = True
                        break
                if not ja_tem and jogo.genero == genero_fav and jogo.critic_score >= 8:
                    recomendados.append(jogo)

        # 3a passagem: qualquer genero, nota >= 8
        # (Menos especifico - apenas por qualidade)
        if len(recomendados) < 5:
            for jogo in self.catalogo:
                if jogo.id in ids_jogados:
                    continue
                if jogo.id in ids_backlog:
                    continue
                ja_tem = False
                for r in recomendados:
                    if r.id == jogo.id:
                        ja_tem = True
                        break
                if not ja_tem and jogo.critic_score >= 8:
                    recomendados.append(jogo)
                if len(recomendados) >= 10:
                    break

        # PASSO 5: Exibe as recomendacoes
        if len(recomendados) == 0:
            print("\n  Nenhuma recomendacao encontrada com esses criterios.")
        else:
            # Exibe ate 10 recomendacoes
            print(f"\n  {len(recomendados[:10])} jogo(s) recomendado(s):\n")
            for i, jogo in enumerate(recomendados[:10]):
                print(f"  {i+1}. [{jogo.id}] {jogo.titulo}")
                print(f"      Console: {jogo.console} | Genero: {jogo.genero}")
                print(f"      Nota: {jogo.critic_score} | Vendas: {jogo.total_sales}M")
                print()

    # --------------------------------------------------------
    # RANKING PESSOAL
    # --------------------------------------------------------

    def gerar_ranking_pessoal(self):
        # Gera ranking pessoal baseado no comportamento do usuario
        # Mostra: jogos mais jogados, generos favoritos, consoles favoritos, etc

        if len(self.historico) == 0:
            print("\nNenhum jogo jogado ainda.")
            return

        print(f"\n{'='*60}")
        print(f"  RANKING PESSOAL")
        print(f"{'='*60}")

        # RANKING 1: Jogos mais jogados (por tempo acumulado)
        # Cria lista com tempo total de cada jogo
        lista_tempo = []
        for id_jogo, tempo in self.tempos_por_jogo.items():
            if id_jogo in self.jogos_por_id:
                lista_tempo.append((self.jogos_por_id[id_jogo], tempo))

        # Ordena jogos por tempo descrescente usando bubble sort
        n = len(lista_tempo)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_tempo[j][1] < lista_tempo[j+1][1]:
                    lista_tempo[j], lista_tempo[j+1] = lista_tempo[j+1], lista_tempo[j]

        # Exibe top 5 jogos mais jogados
        print("\n  Jogos mais jogados:")
        for i, (jogo, tempo) in enumerate(lista_tempo[:5]):
            print(f"  {i+1}. {jogo.titulo} - {tempo:.1f}h")

        # RANKING 2: Generos mais jogados (por horas totais)
        # Calcula horas totais por genero
        contagem_genero = {}
        for sessao in self.historico:
            g = sessao.jogo.genero
            if g in contagem_genero:
                contagem_genero[g] += sessao.tempo_jogado
            else:
                contagem_genero[g] = sessao.tempo_jogado

        # Cria lista com generos e horas totais
        lista_genero = []
        for g, t in contagem_genero.items():
            lista_genero.append((g, t))

        # Ordena generos por horas descrescente
        n = len(lista_genero)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_genero[j][1] < lista_genero[j+1][1]:
                    lista_genero[j], lista_genero[j+1] = lista_genero[j+1], lista_genero[j]

        # Exibe top 5 generos mais jogados
        print("\n  Generos mais jogados:")
        for i, (g, t) in enumerate(lista_genero[:5]):
            print(f"  {i+1}. {g} - {t:.1f}h")

        # RANKING 3: Consoles mais jogados (por horas totais)
        # Calcula horas totais por console
        contagem_console = {}
        for sessao in self.historico:
            c = sessao.jogo.console
            if c in contagem_console:
                contagem_console[c] += sessao.tempo_jogado
            else:
                contagem_console[c] = sessao.tempo_jogado

        # Cria lista com consoles e horas totais
        lista_console = []
        for c, t in contagem_console.items():
            lista_console.append((c, t))

        # Ordena consoles por horas descrescente
        n = len(lista_console)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_console[j][1] < lista_console[j+1][1]:
                    lista_console[j], lista_console[j+1] = lista_console[j+1], lista_console[j]

        # Exibe top 5 consoles mais jogados
        print("\n  Consoles mais jogados:")
        for i, (c, t) in enumerate(lista_console[:5]):
            print(f"  {i+1}. {c} - {t:.1f}h")

        # RANKING 4: Melhores notas (jogos que usuario jogou)
        # Coleta jogos unicos com suas notas
        ids_vistos = {}
        lista_notas = []
        for sessao in self.historico:
            if sessao.jogo.id not in ids_vistos:
                ids_vistos[sessao.jogo.id] = True
                lista_notas.append(sessao.jogo)

        # Ordena jogos por nota descrescente
        n = len(lista_notas)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_notas[j].critic_score < lista_notas[j+1].critic_score:
                    lista_notas[j], lista_notas[j+1] = lista_notas[j+1], lista_notas[j]

        # Exibe top 5 jogos com melhor nota que usuario jogou
        print("\n  Melhores notas (jogos que voce jogou):")
        for i, jogo in enumerate(lista_notas[:5]):
            print(f"  {i+1}. {jogo.titulo} - Nota: {jogo.critic_score}")

        print(f"\n{'='*60}")

    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    def exibir_dashboard(self):
        # Exibe um painel (dashboard) com estatisticas gerais do usuario
        # Similar aos dashboards de plataformas reais como Steam

        # CALCULO 1: Sessoes e tempo total
        # Total de sessoes jogadas
        total_sessoes = len(self.historico)

        # Tempo total jogado em horas
        tempo_total = 0.0
        for sessao in self.historico:
            tempo_total += sessao.tempo_jogado

        # Media de horas por sessao
        media_horas = 0.0
        if total_sessoes > 0:
            media_horas = tempo_total / total_sessoes

        # CALCULO 2: Jogo mais jogado
        # Encontra jogo com maior tempo total acumulado
        jogo_mais_jogado = None
        maior_tempo = 0
        for id_jogo, tempo in self.tempos_por_jogo.items():
            if tempo > maior_tempo:
                maior_tempo = tempo
                if id_jogo in self.jogos_por_id:
                    jogo_mais_jogado = self.jogos_por_id[id_jogo]

        # CALCULO 3: Preferencias (genero, console, nota media)
        # Coleta dados sobre preferencias do usuario
        contagem_g = {}
        contagem_c = {}
        soma_notas = 0.0
        qtd_notas = 0

        for sessao in self.historico:
            g = sessao.jogo.genero
            c = sessao.jogo.console
            if g in contagem_g:
                contagem_g[g] += 1
            else:
                contagem_g[g] = 1
            if c in contagem_c:
                contagem_c[c] += 1
            else:
                contagem_c[c] = 1
            if sessao.jogo.critic_score > 0:
                soma_notas += sessao.jogo.critic_score
                qtd_notas += 1

        # Encontra genero favorito
        genero_fav = '-'
        maior = 0
        for g, q in contagem_g.items():
            if q > maior:
                maior = q
                genero_fav = g

        # Encontra console favorito
        console_fav = '-'
        maior = 0
        for c, q in contagem_c.items():
            if q > maior:
                maior = q
                console_fav = c

        # Calcula nota media dos jogos jogados
        nota_media = 0.0
        if qtd_notas > 0:
            nota_media = soma_notas / qtd_notas

        # CALCULO 4: Status dos jogos
        # Conta quantos jogos estao em cada status
        iniciados = 0
        em_andamento = 0
        concluidos = 0
        for sessao in self.historico:
            if sessao.status == 'Iniciado':
                iniciados += 1
            elif sessao.status == 'Em andamento':
                em_andamento += 1
            elif sessao.status == 'Concluido simbolicamente':
                concluidos += 1

        # CALCULO 5: Jogos populares e bem avaliados
        # Jogo mais popular jogado (por vendas totais)
        jogo_popular = None
        maior_venda = 0
        ids_jogados = {}
        for sessao in self.historico:
            jogo = sessao.jogo
            if jogo.id not in ids_jogados:
                ids_jogados[jogo.id] = True
                if jogo.total_sales > maior_venda:
                    maior_venda = jogo.total_sales
                    jogo_popular = jogo

        # Jogo com melhor nota que usuario jogou
        jogo_melhor_nota = None
        melhor_nota = 0
        ids_vis = {}
        for sessao in self.historico:
            jogo = sessao.jogo
            if jogo.id not in ids_vis:
                ids_vis[jogo.id] = True
                if jogo.critic_score > melhor_nota:
                    melhor_nota = jogo.critic_score
                    jogo_melhor_nota = jogo

        # CALCULO 6: Recomendacoes disponiveis
        # Conta quantos jogos com nota >= 8 ainda nao foram jogados
        ids_jog_dash = {}
        for sessao in self.historico:
            ids_jog_dash[sessao.jogo.id] = True
        recomendacoes_disp = 0
        for jogo in self.catalogo:
            if jogo.id not in ids_jog_dash and jogo.critic_score >= 8:
                recomendacoes_disp += 1

        # EXIBICAO: Mostra o dashboard formatado
        print(f'\n{'='*60}')
        print(f'  DASHBOARD - STEAMPY')
        print(f'{'='*60}')
        print(f'  Total de jogos no catalogo   : {len(self.catalogo)}')
        print(f'  Total de jogos no backlog    : {self.backlog.tamanho()}')
        print(f'  Total de jogos recentes      : {self.recentes.tamanho()}')
        print(f'  Total de sessoes jogadas     : {total_sessoes}')
        print(f'  Tempo total jogado           : {tempo_total:.1f}h')
        print(f'  Media de horas por sessao    : {media_horas:.1f}h')
        print(f'{'='*60}')
        print(f'  Jogo mais jogado             : {jogo_mais_jogado.titulo if jogo_mais_jogado else "-"} ({maior_tempo:.1f}h)')
        print(f'  Genero favorito              : {genero_fav}')
        print(f'  Console favorito             : {console_fav}')
        print(f'  Nota media dos jogados       : {nota_media:.1f}')
        print(f'{'='*60}')
        print(f'  Sessoes Iniciado             : {iniciados}')
        print(f'  Sessoes Em andamento         : {em_andamento}')
        print(f'  Sessoes Concluido            : {concluidos}')
        print(f'{'='*60}')
        print(f'  Recomendacoes disponiveis    : {recomendacoes_disp}')
        print(f'  Jogo mais popular jogado     : {jogo_popular.titulo if jogo_popular else "-"} ({maior_venda:.2f}M vendas)')
        print(f'  Jogo melhor nota jogado      : {jogo_melhor_nota.titulo if jogo_melhor_nota else "-"} (nota {melhor_nota:.1f})')
        print(f'{'='*60}')

    # --------------------------------------------------------
    # SALVAR TUDO
    # --------------------------------------------------------

    def salvar_tudo(self):
        # Salva TODOS os dados do usuario em arquivos
        # Garante que nao ha perda de dados ao fechar o programa
        # Salva: backlog, historico, jogos recentes

        self.salvar_backlog()
        self.salvar_historico()
        self.salvar_recentes()
        print('\nTodos os dados foram salvos!')
