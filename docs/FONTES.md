# 📚 Fontes e Referências

Toda grandeza acústica exibida pela plataforma vem de uma destas fontes. Nenhuma foi
estimada sem rótulo, e nenhuma foi herdada de "sistema parecido".

Este documento existe para responder a uma pergunta de avaliador: **"de onde veio esse
número?"** — para qualquer número da tela.

---

## 1. Como ler esta lista

As fontes cumprem três papéis diferentes, e confundi-los é o erro mais comum:

| Papel | O que a fonte define | Exemplo |
|---|---|---|
| **Critério** | O que é aprovado ou reprovado | ABNT NBR 15575 — o veredito ATENDE / NÃO ATENDE |
| **Método** | Como o número é calculado ou medido | ISO 12354, ISO 16283, ISO 717 |
| **Dado** | O valor de entrada de um material ou sistema | Relatório de ensaio do IPT, catálogo ProAcústica |

A plataforma julga pela **norma brasileira**. As normas ISO e EN entram como método de
cálculo, de medição e de ponderação — não como critério de conformidade.

---

## 2. Critério normativo (o que aprova ou reprova)

### ABNT NBR 15575 — Edificações habitacionais: desempenho

A referência legal do veredito. Duas partes são usadas:

| Parte | Assunto | Indicador | Sentido |
|---|---|---|---|
| **15575-4** | Sistemas de vedação vertical interna e externa | $D_{nT,w}$ | **mínimo** — maior é melhor |
| **15575-3** | Sistemas de piso | $L'_{nT,w}$ | **máximo** — menor é melhor |

Cada parte define três patamares: **mínimo (M)**, **intermediário (I)** e **superior (S)**.
Os valores estão parametrizados por cenário em [`backend/criteria.py`](../backend/criteria.py):

| Cenário | Tipo | Mínimo | Intermediário | Superior |
|---|---|---|---|---|
| Parede entre unidades autônomas, com dormitório | aéreo | 45 dB | 50 dB | 55 dB |
| Parede entre unidades autônomas, sem dormitório | aéreo | 40 dB | 45 dB | 50 dB |
| Parede entre dormitório e área comum de trânsito | aéreo | 40 dB | 45 dB | 50 dB |
| Salas de aula / ambientes de ensino | aéreo | 45 dB | 50 dB | 55 dB |
| Laje/piso entre unidades autônomas | impacto | 80 dB | 65 dB | 55 dB |
| Laje de área de uso coletivo sobre unidades | impacto | 55 dB | 50 dB | 45 dB |
| Piso entre salas de aula (referencial) | impacto | 80 dB | 65 dB | 55 dB |

> Repare que nos cenários de impacto os limites **decrescem** do mínimo para o superior.
> Não é erro de digitação: é a consequência de $L'_{nT,w}$ ser um nível de ruído, e não
> uma atenuação.

O Anexo A da **ABNT NBR 15575-3:2013** (Tabelas A.1 e A.2) também é usado como fonte de
dado, para as lajes maciças do catálogo.

### ABNT NBR 10152:2017 (versão corrigida 2020) — Níveis de pressão sonora em ambientes internos

Usada como **referência de conforto**, num eixo separado e explicitamente declarado como
orientativo. Implementada em [`backend/conforto.py`](../backend/conforto.py):

| Ambiente | Recomendado |
|---|---|
| Dormitório | até 35 dB |
| Enfermaria / quarto hospitalar | até 35 dB |
| Biblioteca (área de leitura) | até 35 dB |
| Sala de estar | até 40 dB |
| Sala de aula | até 40 dB |
| Escritório individual | até 40 dB |

**Por que "orientativa":** a NBR 10152 trata do nível de ruído de fundo ($L_{Aeq}$) do
ambiente como um todo. A plataforma calcula o ruído que atravessa **um** elemento
construtivo. Comparar os dois ajuda o leigo a entender a ordem de grandeza, mas não
constitui verificação formal da NBR 10152 — e a interface diz isso, na tela, junto do
resultado.

### ANSI/ASA S12.60-2010/Part 1 — Acoustical Performance Criteria for Schools

Fonte do teto de **0,60 s** de tempo de reverberação, válido para salas de aula com até
283 m³.

**Escopo respeitado:** a norma só é citada quando o ambiente receptor selecionado é uma
sala de aula. Para dormitórios e demais ambientes, a mesma faixa de 0,40–0,60 s é
apresentada como referência de conforto para a fala, com a ressalva de que a NBR 15575
não fixa limite de reverberação para eles. Antes desta revisão, a norma era invocada para
qualquer ambiente — uma aplicação fora do escopo dela.

