from file_system_script import SistemaDeArquivos
from rich.console import Console
from time import sleep

console = Console()

def menu_principal():

    console.print("="*5 + ' [bold magenta]SISTEMA DE ARQUIVOS[/bold magenta] ' + "="*5)
    print()

    sleep(1)

    console.print('[bold cyan]Bem-vindo ao Sistema de Arquivos![/bold cyan]')
    sleep(1)

    print()

    memoria_disponivel = 1024
    console.print(f'[bold green]Sistema inicializado com {memoria_disponivel} bits de memória.[/bold green]')
    print()

    sistema = SistemaDeArquivos(memoria_disponivel)

    while True:
        sleep(2)
        console.print("="*5 + " [bold cyan]Menu Principal[/bold cyan] " + "="*5)
        console.print('[bold blue]Escolha uma das opções abaixo:[/bold blue]')
        print("1. Criar Novo Arquivo")
        print("2. Visualizar Arquivo")
        print("3. Excluir Arquivo")
        print("4. Exibir Estado do Disco")
        print("5. Exibir Blocos Livres")
        print("6. Exibir Tabela de Arquivos")
        print("7. Sair do Sistema")
        
        opcao_escolhida = int(input("Digite a opção desejada: "))

        if opcao_escolhida == 1:
            nome_arquivo = input('Informe o nome do arquivo a ser criado: ')
            conteudo_arquivo = input('Digite o conteúdo do arquivo: ')
            sistema.criar(nome_arquivo, conteudo_arquivo)

        elif opcao_escolhida == 2:
            nome_arquivo = input("Digite o nome do arquivo que deseja ler: ")
            sistema.ler(nome_arquivo)
        
        elif opcao_escolhida == 3:
            nome_arquivo = input("Informe o nome do arquivo a ser removido: ")
            sistema.excluir(nome_arquivo)
        
        elif opcao_escolhida == 4:
            sistema.disco.exibir_setores()
        
        elif opcao_escolhida == 5:
            sistema.disco.exibir_blocos_livres()
        
        elif opcao_escolhida == 6:
            sistema.listar()
        
        elif opcao_escolhida == 7:
            console.print("[bold]Fechando o programa...[/bold]")
            sleep(1)
            break
        
        else:
            console.print("[bold red]Opção inválida, tente novamente.[/bold red]")

menu_principal()
