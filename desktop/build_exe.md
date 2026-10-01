# Build do executável Windows (PyInstaller)

Passo a passo para gerar o `CalculadoraVerbasFhemig.exe`. **Precisa rodar em Windows**
(PyInstaller gera binário para a plataforma onde roda — não serve WSL/Linux).

## O que o executável faz

- Empacota Python, Streamlit e todas as dependências: quem recebe **não instala Python
  nem nada via pip**.
- Ao abrir, sobe um servidor Streamlit em `localhost` (porta 8501, ou outra livre) e
  abre o app numa **janela própria, sem barra de endereço** (Chrome; se não houver,
  Edge; se não houver nenhum, o navegador padrão).
- **Sem console.** Logs vão para `%LOCALAPPDATA%\CalculadoraFhemig\app.log`.
- **Fechar a janela encerra o servidor** (só vale no modo janela; no fallback para o
  navegador padrão o processo segue em segundo plano).
- Não instala nada, não mexe em registro, não precisa de admin.
- **Funciona sem rede.** Não há login nem servidor externo: o histórico da análise e a
  base de servidores ficam num SQLite local (ver "Dados locais" abaixo).

## Pré-requisitos

- Windows 10/11 com Python 3.11+ (o mesmo usado no desenvolvimento).
- `desktop\icone.ico` (gerado no passo 3 abaixo, a partir de `assets/icone.png`).

## Passo a passo

Rode tudo a partir da **raiz do projeto** (PowerShell):

```powershell
# 1. Ambiente virtual
python -m venv venv
venv\Scripts\activate

# 2. Dependências (requirements.txt já inclui pyinstaller)
pip install -r requirements.txt

# 3. Gerar o ícone .ico (o PyInstaller não aceita .png) — antes do build
python -c "from PIL import Image; Image.open('assets/icone.png').save('desktop/icone.ico')"

# 4. Build — sempre com --clean, senão o PyInstaller reaproveita análise antiga
pyinstaller desktop/calculadora.spec --clean --noconfirm

# 5. Resultado
#    dist\CalculadoraVerbasFhemig\CalculadoraVerbasFhemig.exe
```

> **Git Bash / MSYS2:** a barra invertida (`\`) é caractere de escape nesses terminais e
> some do caminho (erro `Spec file "desktopcalculadora.spec" not found!`). Use barras
> normais (`desktop/calculadora.spec`) e ative o venv com `source venv/Scripts/activate`.
> Em PowerShell as duas formas funcionam; por isso o comando do build usa `/`.

O build leva alguns minutos (o Streamlit é grande). Avisos de "hidden import not found"
no log costumam ser inofensivos; erro só se o app falhar ao abrir.

## Testar antes de distribuir

1. Abra `dist\CalculadoraVerbasFhemig\CalculadoraVerbasFhemig.exe`: deve aparecer só a
   janela do app (sem console, sem barra de endereço).
2. Teste **importar a planilha de servidores** (.csv e .xlsx), a **busca por MASP/admissão**,
   **geração de PDF** e **persistência** (feche e reabra: a análise deve voltar) — são as
   áreas que mais quebram em build PyInstaller.
3. Fechar a janela deve encerrar o processo (confira no Gerenciador de Tarefas).
4. Idealmente teste numa máquina/VM Windows limpa, sem Python, para achar dependência
   escondida do seu ambiente.
5. O Windows SmartScreen ("Windows protegeu seu PC") deve aparecer: o `.exe` não é
   assinado digitalmente. Orientar o usuário a clicar em "Mais informações" →
   "Executar assim mesmo". Eliminar o aviso exige certificado de assinatura de código
   (custo e processo à parte).

## Distribuir

Zipar a pasta **inteira** `dist\CalculadoraVerbasFhemig\` (o `.exe` sozinho não roda: ele
depende da pasta `_internal\`). O usuário descompacta e abre o `.exe`.

## Dados locais (SQLite) e base de servidores

Arquivo: `%LOCALAPPDATA%\CalculadoraFhemig\calculadora.db` (um por usuário do Windows).

- **Análise ativa:** dados do servidor + histórico de cálculos, gravados a cada alteração e
  restaurados ao reabrir o app. Só existe uma análise (salvar sobrescreve a anterior).
- **Base de servidores:** importada de planilha pelo painel "Base de servidores" no topo
  do app (aceita `.csv` ou `.xlsx`). Cada importação **substitui** a base inteira; se a
  planilha for inválida, a base anterior é mantida.
- **Colunas obrigatórias** (mesmo layout do CSV de dados funcionais): `Nome Servidor`,
  `MASP`, `Nº Admissão`, `Masp/Admissão`, `Data Inicio`, `Data Fim Efetiva`, `Cod Carreira`,
  `Símbolo Vencimento`, `Nivel`, `Grau`, `Carga Horária Pagamento`.
- **Fluxo mensal:** gere a planilha (de preferência só com os servidores da unidade),
  envie à unidade, e ela importa pelo painel. Não precisa de novo build.
- Para "zerar" tudo (histórico + base), apague o `calculadora.db` com o app fechado.

## Segurança

- O `.exe` **não embute credenciais** (o `secrets.toml`/Supabase/SMTP foram removidos).
- A planilha de servidores contém **dados pessoais (LGPD)**: envie só às unidades
  autorizadas, de preferência recortada por unidade, e por canal institucional.
- O banco local não é criptografado: quem acessa a conta do Windows lê o arquivo.

## Problemas comuns

- **Janela não abre / fecha sozinha:** veja `%LOCALAPPDATA%\CalculadoraFhemig\app.log`.
  Para ver o traceback ao vivo, troque `console=False` por `console=True` no
  `calculadora.spec` e refaça o build.
- **`No such component directory` / `ModuleNotFoundError` / `PackageNotFoundError`:**
  falta dado ou módulo no bundle. Adicione `collect_data_files("pacote")`,
  `copy_metadata("pacote")` ou o módulo em `hiddenimports` no `calculadora.spec`
  (já cobertos: streamlit, tzdata, reportlab, openpyxl, sqlite3).
- **Busca não encontra o servidor:** a base não foi importada (veja o painel no topo) ou o
  MASP/Nº de admissão não estão na planilha. O formulário segue podendo ser preenchido à mão.
- **Porta 8501 ocupada:** o launcher escolhe outra automaticamente.
