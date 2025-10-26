# Simulação de Gerenciamento de Arquivos com Lista Encadeada

**Equipe:** Rayane Quézia, Thallys Asafe e Thalia

**Disciplina:** Sistemas Operacionais

**Professor:** Tércio de Morais

**Repositório:** [https://github.com/rayquezia03/fileManagement-SO](https://github.com/rayquezia03/fileManagement-SO)

---

## Descrição

Este projeto é uma simulação de um sistema de arquivos simples, implementado em Python para a disciplina de Sistemas Operacionais. O objetivo é demonstrar o gerenciamento de espaço em disco usando alocação por lista encadeada.

O sistema permite a criação, leitura e exclusão de "arquivos" (representados por strings/palavras), gerenciando o espaço livre em um disco simulado. A principal característica é a capacidade de alocar arquivos mesmo que não haja espaço contíguo suficiente, utilizando "buracos" deixados por arquivos excluídos.

---

## Conceitos de Implementação

Dividimos o projeto em quatro arquivos principais:

* **`Disco Simulado`**
  O disco é simulado usando um array Python (import array), conforme a restrição do projeto.

O disco tem um tamanho total de 1024 bits, organizado em 32 blocos de 32 bits cada.

* **`Estrutura do Bloco`**
Cada bloco de 32 bits é dividido em duas partes:

16 bits para Dados: Armazena um único caractere (char) do arquivo.

16 bits para Ponteiro: Armazena o índice (short int) do próximo bloco que compõe o arquivo. O último bloco de um arquivo possui um ponteiro nulo.

* **`Tabela de Diretório`**
  Uma tabela de diretório simples armazena o nome de cada arquivo (com no máximo 4 caracteres) e o índice do bloco onde o arquivo se inicia.

* **`Gerenciamento de Espaço Livre`**
O espaço livre é gerenciado como uma lista encadeada de blocos livres.

Uma variável short int aponta para a primeira posição livre no array.

Outra variável short int armazena o tamanho total de blocos livres.

Quando um arquivo é criado, o sistema verifica se o tamanho total livre é suficiente. Se for, ele aloca os blocos necessários da lista livre. Se for insuficiente, uma mensagem de "memória insuficiente" é exibida

---

## Funcionalidades

O sistema implementa as três operações básicas de gerenciamento de arquivos:

Criação (create_file): Recebe um nome e um conteúdo (palavra). Verifica se há espaço livre total. Se houver, aloca os blocos (um para cada caractere) da lista livre e os encadeia.

Leitura (read_file): Recebe um nome de arquivo. Navega pela lista encadeada de blocos a partir do índice inicial (armazenado no diretório) e imprime o conteúdo (palavra) na tela.

Exclusão (delete_file): Recebe um nome de arquivo. Remove a entrada do diretório e retorna todos os blocos do arquivo para o início da lista de espaço livre.

O projeto também inclui funções auxiliares para demonstrar o funcionamento:

Imprimir o estado atual do disco (dados e ponteiros de cada bloco).

Imprimir a tabela de diretório.

Imprimir os índices dos blocos vazios (a lista livre).