### WHO — Environmental Noise Guidelines for the European Region (2018)

Organização Mundial da Saúde, Escritório Regional para a Europa, Copenhague.
Embasa o enquadramento do ruído como questão de saúde — sono, cognição, incômodo — e
sustenta a premissa de que a escala de conforto corre sempre no sentido "menos decibéis é
melhor". Não é usada como critério numérico de conformidade.

---

## 3. Método (como o número é obtido)

### ISO 12354-1:2017 e ISO 12354-2:2017 (EN 12354)
*Building acoustics — Estimation of acoustic performance of buildings from the performance
of elements.* Partes 1 (ruído aéreo) e 2 (ruído de impacto).

Modelo de previsão de desempenho em campo a partir do desempenho dos elementos. É o que
permite sair do $R_w$ de laboratório e chegar ao $D_{nT,w}$ do ambiente real.

**Limitação assumida:** a plataforma implementa apenas a **transmissão direta**. A
transmissão por flancos (marginal) não é modelada, e o resultado declara isso entre as
limitações técnicas. Em obra real, os flancos podem reduzir o desempenho efetivo.

A ISO 12354-1 também fornece a faixa de validade usada na validação de entrada: área do
elemento até 500 m².

### ISO 16283-1 e ISO 16283-2:2020
*Acoustics — Field measurement of sound insulation in buildings and of building elements.*

Procedimento de medição em campo. Define as grandezas padronizadas $D_{nT}$ e $L'_{nT}$ e
o tempo de reverberação de referência $T_0 = 0{,}5$ s. É o caminho usado quando o usuário
informa medições próprias de $L_1$, $L_2$ ou $L_i$.

### ISO 717-1:2020 e ISO 717-2:2020
*Acoustics — Rating of sound insulation in buildings and of building elements.*

Define os números únicos ponderados $R_w$, $D_{nT,w}$, $L_{n,w}$ e $L'_{nT,w}$, e a área de
absorção de referência $A_0 = 10$ m². A banda de 500 Hz usada na lei da massa vem daqui.

### ABNT NBR ISO 10140-2 e 10140-3
*Medição em laboratório do isolamento acústico de elementos de construção.* Partes 2
(ruído aéreo) e 3 (ruído de impacto).

Norma sob a qual foram realizados os ensaios dos sistemas do catálogo. Aparece no campo
`norma_ensaio` de cada registro de dado acústico.

### ISO 3382-2:2008
*Acoustics — Measurement of room acoustic parameters — Part 2: Reverberation time in
ordinary rooms.* Procedimento de medição do tempo de reverberação $T$, que o usuário
informa no passo 2.

### ISO 12999-1:2020
*Acoustics — Determination and application of measurement uncertainties in building
acoustics.* Sustenta o tratamento de incerteza: por que a plataforma apresenta os
resultados como **estimativa de projeto** e não como laudo.

### ABNT NBR 15220-2 — Desempenho térmico de edificações: métodos de cálculo

Fonte das **densidades** ($\rho$) dos materiais do catálogo. É uma norma de desempenho
térmico, mas o Anexo B traz a tabela de propriedades físicas de materiais de construção
usada aqui apenas para massa específica — não para nada acústico.

### ABNT NBR 14715 — Chapas de gesso para drywall
Propriedades físicas das chapas de gesso acartonado.

### ABNT NBR 6118 — Projeto de estruturas de concreto
Massa específica do concreto estrutural de densidade normal.

---

## 4. Literatura científica

**GERGES, Samir N. Y.** *Ruído: fundamentos e controle.* 2. ed. Florianópolis:
NR Editora, 2000. ISBN 85-87550-02-0.
Referência de língua portuguesa para os fundamentos: lei da massa, frequência crítica,
percepção logarítmica do som e a regra prática de que ~10 dB de diferença correspondem à
sensação de metade (ou dobro) do volume — usada em
[`backend/conforto.py`](../backend/conforto.py) para traduzir decibéis em linguagem comum.
É a única referência de literatura citada pela plataforma: tudo o mais vem de norma
técnica, de documento setorial identificado ou é autoria própria declarada como tal.

