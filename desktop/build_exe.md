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

## Pré-requisitos

- Windows 10/11 com Python 3.11+ (o mesmo usado no desenvolvimento).
- `.streamlit\secrets.toml` **preenchido** na raiz do projeto — o build **aborta** sem ele.
- (opcional) `desktop\icone.ico`. Para gerar a partir do PNG:
  `python -c "from PIL import Image; Image.open('assets/icone.png').save('desktop/icone.ico')"`

## Passo a passo

Rode tudo a partir da **raiz do projeto** (PowerShell):

```powershell
# 1. Ambiente virtual limpo (evita empacotar lixo do ambiente de dev)
python -m venv venv-build
venv-build\Scripts\activate

# 2. Dependências de build (requirements.txt + pyinstaller)
pip install -r desktop\requirements-build.txt

# 3. Build — sempre com --clean, senão o PyInstaller reaproveita análise antiga
pyinstaller desktop\calculadora.spec --clean --noconfirm

# 4. Resultado
#    dist\CalculadoraVerbasFhemig\CalculadoraVerbasFhemig.exe
```

O build leva alguns minutos (o Streamlit é grande). Avisos de "hidden import not found"
no log costumam ser inofensivos; erro só se o app falhar ao abrir.

## Testar antes de distribuir

1. Abra `dist\CalculadoraVerbasFhemig\CalculadoraVerbasFhemig.exe`: deve aparecer só a
   janela do app (sem console, sem barra de endereço).
2. Teste **login**, **"Esqueci minha senha"** (código por e-mail), **geração de PDF** e
   **persistência** (Supabase) — são as áreas que mais quebram em build PyInstaller.
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

## Segurança — leia antes de distribuir

O build **empacota `secrets.toml` dentro do `.exe`** (decisão do responsável pelo projeto,
para distribuição às unidades). Um `.exe` do PyInstaller é trivialmente extraível
(7-zip, `pyinstxtractor`), então **qualquer pessoa que receber o executável consegue
ler as credenciais**: chave admin do Supabase (`service_role`) e senha SMTP.

- Distribua só para grupo pequeno e de confiança, enquanto essa chave for a admin.
- Para distribuição ampla, o ideal é trocar por credenciais de permissão restrita
  (ver pendência 4.34 em `contexto.md`).
- Para trocar credenciais **sem refazer o build**: coloque um `.streamlit\secrets.toml`
  ao lado do `.exe`; ele tem prioridade sobre o embutido.
- `secrets.toml` **nunca** vai para o Git (está no `.gitignore`).

## Problemas comuns

- **Janela não abre / fecha sozinha:** veja `%LOCALAPPDATA%\CalculadoraFhemig\app.log`.
  Para ver o traceback ao vivo, troque `console=False` por `console=True` no
  `calculadora.spec` e refaça o build.
- **`No such component directory` / `ModuleNotFoundError` / `PackageNotFoundError`:**
  falta dado ou módulo no bundle. Adicione `collect_data_files("pacote")`,
  `copy_metadata("pacote")` ou o módulo em `hiddenimports` no `calculadora.spec`
  (já cobertos: streamlit, supabase, tzdata, streamlit_cookies_controller, reportlab).
- **Build aborta com "secrets.toml não encontrado":** copie o arquivo para `.streamlit\`.
- **Login não persiste entre aberturas:** esperado — o perfil do navegador é temporário e
  apagado ao fechar, junto com o cookie de sessão. (Ver `contexto.md`, pendências.)
- **Porta 8501 ocupada:** o launcher escolhe outra automaticamente.
