# Biomag TMS Experiment Dashboard 

<p align="center">
  <img src="https://github.com/biomaglab.png" width="100px" alt="Logo Biomag">
</p>

> Interface gráfica web moderna para visualização e controle de eventos durante experimentos de TMS acoplados a EMG usando o InVesalius.

## 🚀 Instalação Rápida

### Opção 1: Com uv (Recomendado)

```bash
# Clone o repositório
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
cd tms-experiment-dashboard

# Instale com NiceGUI (recomendado)
uv sync --extra nicegui

# OU instale com Streamlit
uv sync --extra streamlit

# OU instale ambos
uv sync --extra all
```

### Opção 2: Com pip/venv (Tradicional)

```bash
# Clone o repositório
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
cd tms-experiment-dashboard

# Crie um ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instale as dependências
pip install -e .

# OU instale com NiceGUI
pip install -e .[nicegui]

# OU instale com Streamlit
pip install -e .[streamlit]

# OU instale com ambos
pip install -e .[all]
```

## ☕ Como Usar

### 1. Inicie o servidor de relay

**Com uv:**
```bash
uv run python scripts/relay_server.py 127.0.0.1 5000
```

**Com pip/venv:**
```bash
# Certifique-se que o ambiente virtual está ativado
python scripts/relay_server.py 127.0.0.1 5000
```

### 2. (Opcional) Inicie o InVesalius

```bash
python /caminho/para/invesalius3/app.py --remote-host http://localhost:5000
```

### 3. Inicie o Dashboard

**Com uv:**
```bash
# Auto-detecção (NiceGUI ou Streamlit)
uv run python main.py
```

**Com pip/venv:**
```bash
# Certifique-se que o ambiente virtual está ativado
python main.py
```

**Acesso:**
- NiceGUI: http://localhost:8084
- Streamlit: Abre automaticamente no navegador

## 🤝 Colaboradores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/crondinoni" title="Nome">
        <img src="https://github.com/crondinoni.png" width="100px;" alt="Foto do/a Nome"/><br>
          <b>Carlo Rondinoni</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/MarcioCamposJr" title="Nome">
        <img src="https://github.com/MarcioCamposJr.png" width="100px;" alt="Foto do/a Nome"/><br>
        <sub>
          <b>Marcio Campos</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/thaismarchetti" title="Nome">
        <img src="https://github.com/thaismarchetti.png" width="100px;" alt="Foto do/a Nome"/><br>
        <sub>
          <b>Thais Marchetti</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/LucasBetioli123" title="Nome">
        <img src="https://github.com/LucasBetioli123.png" width="100px;" alt="Foto do/a Nome"/><br>
        <sub>
          <b>Lucas Betioli</b>
        </sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/vhemalheiro" title="Nome">
        <img src="https://github.com/vhemalheiro.png" width="100px;" alt="Foto do/a Nome"/><br>
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