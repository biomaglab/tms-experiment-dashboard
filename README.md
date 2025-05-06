# Biomag TMS Experiment Dashboard

<img src="https://raw.githubusercontent.com/biomaglab/tms-experiment-dashboard/master/static/biomag_logo.jpg" alt="Logo Biomag">

> Interface gráfica em formato web para visualização e controle de eventos durante experimentos de TMS acoplados a EMG usando o InVesalius.

### Ajustes e melhorias

O projeto está em desenvolvimento e as próximas atualizações serão voltadas para as seguintes tarefas:

- [x] Adicionados recursos de metadados para adequação com os modelos de dados do CEPID Neuromat
- [x] Integração dos scripts para a aquisição de eventos durante o experimento (socket messages)
- [x] Implementação de um sistema de cadastramento de experimentos usando o esquema json
- [ ] Incremento da capacidade dos scripts de mostrar os movimentos de um ou mais braços robóticos
- [ ] Envio de mensagens por socket para a rede local do InVesalius Neuronavigator
- [ ] Implementação da visualização do andamento completo do experimento


## 💻 Pré-requisitos

Antes de começar, verifique se você instalou as seguintes dependências:

- Estão instalados as bibliotecas python: serial e streamlit (ver setup.py)
- Você tem uma máquina Linux/Mac ou Windows com WSL ou Anaconda/Miniconda.
- Você leu este README.

## 🚀 Instalando Biomag TMS Experiment Dashboard

Para instalar o Dashboard, siga estas etapas:

Linux e macOS:

```
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
```

Windows:

```
git clone git@github.com:biomaglab/tms-experiment-dashboard.git
```

## ☕ Usando o Biomag Dashboard, 

Para usar Dashboard, siga estas etapas:

```
- Abra o prompt do Anaconda ou o terminal Linux e navegue até a pasta que foi clonada do repositório (algo como C:\Users\userName\Documents\GitHub\tms-experiment-dashboard
- Digite "code ." para abrir o VS Code, caso queira verificar os códigos a serem rodados
- Em seguida, execute o script main_loop.py. Observação: o main_loop deve ser executado usando o **Python Console**:

`python.exe relay_server.py 127.0.0.1 5000`
 
Depois disso, execute o script InVesalius app.py (https://github.com/invesalius/invesalius3) com o argumento --remote-host, especificando a mesma porta do servidor de retransmissão:

`python.exe c:/Users/user/GitHub/invesalius3/app.py --remote-host http://localhost:5000`

E depois:

`streamlit run web_UI_streamlit_trials.py`

ou

`python.exe ./main_nicegui.py`


```

## 📫 Contribuindo para o Biomag TMS Experiment Dashboard

Para contribuir com Biomag TMS Experiment Dashboard, siga estas etapas:

1. Bifurque este repositório.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

Como alternativa, consulte a documentação do GitHub em [como criar uma solicitação pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

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

## 😄 Seja um dos contribuidores

Quer fazer parte desse projeto? Clique [AQUI](CONTRIBUTING.md) e leia como contribuir.

## 📝 Licença

Esse projeto está sob licença. Veja o arquivo [LICENÇA](LICENSE.md) para mais detalhes.

# Este trabalho é apoiado pelo NeuroMat

O Centro de Pesquisa, Inovação e Difusão em Neuromatemática (CEPID NeuroMat, ou simplesmente NeuroMat) é um centro de pesquisa brasileiro estabelecido em 2013 na Universidade de São Paulo que se dedica a integrar modelagem matemática e neurociência teórica. Entre as principais missões do NeuroMat está a criação de um novo sistema matemático para entender dados neurais e o desenvolvimento de ferramentas computacionais neurocientíficas de código aberto, mantendo um papel ativo no contexto do conhecimento aberto, ciência aberta e divulgação científica. O centro de pesquisa é financiado pela Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP). Homepage do NeuroMat: http://neuromat.numec.prp.usp.br
- No terminal do sistema ou no do VS Code use o comando: streamlit run web_UI_streamlit_trials.py
- Aguarde a página da interface ser gerada em uma nova aba do seu navegador principal
- Caso modifique algo nos códigos (ou nos arquivos da pasta), salve o código e clique Atualizar (F5) na pagina do navegador web.