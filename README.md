# BND Diesel — Sistema de Gestão de Orçamentos

MVP web responsivo para apoiar a organização administrativa da BND Diesel, com cadastro de clientes, veículos e serviços, criação de orçamentos e acompanhamento de status.

## Funcionalidades desta versão

- Autenticação de usuários com o sistema nativo do Django.
- Painel administrativo com indicadores calculados a partir do banco de dados.
- Cadastro, consulta, edição e exclusão de clientes, veículos e serviços.
- Criação de orçamentos com um ou mais itens de serviço (até dez por orçamento).
- Cálculo do total no servidor e preservação do preço/descrição do serviço no momento da criação do orçamento.
- Busca de orçamentos, filtro por status e atualização de situação por requisição POST.
- Interface responsiva com navegação por teclado, rótulos associados e indicação textual de status.
- Testes automatizados e pipeline de integração contínua com GitHub Actions.

## Tecnologias

- Python 3.14
- Django 5.2 LTS (dependência fixada em 5.2.19)
- Bootstrap 5.3.8 (CSS carregado pelo CDN oficial de distribuição)
- PostgreSQL via Psycopg 3.3.8
- SQLite como banco padrão para desenvolvimento local e execução dos testes

## Requisitos

- Python 3.14 instalado.
- Git (para versionamento).
- Navegador atualizado.

O PostgreSQL é opcional para executar localmente. O projeto inicia com SQLite para reduzir a configuração inicial; a conexão PostgreSQL pode ser habilitada por variáveis de ambiente.

## Executar no Windows com VS Code

1. Extraia ou abra a pasta do projeto no VS Code.
2. Abra o terminal integrado em **Terminal → Novo Terminal**.
3. Crie o ambiente virtual:

   ```powershell
   py -3.14 -m venv .venv
   ```

4. Ative o ambiente virtual:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Se o PowerShell bloquear a ativação, use o terminal CMD e execute:

   ```cmd
   .venv\Scripts\activate.bat
   ```

5. Instale as dependências:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

6. Aplique as migrações do banco local:

   ```powershell
   python manage.py migrate
   ```

7. Crie seu usuário administrador:

   ```powershell
   python manage.py createsuperuser
   ```

   Informe o usuário, e-mail (se solicitado) e uma senha pessoal. Não compartilhe nem envie a senha ao repositório.

8. Inicie o servidor de desenvolvimento:

   ```powershell
   python manage.py runserver
   ```

9. Acesse `http://127.0.0.1:8000/` e entre com o usuário criado.
10. Opcionalmente, carregue dados fictícios para explorar o fluxo: `python manage.py seed_demo`.

## Executar os testes

Com o ambiente virtual ativo, execute:

```powershell
python manage.py test
```

Verificações adicionais:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Utilizar PostgreSQL

Para mudar do SQLite para PostgreSQL, crie um banco chamado `bnd_diesel` e defina as variáveis de ambiente antes de iniciar o Django:

```text
DB_ENGINE=postgresql
DB_NAME=bnd_diesel
DB_USER=postgres
DB_PASSWORD=sua_senha_local
DB_HOST=127.0.0.1
DB_PORT=5432
```

No PowerShell, elas podem ser definidas para a sessão atual com `$env:NOME_DA_VARIAVEL="valor"`. O arquivo `.env.example` serve como referência; ele não contém credenciais e não é carregado automaticamente pelo Django.

## Estrutura do projeto

```text
config/                 Configurações e URLs do Django
oficina/                Modelos, formulários, regras, views e testes
oficina/migrations/     Histórico da estrutura do banco de dados
templates/              Interfaces HTML do sistema
static/css/             Estilos visuais
static/js/              Interações do navegador
.github/workflows/      Pipeline de integração contínua
docs/                   Protótipo HTML original preservado como referência
```

## Modelo de dados

- **Cliente**: nome e meios de contato mínimos para a rotina administrativa.
- **Veículo**: marca, modelo, ano, placa opcional e vínculo com um cliente.
- **Serviço**: nome, descrição, preço de referência e disponibilidade.
- **Orçamento**: cliente, veículo, código, data, validade, observações e status.
- **Item do orçamento**: descrição, quantidade e preço unitário registrado no momento da criação.

O preço e a descrição do item são copiados para o orçamento. Assim, uma alteração posterior no cadastro do serviço não modifica o histórico de orçamentos já criados.

## Segurança e privacidade

- Todas as páginas administrativas exigem autenticação.
- Os formulários usam proteção CSRF e validação no servidor.
- A atualização de status é feita por POST.
- As consultas são realizadas pelo ORM do Django.
- Não versionar arquivos `.env`, banco local, senhas, tokens ou dados reais de clientes.
- Para uso fora do ambiente acadêmico/local, revisar a configuração de produção, HTTPS, backups, permissões e política de privacidade antes de disponibilizar o sistema.

## Escopo e limitações

Esta versão é um MVP acadêmico. Não contempla emissão fiscal, controle de estoque, integração com WhatsApp, pagamentos, envio automático de orçamento ou implantação em ambiente de produção. O cadastro de usuários é administrado pelo Django; não há recuperação de senha ou gestão de perfis avançada nesta primeira versão.

## Histórico de implementação

As alterações devem ser registradas no Git com mensagens semânticas, por exemplo:

- `chore: criar estrutura inicial do projeto Django`
- `feat: implementar cadastro de clientes e veículos`
- `feat: implementar criação e consulta de orçamentos`
- `test: adicionar testes para cadastros e orçamentos`
- `ci: configurar GitHub Actions para executar testes`

Use essas mensagens somente quando a alteração correspondente estiver concluída.