> ℹ️ **Para a equipe:** autor, título, editora e ISBN estão confirmados em registros de
> catálogo de biblioteca. Confirme a **edição e o número de páginas no exemplar que vocês
> realmente consultarem** antes de submeter artigo ou relatório: há registros tanto para a
> 1ª edição (1992) quanto para a 2ª (2000), ambas pela NR Editora, em Florianópolis.
>
> As recomendações da plataforma sobre vedação de frestas e preenchimento de cavidade
> (em [`backend/suggestions.py`](../backend/suggestions.py)) **não** têm referência
> bibliográfica atribuída: são boa prática construtiva consolidada, apresentadas como
> autoria própria. Se forem usadas em texto científico, precisam de uma fonte lida e
> verificada — não de uma citação preenchida de memória.

---

## 5. Dado: catálogo de sistemas construtivos

Dez sistemas construtivos. **Nenhum deles tem, hoje, relatório de ensaio que se possa
pedir e ler** — e o catálogo passou a dizer isso em vez de esconder. As duas paredes
drywall têm fonte pública rastreável; os outros oito são valores de referência de
literatura técnica, rotulados como tal no banco, na API e na tela.

> ⚠️ **Por que esta tabela mudou — leia antes de citar qualquer coisa daqui.**
> A versão anterior atribuía cada valor a um relatório de ensaio específico (IPT
> nº 1 035 812-205, IPT nº 994 210, Ficha ALV-CER-02 da ProAcústica, Placo/IPT
> nº 1 042 115, Tarkett/IPT nº 1 028 411, Ficha FLU-01 da ProAcústica) e as duas lajes a
> tabelas de um "Anexo A" da NBR 15575-3. **Nenhuma dessas referências pôde ser localizada
> ou confirmada.** Número de relatório que ninguém acha não é fonte: é o risco de a banca
> descobrir antes de vocês. Os valores numéricos foram mantidos, porque são compatíveis
> com a ordem de grandeza da literatura da área; o que mudou foi o rótulo, que agora conta
> a verdade. Trocar um rótulo falso por um rótulo honesto enfraquece a tabela e fortalece
> o projeto.

| Código | Sistema | Desempenho | Procedência do valor |
|---|---|---|---|
| `PAR-CER-014` | Alvenaria bloco cerâmico 14 cm + argamassa 1,5 cm | $R_w$ = 40 dB | Referência de literatura — fonte a confirmar |
| `PAR-CER-019` | Alvenaria bloco cerâmico 19 cm + argamassa 1,5 cm | $R_w$ = 44 dB | Referência de literatura — fonte a confirmar |
| `PAR-CON-010` | Parede de concreto maciço 10 cm | $R_w$ = 45 dB | Referência de literatura — fonte a confirmar |
| `PAR-CON-015` | Parede de concreto maciço 15 cm | $R_w$ = 49 dB | Referência de literatura — fonte a confirmar |
| `PAR-DRY-073` | Drywall 73/48 — 1 placa ST 12,5 mm/face + lã 50 mm | $R_w$ = 43 dB | ✅ *Desempenho Acústico em Sistemas Drywall*, 3. ed., Associação Brasileira do Drywall (rev. téc. ProAcústica) — faixa publicada de **40 a 44 dB** |
| `PAR-DRY-098` | Drywall 98/48 — 2 placas ST 12,5 mm/face + lã 50 mm | $R_w$ = 51 dB | ✅ Mesmo manual — faixa publicada de **50 a 54 dB** |
| `LAJ-MAC-010` | Laje maciça 10 cm, sem atenuador | $R_w$ = 45 dB · $L_{n,w}$ = 80 dB | Referência de literatura — fonte a confirmar (atribuição ao "Anexo A" da NBR 15575-3 retirada) |
| `LAJ-MAC-014` | Laje maciça 14 cm, sem atenuador | $R_w$ = 49 dB · $L_{n,w}$ = 76 dB | Referência de literatura — fonte a confirmar (idem) |
| `LAJ-FLU-014` | Laje 14 cm + manta 5 mm + contrapiso 5 cm | $R_w$ = 52 dB · $L_{n,w}$ = 56 dB ($\Delta L_w$ = 20 dB) | Referência de literatura — fonte a confirmar |
| `LAJ-VIN-014` | Laje 14 cm + contrapiso 3 cm + vinílico 2 mm | $R_w$ = 50 dB · $L_{n,w}$ = 68 dB ($\Delta L_w$ = 8 dB) | Referência de literatura — fonte a confirmar |

Cada laje tem dois registros de dado acústico — um para ruído aéreo ($R_w$) e outro para
ruído de impacto ($L_{n,w}$) — porque são fenômenos distintos, julgados por partes
diferentes da norma.

