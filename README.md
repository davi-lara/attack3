# Attack 3 Joystick Mapper

Este projeto transforma um joystick do tipo Logitech Attack 3 em entradas de teclado para uso em jogos ou aplicações que exigem controle por teclado. O script lê os eixos analógicos e os botões do controle e os converte em pressionamentos de teclas, permitindo que o joystick funcione como um periférico de teclado virtual.

## O que o projeto faz

- Mapeia os eixos analógicos do joystick para setas direcionais
- Permite personalizar cada botão do controle para uma tecla do teclado
- Ajusta a sensibilidade do eixo analógico automaticamente
- Mantém o funcionamento em tempo real com atualização constante

## Requisitos

- Python 3.9+
- Pygame
- pynput
- Um joystick compatível com SDL/Pygame, como o Logitech Attack 3

## Instalação

1. Clone este repositório:

```bash
git clone <url-do-repositorio>
cd attack3
```

2. Crie um ambiente virtual (opcional, mas recomendado):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências:

```bash
pip install pygame pynput
```

## Como executar

Conecte o joystick e rode:

```bash
python attack3.py
```

O programa verifica se há algum joystick disponível e inicia o mapeamento automático. Para encerrar, pressione `Ctrl + C` no terminal.

## Mapeamento padrão

O script já vem com um exemplo de mapeamento para botões e eixos:

- Eixo X: setas esquerda/direita
- Eixo Y: setas cima/baixo
- Botão 0: `Space`
- Botão 1: `Enter`
- Botão 2: `a`
- Botão 3: `b`
- Botão 4: `c`

Esses valores podem ser alterados no dicionário `MAPEAMENTO_BOTOES` dentro do arquivo `attack3.py`.

## Configuração personalizada

Abra o arquivo `attack3.py` e edite o dicionário `MAPEAMENTO_BOTOES`:

```python
MAPEAMENTO_BOTOES = {
    0: Key.space,
    1: Key.enter,
    2: "a",
    3: "b",
    4: "c",
}
```

Você pode trocar as teclas por qualquer valor suportado pelo `pynput`, como:

- `Key.space`
- `Key.enter`
- `Key.left`, `Key.right`, `Key.up`, `Key.down`
- Strings como `"w"`, `"a"`, `"s"`, `"d"`
- Caracteres individuais como `"x"`, `"y"`, `"z"`

## Ajuste de sensibilidade

A sensibilidade analógica pode ser ajustada no código com os parâmetros de eixo e zona morta:

```python
ZONA_MORTA = 0.3
```

Esse valor define o limiar mínimo para que o joystick passe a enviar movimento de teclado. Quanto menor o valor, mais sensível o controle fica.

## Observações

- O script usa `pygame` para detectar o joystick e `pynput` para simular teclas.
- O programa libera as teclas ao encerrar, para evitar travamentos no teclado virtual.
- Em alguns casos, pode ser necessário ajustar o identificador do joystick ou o mapeamento conforme o modelo e o sistema operacional.

## Licença

Este projeto é um utilitário pessoal/experimental e pode ser adaptado conforme a necessidade do usuário.

## Dica de uso

Este tipo de script é especialmente útil para:

- jogos antigos que dependem de teclado
- emuladores
- automações de teclado
- setups de acessibilidade

Se o controle tiver botões extras, basta adicionar novos índices no dicionário `MAPEAMENTO_BOTOES`.
