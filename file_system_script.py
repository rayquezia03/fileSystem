from rich.console import Console
from rich.table import Table
import array

console = Console()

# Classe que representa o registro de um arquivo na tabela de diretório
class RegistroArquivo:
    def __init__(self, nome, tamanho, inicio):
        self.nome = nome      # Nome do arquivo (máximo 4 caracteres)
        self.tamanho = tamanho  # Tamanho do arquivo em blocos
        self.inicio = inicio    # Endereço do primeiro bloco do arquivo no disco

# Classe para simular a memória do disco
class MemoriaDisco:
    def __init__(self, capacidade_bits):
        self.capacidade = 1024 // 32  # 1024 bits / 32 bits/bloco = 32 blocos
        
        # Simulação da memória com o módulo 'array'
        # 'u' para caracteres unicode (16 bits) e 'h' para short int (16 bits)
        self.dados = array.array('u', ['\0'] * self.capacidade)
        self.ponteiros = array.array('h', [0] * self.capacidade)
        
        # Variável para guardar o tamanho total da memória livre
        self.memoria_livre_tamanho = self.capacidade
        # Ponteiro para a primeira posição livre
        self.lista_bloco_livre = 0

        # Inicializando a lista encadeada de blocos livres
        for i in range(self.capacidade - 1):
            self.ponteiros[i] = i + 1
        self.ponteiros[self.capacidade - 1] = -1  # -1 representa o ponteiro nulo

    def alocar(self):
        # Aloca um bloco se houver espaço livre
        if self.lista_bloco_livre == -1:
            return None
        
        primeiro_livre = self.lista_bloco_livre
        self.lista_bloco_livre = self.ponteiros[primeiro_livre]
        self.memoria_livre_tamanho -= 1
        return primeiro_livre

    def desalocar(self, indice):
        # Desaloca um bloco, tornando-o livre novamente
        self.ponteiros[indice] = self.lista_bloco_livre
        self.lista_bloco_livre = indice
        self.dados[indice] = '\0' # Limpa o dado do bloco
        self.memoria_livre_tamanho += 1

    def exibir_setores(self):
        tabela = Table(title="Situação Atual do Disco")
        tabela.add_column("Bloco", justify="center", style="cyan")
        tabela.add_column("Dado", justify="center", style="green")
        tabela.add_column("Próximo", justify="center", style="magenta")

        for i in range(self.capacidade):
            dado = self.dados[i] if self.dados[i] != '\0' else "-"
            proximo = str(self.ponteiros[i]) if self.ponteiros[i] != -1 else "-"
            tabela.add_row(str(i), dado, proximo)
        console.print(tabela)

    def exibir_blocos_livres(self):
        indices_livres = []
        bloco_atual = self.lista_bloco_livre
        while bloco_atual != -1:
            indices_livres.append(str(bloco_atual))
            bloco_atual = self.ponteiros[bloco_atual]
        console.print(f"[bold yellow]Índices de Blocos Livres:[/bold yellow] {' -> '.join(indices_livres)}")

# Classe principal que simula o sistema de arquivos
class SistemaDeArquivos:
    def __init__(self, tamanho_total):
        self.disco = MemoriaDisco(tamanho_total)
        self.arquivos = []  # Simula a tabela de diretório

    def criar(self, nome, dados):
        # Valida o nome do arquivo (máximo 4 caracteres)
        if len(nome) > 4:
            console.print(f"[red]Nome do arquivo '{nome}' excede o limite de 4 caracteres![/red]")
            return
        if any(a.nome == nome for a in self.arquivos):
            console.print(f"[red]O arquivo '{nome}' já existe![/red]")
            return

        # Verifica se o espaço livre total é suficiente
        if self.disco.memoria_livre_tamanho < len(dados):
            console.print(f"[bold red]Memória insuficiente para criar o arquivo '{nome}'![/bold red]")
            return

        inicio = self.disco.alocar()
        if inicio is None:
            console.print("[bold red]Não foi possível alocar espaço![/bold red]")
            return

        atual = inicio
        for i, caractere in enumerate(dados):
            self.disco.dados[atual] = caractere # Armazena um caractere por bloco
            if i < len(dados) - 1:
                proximo = self.disco.alocar()
                self.disco.ponteiros[atual] = proximo
                atual = proximo
            else:
                self.disco.ponteiros[atual] = -1 # Último bloco aponta para nulo

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
        while endereco != -1:
            conteudo += self.disco.dados[endereco]
            endereco = self.disco.ponteiros[endereco]
        console.print(f"[bold blue]Conteúdo de '{nome}':[/bold blue] {conteudo}")

    def excluir(self, nome):
        arq = next((a for a in self.arquivos if a.nome == nome), None)
        if arq is None:
            console.print(f"[red]Arquivo '{nome}' não encontrado.[/red]")
            return

        blocos_a_excluir = []
        endereco = arq.inicio
        while endereco != -1:
            blocos_a_excluir.append(endereco)
            endereco = self.disco.ponteiros[endereco]

        for bloco_idx in reversed(blocos_a_excluir):
            self.disco.desalocar(bloco_idx)

        self.arquivos.remove(arq)
        console.print(f"[bold cyan]Arquivo '{nome}' excluído com sucesso![/bold cyan]")

    def listar(self):
        tabela = Table(title="Tabela de Diretório", show_lines=True)
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