**Sobre o $\Delta L_w$ das duas últimas lajes.** O $\Delta L_w$ é a melhoria que o
revestimento traz *sobre a laje nua*, e os três registros são coerentes entre si: laje de
14 cm nua = 76 dB; com piso flutuante, $76 - 20 = 56$ dB; com vinílico colado,
$76 - 8 = 68$ dB. Como o $L_{n,w}$ gravado **já inclui** essa melhoria, o campo
`delta_lw` é informativo e **não entra na conta** — subtraí-lo outra vez contaria o
revestimento duas vezes. Isso está anotado no código, em
[`backend/models.py`](../backend/models.py) e em [`backend/seed.py`](../backend/seed.py),
justamente para que ninguém "conserte" isso no futuro.

### Como transformar isto em fonte de verdade

Em ordem de esforço, do menor para o maior:

1. **Pedir ao fabricante** o relatório de ensaio do sistema que vocês quiserem citar
   (Knauf, Placo, Saint-Gobain, Tarkett, fabricantes de blocos). Eles costumam enviar o
   PDF do laboratório para pedido de estudante. Chegando o PDF, o registro muda de
   `referencia_literatura` para `ensaio_laboratorio` e a fonte passa a ser o número do
   relatório — que aí existe de fato.
2. **Artigos de congresso brasileiros** (ENTAC/ANTAC, SOBRAC) têm ensaios de laje maciça e
   de alvenaria com norma declarada. Valem como fonte **desde que alguém do grupo abra o
   PDF e leia** — citar pelo resumo do buscador é repetir o erro que esta seção corrigiu.
3. **Comunicações técnicas do IPT** publicadas abertamente. Atenção ao escopo: a que
   localizamos (nº 175839, de 2018) trata de **blocos de concreto**, não de bloco cerâmico
   nem de laje — citá-la para outro sistema seria usá-la fora do que ela mediu.

Tudo isso está em [`backend/seed.py`](../backend/seed.py), nos campos `fonte`,
`condicao_ensaio` e `confiabilidade` de cada registro — é o que a interface exibe no
cartão do sistema, sob o rótulo "Procedência do valor".

---

## 5.1 Dado: densidade dos materiais

Quando não existe ensaio para a composição, a estimativa pela lei da massa se apoia
**inteiramente** nestas densidades. Por isso cada uma declara não só a fonte, mas o
**tipo** de fonte: valor de norma, valor derivado de uma massa declarada, ou valor típico
a confirmar.

> ⚠️ **Auditoria de outubro de 2026 — três erros corrigidos.** A tabela anterior tinha
> valores que contrariavam a própria norma citada ou o resto do banco:
>
> 1. **Concreto armado: 2400 → 2500 kg/m³.** A NBR 6118, item 8.2.2, manda usar
>    2400 kg/m³ para concreto **simples** e 2500 kg/m³ para concreto **armado**. O
>    material é armado (laje e parede estrutural), então 2400 contrariava a norma que
>    estava citada ao lado e **subestimava a massa** — que é exatamente o que a lei da
>    massa usa para prever isolamento. As massas das variações e dos sistemas de concreto
>    foram recalculadas (ver tabela seguinte).
> 2. **Bloco cerâmico: 1200 → 780 kg/m³.** Com 1200 kg/m³, a espessura de 14 cm daria
>    168 kg/m² — 53% acima dos 110 kg/m² que a própria variação do bloco declarava. O
>    campo guarda a densidade **aparente** do bloco vazado (barro + vazios), não a do
>    barro cozido maciço, que é a faixa de 1000 a 2000 kg/m³ da NBR 15220-2.
> 3. **Placa de gesso: 800 → 760 kg/m³.** 800 kg/m³ × 12,5 mm = 10,0 kg/m², mas a chapa
>    declara 9,5 kg/m². Agora os dois campos contam a mesma história.
>
> Fontes de catálogo comercial sem edição nem data ("Catálogo Técnico Saint-Gobain",
> "Ficha Técnica Tarkett") foram substituídas por uma declaração honesta de valor típico
> a confirmar na ficha do produto que o projeto realmente especificar.

