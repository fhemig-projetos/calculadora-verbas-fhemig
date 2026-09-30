# Build do executável Windows (PyInstaller)

## Visão geral

O `.exe` empacota o Python, o Streamlit e todas as dependências da aplicação
(pandas, reportlab, supabase, bcrypt, streamlit-cookies-controller). Quem
recebe o executável **não precisa instalar Python nem nada via pip** — basta
rodar o `.exe`. Ele sobe um servidor Streamlit em `localhost` e abre o
navegador padrão automaticamente.

O que o `.exe` faz sozinho: nada é instalado na máquina do usuário além do
próprio arquivo — não mexe em registro, não precisa de admin, não instala
serviço. É um programa autocontido rodando localmente.

## Por que `secrets.toml` NÃO vai dentro do `.exe`

`.streamlit/secrets.toml` tem a chave admin do Supabase e a senha SMTP. Um
`.exe` do PyInstaller é trivialmente extraível (7-zip, `pyinstxtractor` etc.),
então qualquer coisa embutida nele deve ser tratada como pública. Por isso:

- O build (`calculadora.spec`) empacota `assets/`, `data/tabelas.json` e
  `.streamlit/config.toml` — mas **não** `secrets.toml`.
- Em tempo de execução, `desktop/launcher.py` aponta a variável de ambiente
  `STREAMLIT_SECRETS_FILES` para `.streamlit/secrets.toml` **ao lado do
  `.exe`**, não dentro dele. Se o arquivo não existir ali, o launcher avisa e
  encerra em vez de subir sem configuração.
- Isso significa que cada pessoa que rodar o `.exe` precisa receber esse
  `secrets.toml` por um canal separado e confiável (não pelo mesmo zip do
  `.exe`, não por e-mail em texto puro). Na prática isso tende a limitar a
  distribuição a um grupo pequeno e controlado — se o objetivo é abrir acesso
  amplo, vale reconsiderar dar a cada usuário uma chave com permissões mais
  restritas que a `service_role`/admin atual, em vez de replicar a mesma chave
  admin em N máquinas.

## Passo a passo (rodar no Windows, não no WSL/Linux)

PyInstaller gera binário para a plataforma onde ele roda — build precisa
acontecer em Windows para gerar `.exe`.

```powershell
# 1. Ambiente virtual limpo
python -m venv venv-build
venv-build\Scripts\activate

# 2. Dependências de build
pip install -r desktop\requirements-build.txt

# 3. (opcional) gerar o ícone .ico a partir do assets\icone.png
#    ex: usando Pillow
python -c "from PIL import Image; Image.open('assets/icone.png').save('desktop/icone.ico')"

# 4. Build
pyinstaller desktop\calculadora.spec --clean

# 5. Resultado em dist\CalculadoraVerbasFhemig\
#    Rode o .exe direto dessa pasta pra testar antes de distribuir.
```

## Preparando a pasta para distribuir

Dentro de `dist\CalculadoraVerbasFhemig\`, antes de zipar para enviar:

```
CalculadoraVerbasFhemig\
  CalculadoraVerbasFhemig.exe
  _internal\...              (gerado pelo PyInstaller, não mexer)
  .streamlit\
    secrets.toml             <- copiar aqui manualmente, fora do zip público
```

Recomendado: distribuir o `.exe` (sem secrets) por um canal, e o
`secrets.toml` por outro canal (ex.: pasta de rede da FHEMIG, Bitwarden,
e-mail institucional criptografado) — nunca os dois juntos no mesmo arquivo.

## Teste antes de distribuir

1. Rode `CalculadoraVerbasFhemig.exe` numa máquina limpa (sem Python, idealmente
   uma VM Windows nova) para confirmar que não há dependência escondida do seu
   ambiente de dev.
2. Confirme que o antivírus/SmartScreen não bloqueia — executáveis do
   PyInstaller sem assinatura digital costumam disparar aviso do Windows
   Defender SmartScreen ("Windows protegeu seu PC"). Isso é esperado sem
   assinatura de código; para eliminar o aviso seria necessário um certificado
   de assinatura de código (tem custo, é outro passo, não incluído aqui).
3. Teste login, geração de PDF (reportlab) e persistência (Supabase) de fato
   — essas três áreas são as que mais comumente dão erro de "arquivo não
   encontrado" ou import faltando em builds do PyInstaller.

## Problemas comuns

- **App abre e fecha na hora**: rode pelo terminal (`CalculadoraVerbasFhemig.exe`
  direto no PowerShell, não clicando duas vezes) pra ver o traceback antes da
  janela fechar. `console=True` no spec já deixa o console visível para isso.
- **`ModuleNotFoundError` em algo do streamlit/supabase**: falta de
  hiddenimport — adicione o módulo em `hiddenimports` no `calculadora.spec`.
- **Ícone/logo não aparece no PDF**: confirme que `assets/` foi mesmo copiado
  pro `datas` do spec (já está, mas confira o caminho gerado em
  `dist\...\_internal\assets`).
- **Porta 8501 ocupada**: o launcher já escolhe outra porta livre automaticamente
  (`porta_livre()` em `launcher.py`), não precisa intervir.
