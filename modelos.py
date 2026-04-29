from datetime import date


class Jogo:

    def __init__(self, id, titulo, console, genero, publisher, developer,
                 critic_score, total_sales, na_sales, jp_sales,
                 pal_sales, other_sales, release_date):
        self.id = id
        self.titulo = titulo
        self.console = console
        self.genero = genero
        self.publisher = publisher
        self.developer = developer
        self.critic_score = critic_score
        self.total_sales = total_sales
        self.na_sales = na_sales
        self.jp_sales = jp_sales
        self.pal_sales = pal_sales
        self.other_sales = other_sales
        self.release_date = release_date

    def __str__(self):
        return (f"[{self.id}] {self.titulo} | {self.console} | "
                f"{self.genero} | Nota: {self.critic_score} | "
                f"Vendas: {self.total_sales}M | {self.release_date}")


class SessaoJogo:

    def __init__(self, jogo, tempo_jogado):
        self.jogo = jogo
        self.tempo_jogado = tempo_jogado
        self.data_sessao = str(date.today())
        self.percentual_simulado = min(100, int(tempo_jogado * 5))
        self.status = self._calcular_status()

    def _calcular_status(self):
        if self.tempo_jogado < 2:
            return "Iniciado"
        elif self.tempo_jogado <= 10:
            return "Em andamento"
        elif self.tempo_jogado <= 20:
            return "Muito jogado"
        else:
            return "Concluido simbolicamente"

    def __str__(self):
        return (f"{self.jogo.titulo} | {self.tempo_jogado}h | "
                f"{self.data_sessao} | Status: {self.status}")