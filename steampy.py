import csv
import os

from modelos import Jogo, SessaoJogo
from estruturas import FilaBacklog, PilhaRecentes


class SteamPy:

    def __init__(self):
        self.catalogo = []
        self.jogos_por_id = {}
        self.backlog = FilaBacklog()
        self.recentes = PilhaRecentes()
        self.historico = []
        self.tempos_por_jogo = {}

    def carregar_jogos(self, nome_arquivo):
        if not os.path.exists(nome_arquivo):
            print(f"[ERRO] Arquivo '{nome_arquivo}' nao encontrado!")
            return

        self.catalogo = []
        self.jogos_por_id = {}
        contador = 0

        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                for linha in leitor:
                    try:
                        contador += 1

                        try:
                            nota = float(linha.get('critic_score', 0) or 0)
                        except:
                            nota = 0.0

                        try:
                            total = float(linha.get('total_sales', 0) or 0)
                        except:
                            total = 0.0

                        try:
                            na = float(linha.get('na_sales', 0) or 0)
                        except:
                            na = 0.0

                        try:
                            jp = float(linha.get('jp_sales', 0) or 0)
                        except:
                            jp = 0.0

                        try:
                            pal = float(linha.get('pal_sales', 0) or 0)
                        except:
                            pal = 0.0

                        try:
                            other = float(linha.get('other_sales', 0) or 0)
                        except:
                            other = 0.0

                        jogo = Jogo(
                            id=contador,
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

                        self.catalogo.append(jogo)
                        self.jogos_por_id[contador] = jogo

                    except Exception:
                        continue

            print(f"\n{len(self.catalogo)} jogos carregados com sucesso!")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel abrir o arquivo: {e}")

    def listar_jogos(self, lista=None):
        if lista is None:
            lista = self.catalogo

        if len(lista) == 0:
            print("\nNenhum jogo para mostrar.")
            return

        total = len(lista)
        pagina = 30
        inicio = 0

        while inicio < total:
            fim = inicio + pagina
            if fim > total:
                fim = total

            print(f"\n{'='*100}")
            print(f"{'ID':<5} {'Titulo':<28} {'Cons':<6} {'Nota':<5} {'Tot':<6} {'NA':<6} {'JP':<6} {'PAL':<6} {'Out':<6} {'Data':<10}")
            print(f"{'='*100}")

            for jogo in lista[inicio:fim]:
                titulo_curto = jogo.titulo[:26] if len(jogo.titulo) > 26 else jogo.titulo
                print(f"{jogo.id:<5} {titulo_curto:<28} {jogo.console:<6} "
                      f"{jogo.critic_score:<5.1f} {jogo.total_sales:<6.2f} "
                      f"{jogo.na_sales:<6.2f} {jogo.jp_sales:<6.2f} "
                      f"{jogo.pal_sales:<6.2f} {jogo.other_sales:<6.2f} "
                      f"{jogo.release_date:<10}")

            print(f"{'='*100}")
            print(f"Mostrando {inicio+1} a {fim} de {total} jogo(s)")

            if fim < total:
                continuar = input("  Ver proximos 30? (s/n): ").strip().lower()
                if continuar != 's':
                    break

            inicio += pagina

    def buscar_jogo_por_nome(self, termo):
        resultado = []
        termo_lower = termo.lower()
        for jogo in self.catalogo:
            if termo_lower in jogo.titulo.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_genero(self, genero):
        resultado = []
        genero_lower = genero.lower()
        for jogo in self.catalogo:
            if genero_lower in jogo.genero.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_console(self, console):
        resultado = []
        console_lower = console.lower()
        for jogo in self.catalogo:
            if console_lower in jogo.console.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_nota(self, nota_minima):
        resultado = []
        for jogo in self.catalogo:
            if jogo.critic_score >= nota_minima:
                resultado.append(jogo)
        return resultado

    def filtrar_por_vendas(self, vendas_minimas):
        resultado = []
        for jogo in self.catalogo:
            if jogo.total_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_publisher(self, publisher):
        resultado = []
        pub_lower = publisher.lower()
        for jogo in self.catalogo:
            if pub_lower in jogo.publisher.lower():
                resultado.append(jogo)
        return resultado

    def filtrar_por_na_sales(self, vendas_minimas):
        resultado = []
        for jogo in self.catalogo:
            if jogo.na_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_jp_sales(self, vendas_minimas):
        resultado = []
        for jogo in self.catalogo:
            if jogo.jp_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_pal_sales(self, vendas_minimas):
        resultado = []
        for jogo in self.catalogo:
            if jogo.pal_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_other_sales(self, vendas_minimas):
        resultado = []
        for jogo in self.catalogo:
            if jogo.other_sales >= vendas_minimas:
                resultado.append(jogo)
        return resultado

    def filtrar_por_ano(self, ano):
        resultado = []
        ano_str = str(ano)
        for jogo in self.catalogo:
            if jogo.release_date.startswith(ano_str):
                resultado.append(jogo)
        return resultado

    def ordenar_jogos(self, criterio):
        lista = list(self.catalogo)
        n = len(lista)

        if criterio == "titulo":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].titulo.lower() > lista[j+1].titulo.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "nota":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].critic_score < lista[j+1].critic_score:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "vendas":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].total_sales < lista[j+1].total_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "na_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].na_sales < lista[j+1].na_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "jp_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].jp_sales < lista[j+1].jp_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "pal_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].pal_sales < lista[j+1].pal_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "other_sales":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].other_sales < lista[j+1].other_sales:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "data":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].release_date > lista[j+1].release_date:
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "console":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].console.lower() > lista[j+1].console.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        elif criterio == "genero":
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j].genero.lower() > lista[j+1].genero.lower():
                        lista[j], lista[j+1] = lista[j+1], lista[j]

        else:
            print("[AVISO] Criterio de ordenacao invalido.")
            return self.catalogo

        return lista

    def adicionar_ao_backlog(self, id_jogo):
        if id_jogo not in self.jogos_por_id:
            print(f"\n[ERRO] Jogo com ID {id_jogo} nao encontrado.")
            return

        jogo = self.jogos_por_id[id_jogo]

        for j in self.backlog.mostrar():
            if j.id == id_jogo:
                print(f"\n[AVISO] '{jogo.titulo}' ja esta no backlog!")
                return

        self.backlog.enqueue(jogo)
        print(f"\n'{jogo.titulo}' adicionado ao backlog!")

    def mostrar_backlog(self):
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
        if self.backlog.is_empty():
            print("\nBacklog vazio! Adicione jogos primeiro.")
            return

        jogo = self.backlog.dequeue()
        print(f"\nJogando: {jogo.titulo} | {jogo.console}")

        try:
            tempo = float(input("  Quantas horas voce jogou? "))
        except:
            tempo = 1.0

        self.registrar_sessao(jogo, tempo)

    def salvar_backlog(self):
        try:
            with open('backlog.txt', 'w', encoding='utf-8') as f:
                for jogo in self.backlog.mostrar():
                    f.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")
            print("\nBacklog salvo em 'backlog.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar o backlog: {e}")

    def carregar_backlog(self):
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

    def registrar_sessao(self, jogo, tempo):
        sessao = SessaoJogo(jogo, tempo)
        self.historico.append(sessao)

        if jogo.id in self.tempos_por_jogo:
            self.tempos_por_jogo[jogo.id] += tempo
        else:
            self.tempos_por_jogo[jogo.id] = tempo

        self.recentes.push(jogo)

        print(f"\n  Sessao registrada!")
        print(f"  Status: {sessao.status}")
        print(f"  Tempo total em '{jogo.titulo}': {self.tempos_por_jogo[jogo.id]:.1f}h")

    def mostrar_historico(self):
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
        try:
            with open('historico_jogo.txt', 'w', encoding='utf-8') as f:
                for sessao in self.historico:
                    tempo_total = self.tempos_por_jogo.get(sessao.jogo.id, sessao.tempo_jogado)
                    f.write(f"{sessao.jogo.titulo};{sessao.tempo_jogado};"
                            f"{tempo_total};{sessao.status}\n")
            print("\nHistorico salvo em 'historico_jogo.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar o historico: {e}")

    def carregar_historico(self):
        if not os.path.exists('historico_jogo.txt'):
            return

        try:
            with open('historico_jogo.txt', 'r', encoding='utf-8') as f:
                linhas = f.readlines()

            jogos_por_titulo = {}
            for jogo in self.catalogo:
                jogos_por_titulo[jogo.titulo] = jogo

            carregados = 0
            for linha in linhas:
                linha = linha.strip()
                if linha == '':
                    continue
                partes = linha.split(';')
                if len(partes) >= 3:
                    try:
                        titulo = partes[0]
                        tempo_sessao = float(partes[1])
                        tempo_total = float(partes[2])
                        status = partes[3] if len(partes) >= 4 else 'Iniciado'

                        if titulo in jogos_por_titulo:
                            jogo = jogos_por_titulo[titulo]
                            sessao = SessaoJogo(jogo, tempo_sessao)
                            sessao.status = status

                            self.historico.append(sessao)
                            self.tempos_por_jogo[jogo.id] = tempo_total
                            carregados += 1
                    except:
                        continue

            if carregados > 0:
                print(f"Historico carregado: {carregados} sessao(oes).")

        except Exception as e:
            print(f"[ERRO] Nao foi possivel carregar o historico: {e}")

    def mostrar_recentes(self):
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
        jogo = self.recentes.topo()
        if jogo is None:
            print("\nNenhum jogo recente para retomar.")
            return

        print(f"\nRetomando: {jogo.titulo} | {jogo.console}")
        try:
            tempo = float(input("  Quantas horas voce jogou agora? "))
        except:
            tempo = 1.0

        self.registrar_sessao(jogo, tempo)

    def salvar_recentes(self):
        try:
            with open('recentes.txt', 'w', encoding='utf-8') as f:
                lista_interna = self.recentes._pilha
                for jogo in lista_interna:
                    f.write(f"{jogo.id};{jogo.titulo};{jogo.console}\n")
            print("\nRecentes salvos em 'recentes.txt'!")
        except Exception as e:
            print(f"[ERRO] Nao foi possivel salvar os recentes: {e}")

    def carregar_recentes(self):
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

    def recomendar_jogos(self):
        if len(self.historico) == 0:
            print("\nJogue alguns jogos primeiro para receber recomendacoes!")
            return

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

        genero_fav = ''
        maior = 0
        for g, qtd in contagem_genero.items():
            if qtd > maior:
                maior = qtd
                genero_fav = g

        console_fav = ''
        maior = 0
        for c, qtd in contagem_console.items():
            if qtd > maior:
                maior = qtd
                console_fav = c

        ids_jogados = {}
        for sessao in self.historico:
            ids_jogados[sessao.jogo.id] = True

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

        for jogo in self.catalogo:
            if jogo.id in ids_jogados:
                continue
            if jogo.id in ids_backlog:
                continue
            if (jogo.genero == genero_fav and
                    jogo.console == console_fav and
                    jogo.critic_score >= 8):
                recomendados.append(jogo)

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

        if len(recomendados) == 0:
            print("\n  Nenhuma recomendacao encontrada com esses criterios.")
        else:
            print(f"\n  {len(recomendados[:10])} jogo(s) recomendado(s):\n")
            for i, jogo in enumerate(recomendados[:10]):
                print(f"  {i+1}. [{jogo.id}] {jogo.titulo}")
                print(f"      Console: {jogo.console} | Genero: {jogo.genero}")
                print(f"      Nota: {jogo.critic_score} | Vendas: {jogo.total_sales}M")
                print()

    def gerar_ranking_pessoal(self):
        if len(self.historico) == 0:
            print("\nNenhum jogo jogado ainda.")
            return

        print(f"\n{'='*60}")
        print(f"  RANKING PESSOAL")
        print(f"{'='*60}")

        lista_tempo = []
        for id_jogo, tempo in self.tempos_por_jogo.items():
            if id_jogo in self.jogos_por_id:
                lista_tempo.append((self.jogos_por_id[id_jogo], tempo))

        n = len(lista_tempo)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_tempo[j][1] < lista_tempo[j+1][1]:
                    lista_tempo[j], lista_tempo[j+1] = lista_tempo[j+1], lista_tempo[j]

        print("\n  Jogos mais jogados:")
        for i, (jogo, tempo) in enumerate(lista_tempo[:5]):
            print(f"  {i+1}. {jogo.titulo} - {tempo:.1f}h")

        contagem_genero = {}
        for sessao in self.historico:
            g = sessao.jogo.genero
            if g in contagem_genero:
                contagem_genero[g] += sessao.tempo_jogado
            else:
                contagem_genero[g] = sessao.tempo_jogado

        lista_genero = []
        for g, t in contagem_genero.items():
            lista_genero.append((g, t))

        n = len(lista_genero)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_genero[j][1] < lista_genero[j+1][1]:
                    lista_genero[j], lista_genero[j+1] = lista_genero[j+1], lista_genero[j]

        print("\n  Generos mais jogados:")
        for i, (g, t) in enumerate(lista_genero[:5]):
            print(f"  {i+1}. {g} - {t:.1f}h")

        contagem_console = {}
        for sessao in self.historico:
            c = sessao.jogo.console
            if c in contagem_console:
                contagem_console[c] += sessao.tempo_jogado
            else:
                contagem_console[c] = sessao.tempo_jogado

        lista_console = []
        for c, t in contagem_console.items():
            lista_console.append((c, t))

        n = len(lista_console)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_console[j][1] < lista_console[j+1][1]:
                    lista_console[j], lista_console[j+1] = lista_console[j+1], lista_console[j]

        print("\n  Consoles mais jogados:")
        for i, (c, t) in enumerate(lista_console[:5]):
            print(f"  {i+1}. {c} - {t:.1f}h")

        ids_vistos = {}
        lista_notas = []
        for sessao in self.historico:
            if sessao.jogo.id not in ids_vistos:
                ids_vistos[sessao.jogo.id] = True
                lista_notas.append(sessao.jogo)

        n = len(lista_notas)
        for i in range(n):
            for j in range(0, n - i - 1):
                if lista_notas[j].critic_score < lista_notas[j+1].critic_score:
                    lista_notas[j], lista_notas[j+1] = lista_notas[j+1], lista_notas[j]

        print("\n  Melhores notas (jogos que voce jogou):")
        for i, jogo in enumerate(lista_notas[:5]):
            print(f"  {i+1}. {jogo.titulo} - Nota: {jogo.critic_score}")

        print(f"\n{'='*60}")

    def exibir_dashboard(self):
        total_sessoes = len(self.historico)

        tempo_total = 0.0
        for sessao in self.historico:
            tempo_total += sessao.tempo_jogado

        media_horas = 0.0
        if total_sessoes > 0:
            media_horas = tempo_total / total_sessoes

        jogo_mais_jogado = None
        maior_tempo = 0
        for id_jogo, tempo in self.tempos_por_jogo.items():
            if tempo > maior_tempo:
                maior_tempo = tempo
                if id_jogo in self.jogos_por_id:
                    jogo_mais_jogado = self.jogos_por_id[id_jogo]

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

        genero_fav = '-'
        maior = 0
        for g, q in contagem_g.items():
            if q > maior:
                maior = q
                genero_fav = g

        console_fav = '-'
        maior = 0
        for c, q in contagem_c.items():
            if q > maior:
                maior = q
                console_fav = c

        nota_media = 0.0
        if qtd_notas > 0:
            nota_media = soma_notas / qtd_notas

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

        ids_jog_dash = {}
        for sessao in self.historico:
            ids_jog_dash[sessao.jogo.id] = True
        recomendacoes_disp = 0
        for jogo in self.catalogo:
            if jogo.id not in ids_jog_dash and jogo.critic_score >= 8:
                recomendacoes_disp += 1

        print(f'\n{"="*60}')
        print(f'  DASHBOARD - STEAMPY')
        print(f'{"="*60}')
        print(f'  Total de jogos no catalogo   : {len(self.catalogo)}')
        print(f'  Total de jogos no backlog    : {self.backlog.tamanho()}')
        print(f'  Total de jogos recentes      : {self.recentes.tamanho()}')
        print(f'  Total de sessoes jogadas     : {total_sessoes}')
        print(f'  Tempo total jogado           : {tempo_total:.1f}h')
        print(f'  Media de horas por sessao    : {media_horas:.1f}h')
        print(f'{"="*60}')
        print(f'  Jogo mais jogado             : {jogo_mais_jogado.titulo if jogo_mais_jogado else "-"} ({maior_tempo:.1f}h)')
        print(f'  Genero favorito              : {genero_fav}')
        print(f'  Console favorito             : {console_fav}')
        print(f'  Nota media dos jogados       : {nota_media:.1f}')
        print(f'{"="*60}')
        print(f'  Sessoes Iniciado             : {iniciados}')
        print(f'  Sessoes Em andamento         : {em_andamento}')
        print(f'  Sessoes Concluido            : {concluidos}')
        print(f'{"="*60}')
        print(f'  Recomendacoes disponiveis    : {recomendacoes_disp}')
        print(f'  Jogo mais popular jogado     : {jogo_popular.titulo if jogo_popular else "-"} ({maior_venda:.2f}M vendas)')
        print(f'  Jogo melhor nota jogado      : {jogo_melhor_nota.titulo if jogo_melhor_nota else "-"} (nota {melhor_nota:.1f})')
        print(f'{"="*60}')

    def salvar_tudo(self):
        self.salvar_backlog()
        self.salvar_historico()
        self.salvar_recentes()
        print('\nTodos os dados foram salvos!')