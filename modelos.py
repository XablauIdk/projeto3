# ============================================================
# modelos.py - Classes de dados do sistema SteamPy
# ============================================================
# Define as estruturas de dados principais:
# - Jogo: representa cada jogo do catalogo
# - SessaoJogo: representa cada sessao/tempo jogado em um jogo

from datetime import date


# -------- CLASSE JOGO --------
class Jogo:
    # Representa um jogo individual do catalogo
    # Armazena todas as informacoes do jogo do dataset

    def __init__(self, id, titulo, console, genero, publisher, developer,
                 critic_score, total_sales, na_sales, jp_sales,
                 pal_sales, other_sales, release_date):
        # Inicializa um objeto Jogo com todos seus atributos
        # Parametros vem do arquivo dataset.csv

        self.id = id  # ID unico do jogo
        self.titulo = titulo  # Nome do jogo
        self.console = console  # Plataforma (PS3, Xbox, PC, etc)
        self.genero = genero  # Tipo de jogo (Acao, RPG, etc)
        self.publisher = publisher  # Empresa que publicou
        self.developer = developer  # Empresa que desenvolveu
        self.critic_score = critic_score    # Nota de critica (0-100)
        self.total_sales = total_sales      # Vendas totais em milhoes
        self.na_sales = na_sales  # Vendas America do Norte
        self.jp_sales = jp_sales  # Vendas Japao
        self.pal_sales = pal_sales  # Vendas Europa/PAL
        self.other_sales = other_sales  # Outras vendas
        self.release_date = release_date  # Data de lancamento

    def __str__(self):
        # Retorna uma representacao formatada do jogo em texto
        # Usada para exibir o jogo na tela
        return (f"[{self.id}] {self.titulo} | {self.console} | "
                f"{self.genero} | Nota: {self.critic_score} | "
                f"Vendas: {self.total_sales}M | {self.release_date}")


# -------- CLASSE SESSAO DE JOGO --------
class SessaoJogo:
    # Representa uma unica sessao de jogo (tempo que o usuario jogou)
    # Cada vez que usuario joga, cria-se uma nova SessaoJogo

    def __init__(self, jogo, tempo_jogado):
        # Inicializa uma sessao de jogo
        # Parametros:
        #   jogo: objeto Jogo que foi jogado
        #   tempo_jogado: horas jogadas nessa sessao (float)

        self.jogo = jogo  # Referencia ao objeto Jogo
        self.tempo_jogado = tempo_jogado        # horas (float) desta sessao
        self.data_sessao = str(date.today())  # Data de hoje da sessao
        self.percentual_simulado = min(100, int(tempo_jogado * 5))  # Percentual simulado
        self.status = self._calcular_status()  # Status calculado baseado no tempo

    def _calcular_status(self):
        # Calcula o status do jogo baseado no tempo total jogado
        # Status determina o progresso no jogo:
        #   - Iniciado: menos de 2 horas
        #   - Em andamento: 2 a 10 horas
        #   - Muito jogado: 10 a 20 horas
        #   - Concluido simbolicamente: acima de 20 horas

        if self.tempo_jogado < 2:
            return "Iniciado"  # Usuario mal comecou
        elif self.tempo_jogado <= 10:
            return "Em andamento"  # Usuario esta jogando
        elif self.tempo_jogado <= 20:
            return "Muito jogado"  # Usuario jogou bastante
        else:
            return "Concluido simbolicamente"  # Usuario praticamente terminou

    def __str__(self):
        # Retorna uma representacao formatada da sessao em texto
        # Usada para exibir no historico
        return (f"{self.jogo.titulo} | {self.tempo_jogado}h | "
                f"{self.data_sessao} | Status: {self.status}")