| # | Material | $\rho$ (kg/m³) | Procedência |
|---|---|---:|---|
| 1 | Bloco cerâmico de vedação | 780 | Derivada dos 110 kg/m² da variação de 14 cm (autoria própria: $110 \div 0,14$) |
| 2 | Bloco de concreto vazado | 1400 | Valor típico de densidade aparente — a confirmar na ficha do bloco |
| 3 | Argamassa de cimento e areia | 1900 | ABNT NBR 15220-2, Anexo B — faixa 1800 a 2100; adotado o centro |
| 4 | Concreto armado maciço | **2500** | ABNT NBR 6118, item 8.2.2 — concreto armado |
| 5 | Placa de gesso acartonado (drywall) | **760** | Derivada dos 9,5 kg/m² da chapa ST 12,5 mm (autoria própria) |
| 6 | Lã de vidro para isolamento acústico | 14 | Valor típico (faixa 10 a 20) — a confirmar na ficha do produto |
| 7 | Manta acústica de polietileno expandido | 30 | Valor típico (faixa 25 a 35) — a confirmar na ficha do produto |
| 8 | Contrapiso regularizado de argamassa | 2000 | ABNT NBR 15220-2, Anexo B — faixa 1800 a 2100 |
| 9 | Piso vinílico em réguas (colado) | 1300 | Valor típico de régua LVT — a confirmar na ficha do produto |
| 10 | Piso cerâmico / porcelanato | 2200 | Valor típico (faixa 2000 a 2400) — a confirmar; a faixa da NBR 15220-2 para "cerâmica" é de tijolo e telha |

A lã de vidro e a manta aparecem com densidade baixíssima de propósito: **o efeito
acústico delas não vem da massa**. A lã atua por absorção dentro da cavidade e a manta
por elasticidade (desacoplamento). Na soma da massa superficial, as duas são desprezíveis.

### Variações dimensionais

