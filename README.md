# Biomag TMS Experiment Dashboard v0.2.0

<img src="https://github.com/biomaglab.png" alt="Logo Biomag">

> Interface gráfica web moderna para visualização e controle de eventos durante experimentos de TMS acoplados a EMG usando o InVesalius.

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