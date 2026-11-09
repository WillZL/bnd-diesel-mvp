# Revisão Técnica — MVP BND Diesel

## 1. Objetivo

Registrar a auto-revisão técnica da aplicação BND Diesel, considerando a organização do código, a arquitetura adotada, a qualidade das funcionalidades e os cuidados de segurança.

## 2. Arquitetura e organização

O projeto utiliza uma arquitetura monolítica em camadas, adequada ao escopo do MVP e ao desenvolvimento individual. A pasta `config/` concentra as configurações e rotas gerais do Django. A aplicação `oficina/` organiza os modelos, formulários, regras de negócio, visualizações e testes. As pastas `templates/` e `static/` mantêm os arquivos de apresentação e os recursos utilizados pelo navegador.

Essa divisão favorece a separação de responsabilidades, facilita a manutenção e permite evoluir as funcionalidades sem introduzir a complexidade de uma arquitetura distribuída.

O cálculo dos totais dos orçamentos é realizado no servidor. Os itens também preservam a descrição e o preço praticados no momento da criação, evitando alterações indevidas no histórico quando o cadastro de serviços for atualizado.

## 3. Qualidade e segurança

Na revisão, foram considerados os seguintes controles implementados:

- Autenticação obrigatória nas páginas administrativas.
- Proteção CSRF e validação dos dados no servidor.
- Utilização do ORM do Django para consultas ao banco de dados.
- Atualização do status dos orçamentos por requisição POST.
- Separação de arquivos de configuração e orientação para não versionar senhas, tokens, arquivos `.env` ou dados reais de clientes.

Essas medidas contribuem para reduzir riscos de acesso indevido, requisições forjadas e manipulação inadequada de dados.

## 4. Pontos de atenção e evolução

Antes de qualquer disponibilização em produção, será necessário revisar a configuração de HTTPS, permissões de usuários, proteção de cookies, backups, gerenciamento de segredos e monitoramento de falhas.

Também será importante ampliar os testes conforme novas funcionalidades forem desenvolvidas e utilizar os resultados das validações com o representante da BND Diesel para orientar melhorias.

## 5. Conclusão

A auto-revisão reforçou a importância de manter o código organizado, as responsabilidades separadas e os controles de segurança aplicados no servidor. A documentação desses pontos facilita a compreensão e a evolução futura do MVP.