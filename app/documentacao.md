# Documentação Técnica: Wikipédia GeoHist

Este documento apresenta a especificação técnica detalhada, arquitetura, decisões de design, metodologia e implementação da plataforma **Wikipédia GeoHist**, uma ferramenta interativa desenvolvida em Python com o framework **Reflex** para extração, curadoria e visualização geográfica e temporal de trajetórias biográficas baseadas na Wikipédia em português e no Wikidata.

---

## 1. Introdução e Objetivo do Projeto

O **Wikipédia GeoHist** surgiu da necessidade de converter as ricas narrativas textuais não estruturadas de biografias contidas na Wikipédia em dados históricos e geoespaciais estruturados, facilitando a análise de movimentos migratórios, longevidade, distribuição temporal e completude de informações de personagens históricos de língua portuguesa ou relevância universal.

A aplicação provê aos pesquisadores, estudantes e entusiastas de história:
1. Um fluxo de trabalho editorial estruturado para validação e extração de dados.
2. Visualização cartográfica interativa dos locais de nascimento e óbito.
3. Reconstrução cronológica narrativa de trajetórias de vida unificadas.
4. Análises estatísticas descritivas sobre os biografados.
5. Persistência de dados local segura através de banco de dados SQLite embarcado.

---

## 2. Arquitetura do Sistema e Fluxo de Dados

O ecossistema é baseado no paradigma do framework **Reflex**, o qual separa claramente o estado lógico e de dados (Backend em Python executado no servidor) da camada de interface (compilada para Next.js / React no cliente).


┌────────────────────────────────────────────────────────┐
│                     CLIENTE (UI)                       │
│  - Next.js / Tailwind CSS / Leaflet Map                │
└───────────┬───────────────────────────────▲────────────┘
            │ Eventos (e.g. Pesquisa)       │ Atualização de Estado
┌───────────▼───────────────────────────────┴────────────┐
│                     SERVIDOR (State)                   │
│  - State & Event Handlers (ResearchState, AuthState)   │
└───────────┬───────────────────────────────▲────────────┘
            │ SQLite Query                  │ Dataset / Rows
┌───────────▼───────────────────────────────┴────────────┐
│               PERSISTÊNCIA & EXTERNOS                  │
│  - geohist.db / geohist_auth.db (SQLite)               │
│  - API Wikipédia & Wikidata                            │
└────────────────────────────────────────────────────────┘


### 2.1 Módulos de Estado (States)
- **AuthState (`app/states/auth_state.py`)**: Controla o cadastro e sessão de usuários de forma segura. Utiliza hashing SHA-256 com salting dinâmico armazenado em tabela SQLite independente (`geohist_auth.db`).
- **ResearchState (`app/states/research_state.py`)**: Coordena as buscas na API da Wikipédia, requisições de propriedades semânticas no Wikidata, extração lógica de coordenadas geográficas, agrupamento temporal de eventos e gestão de persistência local em `geohist.db`.

### 2.2 Estrutura de Diretórios da Aplicação
- `app/app.py`: Ponto de entrada, configuração do aplicativo, roteamento e esqueleto visual.
- `app/states/`: Lógica de controle, chamadas de API e manipulação do banco de dados SQLite.
- `app/components/`: Componentes modulares reutilizáveis (Visualização de Mapa, Linha do Tempo, Análises, Workbench de Pesquisa, Tabela e Dashboard).

---

## 3. Tecnologias Utilizadas e Justificativa

| Tecnologia | Papel no Sistema | Justificativa |
| :--- | :--- | :--- |
| **Python 3.13** | Linguagem Principal | Fornece ambiente maduro para ciência de dados, manipulação de texto e chamadas de API. |
| **Reflex 0.9.2** | Full-Stack Web Framework | Permite escrever toda a interface reativa e lógica de negócio em Python puro, com compilação transparente para Next.js e Tailwind CSS. |
| **Leaflet / reflex-enterprise** | Motor de Mapas | Integração de mapas dinâmicos altamente performáticos para plotagem de coordenadas geográficas. |
| **SQLite3** | Banco de dados embarcado | Armazenamento local rápido e sem dependências externas de infraestrutura para sessões persistentes de usuários. |
| **Wikipédia / Wikidata APIs** | Provedor de Conteúdo | APIs oficiais abertas para buscar artigos na Wikipédia lusófona e extrair metadados estruturados (nacionalidades, coordenadas, datas). |

---

## 4. Metodologia de Extração de Dados Biográficos

O processo de extração e conversão de textos enciclopédicos em pontos estruturados obedece às seguintes etapas:

1. **Busca Textual (Wikipedia API)**: Uma consulta `action=query&list=search` é enviada para obter os títulos e resumos mais relevantes.
2. **Resolução de Entidades (Wikibase Item)**: Ao selecionar um artigo, recuperamos o ID Wikidata exclusivo (ex: `Q5` para seres humanos, `Q569` para data de nascimento).
3. **Validação de Tipo (Filtro Humano)**: A claim `P31` (Instância de) é verificada. Se não corresponder a `Q5` (Humano), a interface notifica que o artigo não é elegível para extração biográfica.
4. **Coleta de Propriedades Semânticas**:
   - `P569`: Data de nascimento
   - `P570`: Data de falecimento
   - `P19`: Local de nascimento
   - `P20`: Local de falecimento
   - `P27`: País de nacionalidade
