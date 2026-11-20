from pathlib import Path

from assistente import Assistente
from base_conhecimento import BaseConhecimento


def main():
    pasta = Path(__file__).resolve().parent / 'data'
    base = BaseConhecimento(pasta / 'base_conhecimento.json')
    base.carregar()
    assistente = Assistente('Citizen Assist AI - Mobilidade', base, pasta)
    assistente.menu()


if __name__ == '__main__':
    main()