Alguns materiais têm massa superficial ($m'$) declarada diretamente para uma espessura
comercial, em vez de calculada por $\rho \times e$ — e quando há variação, é ela que o
cálculo usa. Nesses casos vale o valor tabelado, com sua própria procedência:

| Material | Variação | $e$ | $m'$ (kg/m²) | Procedência |
|---|---|---:|---:|---|
| Bloco cerâmico | 14 cm | 0,14 m | 110 | Valor típico com juntas — confirmar pesando o bloco especificado |
| Bloco cerâmico | 19 cm | 0,19 m | 145 | Valor típico com juntas — confirmar pesando o bloco especificado |
| Argamassa | 1,5 cm | 0,015 m | 28,5 | NBR 15220-2 ($1900 \times 0,015$) |
| Concreto armado | 10 cm | 0,10 m | **250** | NBR 6118, item 8.2.2 ($2500 \times 0,10$) |
| Concreto armado | 14 cm | 0,14 m | **350** | NBR 6118, item 8.2.2 ($2500 \times 0,14$) |
| Concreto armado | 15 cm | 0,15 m | **375** | NBR 6118, item 8.2.2 ($2500 \times 0,15$) |
| Placa de gesso | 12,5 mm ST | 0,0125 m | 9,5 | Massa típica da chapa ST (faixa 9 a 10) — confirmar no fabricante |
| Lã de vidro | 50 mm | 0,05 m | 0,7 | Derivada de 14 kg/m³ (autoria própria) |
| Manta acústica | 5 mm | 0,005 m | 0,15 | Derivada de 30 kg/m³ (autoria própria) |
| Contrapiso | 3 cm | 0,03 m | 60 | NBR 15220-2 ($2000 \times 0,03$) |
| Contrapiso | 5 cm | 0,05 m | 100 | NBR 15220-2 ($2000 \times 0,05$) |
| Piso vinílico | 2 mm | 0,002 m | 2,6 | Derivada de 1300 kg/m³ (autoria própria) — confirmar na ficha |

Com o concreto a 2500 kg/m³, as massas dos sistemas que o usam subiram: parede de 10 cm
240 → 250 kg/m², parede de 15 cm 360 → 375, laje de 14 cm 336 → 350, piso flutuante
436,15 → 450,15 e laje com vinílico 398,6 → 412,6 kg/m². Isso **muda resultados**: na
estimativa pela lei da massa, cada 4% de massa a mais vale cerca de 0,35 dB.

> **Sobre a NBR 15220-2:** é uma norma de *desempenho térmico*. O que se usa dela aqui é
> apenas a tabela de propriedades físicas de materiais de construção do Anexo B — massa
> específica. Nada acústico vem dessa norma. A distinção importa: densidade é propriedade
> física, desempenho acústico é ensaio.

### Onde isso aparece na plataforma

A procedência não fica só no banco de dados:

- ao montar uma composição por camadas, o painel **"De onde vêm as densidades usadas"**
  lista cada material com sua densidade e sua fonte;
- no resultado de uma **estimativa teórica**, as fontes das densidades entram na lista de
  fontes junto com o modelo, porque é sobre elas que o número se apoia;
- cada camada devolvida pela API carrega o campo `fonte_densidade`.

> ⚠️ **Para a equipe:** os números de relatório do IPT identificam ensaios reais, mas a
> plataforma não hospeda cópia deles. Antes de publicar, guarde os PDFs (ou a referência
> completa do catálogo onde foram compilados) para poder exibi-los a um avaliador que
> peça a comprovação.

---

## 6. Regra de ouro: quando a plataforma se recusa a responder

A matriz de confiabilidade, em [`backend/engine.py`](../backend/engine.py), escolhe o
caminho de cálculo nesta ordem:

| Rótulo | Origem | Quando se aplica |
|---|---|---|
| `medicao_usuario` | Medição in situ do usuário | Há $L_1$ e $L_2$, ou $L_i$, medidos |
| `informado_usuario` | Valor de $R$ digitado | O usuário conhece o índice do fabricante |
| `ensaio_laboratorio` | Catálogo com ensaio | O sistema escolhido tem ensaio documentado |
| `documentado` | Tabela normativa | O dado vem de tabela de norma (ex.: lajes da NBR 15575-3, Anexo A), não de ensaio próprio do sistema |
| `estimativa_teorica` | Lei da massa | Elemento monolítico, sem ensaio cadastrado |
| `sem_dado` | — | **Nenhum dos anteriores: o cálculo é recusado** |

A lei da massa só é aplicada a elementos que vibram como **um corpo só** — camada única,
ou várias camadas rígidas e coladas (densidade ≥ 100 kg/m³). Havendo camada resiliente
(lã mineral, manta), o conjunto é um sistema **massa-mola-massa**, cujo comportamento a
lei da massa não descreve — e a plataforma exige um valor medido em vez de estimar.

Essa recusa é deliberada e é o principal argumento científico do projeto: **um número
inventado é pior do que a ausência de número**, porque carrega autoridade que não tem.

---

## 7. Normas citadas — lista consolidada

Para copiar em pôster, artigo ou apresentação:

**Critério**
- ABNT NBR 15575-3:2013 — Edificações habitacionais — Desempenho — Sistemas de pisos
- ABNT NBR 15575-4:2013 — Edificações habitacionais — Desempenho — Vedações verticais
- ABNT NBR 10152:2017 — Acústica — Níveis de pressão sonora em ambientes internos
- ANSI/ASA S12.60-2010/Part 1 — Acoustical Performance Criteria for Schools
- WHO (2018) — Environmental Noise Guidelines for the European Region

**Método**
- ISO 12354-1:2017 / ISO 12354-2:2017 — Estimativa de desempenho a partir dos elementos
- ISO 16283-1 / ISO 16283-2:2020 — Medição de isolamento em campo
- ISO 717-1:2020 / ISO 717-2:2020 — Números únicos ponderados
- ISO 3382-2:2008 — Medição de tempo de reverberação
- ISO 12999-1:2020 — Incerteza de medição em acústica de edificações
- ABNT NBR ISO 10140-2 / 10140-3 — Medição em laboratório

**Propriedades físicas**
- ABNT NBR 15220-2 — Desempenho térmico (tabela de densidades)
- ABNT NBR 14715 — Chapas de gesso para drywall
- ABNT NBR 6118 — Projeto de estruturas de concreto

**Literatura**
- GERGES, S. N. Y. — *Ruído: fundamentos e controle* (2. ed., Florianópolis: NR Editora, 2000)

---

## 8. O que a plataforma explicitamente **não** faz

Declarar os limites é parte do rigor. A ferramenta:

- **não modela transmissão por flancos** — só transmissão direta;
- **não substitui laudo** — a conformidade com a NBR 15575 só se comprova por medição em
  campo, conforme a ISO 16283, feita por profissional habilitado;
- **não analisa por banda de frequência** — trabalha com números únicos ponderados;
- **não possui validação experimental própria** — o projeto não realizou campanha de
  medição para aferir as previsões contra a realidade. Essa é a continuação natural do
  trabalho;
- **não cobre sistemas fora do catálogo sem dado do usuário** — e diz isso, em vez de
  aproximar por semelhança.

Cada uma dessas limitações aparece na própria interface, junto do resultado.
