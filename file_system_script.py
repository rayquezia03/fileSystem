from rich.console import Console
from rich.table import Table
import array

console = Console()

# Classe que representa um bloco (com dados e ponteiro)
class Bloco:
    def __init__(self, dado=None, proximo=None):
        self.dado = dado
        self.proximo = proximo

# Classe que representa o registro de um arquivo
class RegistroArquivo:
    def __init__(self, nome, tamanho, inicio):
        self.nome = nome
        self.tamanho = tamanho
        self.inicio = inicio

# Classe para simular a memória do disco
class MemoriaDisco:
    def __init__(self, capacidade):
        self.capacidade = capacidade // 32
        self.blocos = [Bloco() for _ in range(self.capacidade)]
        self.memoria_livre = 0
        self.lista_bloco_livre = None

        # Inicializando a lista de blocos livres (encadeando os blocos)
        for i in range(self.capacidade - 1):
            self.blocos[i].proximo = i + 1  # O próximo bloco do índice 'i' é 'i+1'
        self.blocos[self.capacidade - 1].proximo = None  # O último bloco aponta para None
        self.lista_bloco_livre = 0  # O primeiro bloco livre é o índice 0

    def alocar(self):
        # Alocar um bloco (se houver espaço livre)
        if self.lista_bloco_livre is None:  # Não há mais blocos livres
            return None
        primeiro_livre = self.lista_bloco_livre
        self.lista_bloco_livre = self.blocos[primeiro_livre].proximo  # Atualiza o ponteiro para o próximo bloco livre
        return primeiro_livre

    def desalocar(self, indice):
        # Desalocar um bloco, tornando-o livre novamente
        self.blocos[indice].proximo = self.lista_bloco_livre
        self.lista_bloco_livre = indice  # Atualiza o ponteiro para o próximo bloco livre

    def exibir_setores(self):
        tabela = Table(title="Situação Atual do Disco")
        tabela.add_column("Bloco", justify="center", style="cyan")
        tabela.add_column("Dado", justify="center", style="green")
        tabela.add_column("Próximo", justify="center", style="magenta")

        for i in range(self.capacidade):
            dado = self.blocos[i].dado if self.blocos[i].dado is not None else "-"
            proximo = str(self.blocos[i].proximo) if self.blocos[i].proximo is not None else "-"
            tabela.add_row(str(i), dado, proximo)

        console.print(tabela)

    def exibir_blocos_livres(self):
        indices_livres = []
        bloco_atual = self.lista_bloco_livre
        while bloco_atual is not None:
            indices_livres.append(str(bloco_atual))
            bloco_atual = self.blocos[bloco_atual].proximo
        console.print(f"[bold yellow]Índices de Blocos Livres:[/bold yellow] {' -> '.join(indices_livres)}")

    def exibir_bits(self):
        bits_str = ' '.join(map(str, self.blocos))
        console.print(f"[bold yellow]Mapa de Bits:[/bold yellow] {bits_str}")

# Classe principal que simula o sistema de arquivos
class SistemaDeArquivos:
    def __init__(self, tamanho_total):
        self.disco = MemoriaDisco(tamanho_total)
        self.arquivos = []

    def criar(self, nome, dados):
        # Verifica se o nome é válido (máximo 4 caracteres)
        if len(nome) > 4:
            console.print(f"[red]Nome do arquivo '{nome}' excede o limite de 4 caracteres![/red]")
            return

        # Verifica se o arquivo já existe
        if any(a.nome == nome for a in self.arquivos):
            console.print(f"[red]O arquivo '{nome}' já existe![/red]")
            return

        espaco_disponivel = self.disco.capacidade - sum(1 for b in self.disco.blocos if b.dado != None)
        if espaco_disponivel < len(dados):
            console.print("[bold red]Espaço insuficiente no disco![/bold red]")
            return

        inicio = self.disco.alocar()
        if inicio is None:
            console.print("[bold red]Não foi possível alocar espaço![/bold red]")
            return

        atual = inicio
        for i, caractere in enumerate(dados):
            proximo = self.disco.alocar() if i < len(dados) - 1 else None
            self.disco.blocos[atual] = Bloco(caractere, proximo)
            atual = proximo

        novo_arquivo = RegistroArquivo(nome, len(dados), inicio)
        self.arquivos.append(novo_arquivo)
        console.print(f"[green]Arquivo '{nome}' criado com sucesso![/green]")

    def ler(self, nome):
        arq = next((a for a in self.arquivos if a.nome == nome), None)
        if arq is None:
            console.print(f"[red]Arquivo '{nome}' não encontrado.[/red]")
            return

        endereco = arq.inicio
        conteudo = ""
        while endereco is not None:
            no = self.disco.blocos[endereco]
            conteudo += no.dado
            endereco = no.proximo

        console.print(f"[bold blue]Conteúdo de '{nome}':[/bold blue] {conteudo}")

    def excluir(self, nome):
        arq = next((a for a in self.arquivos if a.nome == nome), None)
        if arq is None:
            console.print(f"[red]Arquivo '{nome}' não encontrado.[/red]")
            return

        blocos_a_excluir = []
        endereco = arq.inicio
        while endereco is not None:
            blocos_a_excluir.append(endereco)
            endereco = self.disco.blocos[endereco].proximo

        for bloco_idx in reversed(blocos_a_excluir):
            self.disco.blocos[bloco_idx] = Bloco()
            self.disco.desalocar(bloco_idx)

        self.arquivos.remove(arq)
        console.print(f"[bold cyan]Arquivo '{nome}' excluído com sucesso![/bold cyan]")

    def listar(self):
        tabela = Table(title="Tabela de Arquivos", show_lines=True)
        tabela.add_column("Nome", justify="center", style="cyan")
        tabela.add_column("Tamanho", justify="center", style="green")
        tabela.add_column("Início", justify="center", style="magenta")

        for a in self.arquivos:
            tabela.add_row(a.nome, str(a.tamanho), str(a.inicio))
        console.print(tabela)

'''
sistema = SistemaDeArquivos(1024)
sistema.criar("arq1", "PERNAMBUCO")
sistema.criar("arq2", "são paulo")
sistema.criar("arq3", "ALAGOAS")
sistema.criar("arq4", "SANTA CATARINA")
# sistema.listar()
# sistema.disco.exibir_bits()
sistema.disco.exibir_setores()
sistema.excluir("arq2")
# sistema.listar()
sistema.disco.exibir_setores()
sistema.criar("arq5", "SANTA CATARINA")
sistema.disco.exibir_setores()
'''