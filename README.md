# Biomag TMS Experiment Dashboard v0.2.0

<img src="https://raw.githubusercontent.com/biomaglab/tms-experiment-dashboard/master/static/biomag_logo.jpg" alt="Logo Biomag">

> Interface gráfica web moderna para visualização e controle de eventos durante experimentos de TMS acoplados a EMG usando o InVesalius.

## ✨ Novidades v0.2.0

- 🎨 **Arquitetura Dual Framework**: Suporte para NiceGUI e Streamlit
- 🔧 **Estrutura Modular**: Código organizado e reutilizável  
- 🚀 **Auto-detecção**: Detecta automaticamente o framework instalado
- 📦 **Instalação Flexível**: Use `uv` com extras opcionais

## 💻 Pré-requisitos

- Python 3.11+
- `uv` (gerenciador de pacotes) - [Instalação](https://github.com/astral-sh/uv)
- Git

## 🚀 Instalação Rápida

```bash
# Clone o repositório
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
cd tms-experiment-dashboard

# Instale com NiceGUI (recomendado)
uv sync --extra nicegui

# OU instale com Streamlit
uv sync --extra streamlit

# OU install ambos
uv sync --extra all
```

## ☕ Como Usar

### 1. Inicie o servidor de relay

```bash
uv run python scripts/relay_server.py 127.0.0.1 5000
```

### 2. (Opcional) Inicie o InVesalius

```bash
python /caminho/para/invesalius3/app.py --remote-host http://localhost:5000
```

### 3. Inicie o Dashboard

```bash
# Auto-detecção (NiceGUI ou Streamlit)
uv run python main.py
```

**Acesso:**
- NiceGUI: http://localhost:8084
- Streamlit: Abre automaticamente no navegador

## 📁 Estrutura do Projeto

```
tms-experiment-dashboard/
├── src/tms_dashboard/
│   ├── core/                    # Lógica compartilhada
│   ├── nicegui_app/            # App NiceGUI
│   ├── streamlit_app/          # App Streamlit
│   ├── utils/                  # Utilitários
│   └── config.py
├── scripts/                    
│   └── relay_server.py
├── data/                       # CSVs gerados
└── main.py                     # Entry point
```

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="#" title="Carlo Rondinoni">
        <img src="https://lh3.googleusercontent.com/a/ACg8ocJkEeuUxD9szj3FaElT1Sq5I5AhdeyJrcVx50g3UTmy5xyeu_gE=s288-c-no" width="100px;" alt="Foto do Carlo"/><br>
        <sub>
          <b>Carlo Rondinoni</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Thais Marchetti">
        <img src="https://media.licdn.com/dms/image/v2/D4D03AQH0JJ0tC3lPdw/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1689595835164?e=2147483647&v=beta&t=-OimYZS5i41I1br2F_Pf0vjEod6mxoCrdIVqkUa8mik" width="100px;" alt="Foto da Thais"/><br>
        <sub>
          <b>Thais Marchetti</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Lucas Betioli">
        <img src="https://media.licdn.com/dms/image/v2/D4E03AQFyS-64Yi4IWQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1670982222858?e=2147483647&v=beta&t=Al4_hnmRXrmKBNlWMldP7QROJejUgcrU9cW_Pmr8mmc" width="100px;" alt="Foto do Lucas"/><br>
        <sub>
          <b>Lucas Betioli</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="#" title="Victor Malheiro">
        <img src="https://miro.medium.com/max/360/0*1SkS3mSorArvY9kS.jpg" width="100px;" alt="Foto do Victor"/><br>
        <sub>
          <b>Victor Malheiros</b>
        </sub>
      </a>
    </td>
  </tr>
</table>

##  Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

## NeuroMat Support

Este trabalho é apoiado pelo NeuroMat - Centro de Pesquisa, Inovação e Difusão em Neuromatemática (CEPID NeuroMat) estabelecido em 2013 na Universidade de São Paulo. Homepage: http://neuromat.numec.prp.usp.br