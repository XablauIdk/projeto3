from steampy import SteamPy
from menu import menu


sistema = SteamPy()
sistema.carregar_jogos('dataset.csv')
sistema.carregar_backlog()
sistema.carregar_historico()
sistema.carregar_recentes()
menu(sistema)