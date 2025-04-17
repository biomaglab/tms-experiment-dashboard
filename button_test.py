from nicegui import ui
from nicegui.elements.label import Label

labels: dict[str, Label] = {}

textos = ['Texto A', 'Texto B', 'Texto C']

for texto in textos:
    label = ui.label(texto)
    label.style('padding: 16px; background-color: grey; color: white;')
    labels[texto] = label

def mudar_cor(texto_alvo: str, nova_cor: str):
    print(f'Trocando cor de "{texto_alvo}" para "{nova_cor}"')
    
    cores = {
        'green': '#4CAF50',
        'red': '#F44336',
        'blue': '#2196F3',
        'grey': '#9E9E9E',
    }

    if texto_alvo in labels:
        cor = cores.get(nova_cor, '#9E9E9E')  # cor padrão se não for válida
        label: Label = labels[texto_alvo]
        label.style(f'padding: 16px; background-color: {cor}; color: white;')
        label.update()

ui.button('Texto A → verde', on_click=lambda: mudar_cor('Texto A', 'green'))
ui.button('Texto B → vermelho', on_click=lambda: mudar_cor('Texto B', 'red'))
ui.button('Texto C → azul', on_click=lambda: mudar_cor('Texto C', 'blue'))

print(labels)
ui.run(port=8081)