5. **Geocodificação e Tratamento de Exceções**: Se o local de nascimento ou óbito não possuir coordenadas próprias (`P625`), o sistema resolve as coordenadas com fallback automático para o país correspondente (`P17`).
6. **Cálculo da Métrica de Completude**: É calculado o percentual de dados recuperados com base na presença dos 6 atributos principais, categorizando-os em buckets estruturados para análise.

---

## 5. Decisões de Design de Interface (UX/UI)

- **Modo Escuro Dinâmico (Dark Mode)**: Implementado de ponta a ponta com classes condicionais do Tailwind CSS coordenadas pelo estado central. Oferece conforto visual para leitura prolongada de artigos históricos.
- **Overlays Flutuantes no Mapa**: Para manter o foco no mapa imersivo de visualização de rotas de vida, as estatísticas, legendas e o mini-card do perfil selecionado são renderizados como camadas translúcidas flutuantes com efeito de backdrop blur, imitando painéis GIS modernos.
- **Cards de Status e Indicadores de Qualidade**: Emprego de tags coloridas (`bg-emerald-50` para registros com completude em 100% e `bg-amber-50` para parciais) para dar feedback imediato sobre a saúde dos dados.
- **Workspaces Claramente Delimitados**: Interface modular baseada em abas laterais consistentes que guiam o usuário intuitivamente através do ciclo de pesquisa: Dashboard -> Pesquisa -> Mapa -> Linha do Tempo -> Análises -> Tabela de Exportação.

---

## 6. Correções de Bugs Significativos

Durante o ciclo de desenvolvimento, as seguintes correções de bugs foram implementadas:
- **Concorrência e Locks de Estado**: Correção de acessos paralelos a variáveis compartilhadas por meio de uso rigoroso de isolamento em manipuladores assíncronos (`async with self`).
- **Tratamento de Desambiguação**: O bloqueio explícito de botões de extração para páginas de desambiguação previne falhas na requisição de entidades semânticas vazias.
- **Prevenção de Falhas de Tipo no Frontend (None Type Check)**: Adição de guards do tipo `rx.cond` no JSX gerado para evitar chamadas de métodos como `.upper()` ou split em propriedades vazias ou não-resolvidas (prevenindo telas brancas por exceções não tratadas no JavaScript).
- **Migração Segura de Esquema SQLite**: Implementação de verificação dinâmica `PRAGMA table_info` ao conectar no SQLite para garantir a criação e existência de novas colunas como `image_url` sem quebrar bancos de dados já criados.

---

## 7. Limitações e Melhorias Futuras

### Limitações Atuais
1. **Dependência das APIs Públicas**: Flutuações ou limites de taxa na API oficial da Wikimedia podem interferir no tempo de resposta das consultas em tempo real.
2. **Foco Monolíngue**: Extração otimizada apenas para a Wikipédia em português, embora muitos registros de personagens globais possam conter dados mais completos nas versões em inglês ou alemão.
3. **Visualizações Complexas Estáticas**: Os gráficos descritivos utilizam grids Tailwind progressivos em vez de bibliotecas pesadas de SVG dinâmico, para manter a aplicação rápida e responsiva em ambientes restritos.

### Melhorias Futuras
- Integração de buscas multilingues com consolidação automática de dados do Wikidata internacional.
- Geração automática de mapas de conexões conectando os pontos de nascimento ao óbito por polilinhas dinâmicas para traçar o vetor físico de deslocamento da vida da personalidade.
- Capacidade de anexar documentos e PDF locais adicionais para enriquecimento manual de lacunas deixadas pela Wikipédia.
- Sistema de tags personalizadas para agrupar composições de biografias de forma temática (ex: "Cientistas do Século XX", "Escritores Modernistas").

---

## 8. Comparativo de Escopo

| Recurso Previsto | Escopo Original (Artigo Técnico) | Implementação Wikipédia GeoHist |
| :--- | :--- | :--- |
| **Curadoria de Artigos** | Busca básica por palavra-chave. | Busca avançada com verificação em tempo real de tipo biográfico (`Q5`) e desambiguação. |
| **Estrutura Biográfica** | Exibição em lista de metadados. | Fichas com indicador de completude, avatares gerados automaticamente via DiceBear e fotos oficiais da Wikipédia. |
| **Cartografia Histórica** | Plotagem básica de coordenadas. | Mapa interativo Leaflet dinâmico com marcadores personalizados, Tooltips, Popups e fallback geográfico para o país de origem. |
| **Cronologia** | Lista de anos de nascimento e morte. | Linha do tempo narrativa estruturada com filtros por tipo de evento e focalização instantânea de perfil no workbench. |
| **Segurança e Persistência** | Armazenamento volátil em memória. | Banco SQLite embarcado resiliente persistindo histórico de pesquisa, sessões de usuário com senhas criptografadas e composições de registros completos. |
