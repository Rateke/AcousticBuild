import { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import Footer from '../components/Footer';
import BioModal from '../components/BioModal';
import Reveal from '../components/Reveal';
import cidadeWireframe from '../assets/bg-sobre.jpg';
import grupo2026 from '../assets/team/grupo-2026.jpg';
import grupo2025 from '../assets/team/grupo-2025.jpg';
import fotoFernando from '../assets/team/fernando-rateke.jpg';
import fotoMaria from '../assets/team/maria-eduarda.jpg';
import fotoJulia from '../assets/team/julia-verissimo.jpg';
import fotoSara from '../assets/team/sara-rotenski.jpg';
import fotoJoao from '../assets/team/joao-hartmann.jpg';
import styles from '../style/About.module.css';



const FERNANDO = {
  nome: 'Fernando Rateke Neto',
  foto: fotoFernando,
  resumo: 'Estudante de Desenvolvimento de Sistemas na Escola SESI e integrante da Iniciação Científica de Matemática. Finalista do Infomatrix 2025 e da FEBRACE 2026.',
  bio: [
    'Fernando Rateke Neto nasceu em Florianópolis em 2008 e atualmente é estudante do 3º ano do Ensino Médio integrado ao curso técnico em Desenvolvimento de Sistemas na Escola SESI. Pretende se candidatar a universidades nos Estados Unidos para cursar uma graduação na área de tecnologia e seguir carreira em programação, com interesse no desenvolvimento full-stack e na área de jogos.',
    'O estudante faz parte do grupo de Iniciação Científica de Matemática de sua escola desde 2025. Foi finalista do Infomatrix 2025 com o AcousticBuild, sendo credenciado para o MILSET 2026, em Fortaleza, Ceará. Em 2026, também participou da FEBRACE, ampliando sua experiência em pesquisa científica e desenvolvimento tecnológico.',
  ],
};

const MARIA = {
  nome: 'Maria Eduarda Tessari',
  foto: fotoMaria,
  resumo: 'Estudante de Desenvolvimento de Sistemas na Escola SESI, com interesse em unir tecnologia e matemática à saúde. Finalista do Infomatrix 2025, FEBRACE e FEBIC 2026.',
  bio: [
    'Maria Eduarda Tessari nasceu em Florianópolis em 2008 e atualmente é estudante do 3º ano do Ensino Médio integrado ao curso técnico em Desenvolvimento de Sistemas na Escola SESI. Pretende ingressar em uma universidade para cursar Medicina, construindo uma carreira que integre tecnologia e matemática à área da saúde.',
    'A estudante faz parte do grupo de Iniciação Científica de Matemática de sua escola desde 2025 e foi finalista do Infomatrix 2025 com o AcousticBuild, sendo credenciada para o MILSET 2026, em Fortaleza, Ceará. Em 2026, também participou da FEBRACE, ampliando sua experiência em pesquisa científica e desenvolvimento tecnológico.',
  ],
};

const JULIA = {
  nome: 'Júlia Veríssimo',
  foto: fotoJulia,
  resumo: 'Estudante de Desenvolvimento de Sistemas na Escola SESI, com objetivo de cursar Medicina. Integrante da Iniciação Científica de Matemática.',
  bio: [
    'Júlia Veríssimo nasceu em Florianópolis em 2009, atualmente é estudante do 3º ano do Ensino Médio integrado ao curso técnico em Desenvolvimento de Sistemas na Escola SESI. Pretende ingressar na Universidade Federal de Santa Catarina no curso de Medicina e construir uma carreira na área de Pediatria, com o objetivo de atuar na promoção da saúde e no cuidado de crianças e adolescentes.',
    'A estudante faz parte do grupo de Iniciação Científica de Matemática de sua escola desde 2026.',
  ],
};

const SARA = {
  nome: 'Sara Rotenski Pereira',
  foto: fotoSara,
  resumo: 'Acadêmica de Ciência de Dados e Inteligência Artificial no UniSENAI. Finalista da FEBRACE 2026 e medalha de ouro na Copa Science 2025, no México.',
  bio: [
    'Sara Rotenski Pereira nasceu em Florianópolis em 2007. Em 2025, se formou no Ensino Médio integrado ao curso técnico em Desenvolvimento de Sistemas na Escola SESI e, atualmente, é acadêmica do bacharelado em Ciência de Dados e Inteligência Artificial no UniSENAI.',
    'A estudante fez parte do grupo de Iniciação Científica de Matemática de sua escola de 2023 até 2025 e foi finalista da FEBRACE 2025 graças ao projeto “Desenvolvimento de uma Plataforma Integrada para Análise dos Níveis de Ruído Rodoviário”, que desenvolveu em 2024. Esse mesmo projeto também foi finalista da FENIC 2024, em Salvador e da FEBIC 2024, onde recebeu o prêmio de banner destaque (exposição) da feira e o credenciamento para a Copa Science 2025 no México. Nesse evento, o projeto foi premiado com medalha de ouro na categoria das Ciências Exatas e recebeu mais uma credencial, desta vez para a Colômbia.',
    'O AcousticBuild foi finalista do Infomatrix 2025 e credenciado para o evento MILSET 2026 em Fortaleza, capital do Ceará. Também foi finalista da FEBRACE 2026, em São Paulo. Além disso, Sara possui uma menção honrosa na OBMEP (Olimpíada Brasileira de Matemática) em 2022.',
  ],
};

const JOAO = {
  nome: 'João Victor Prange Hartmann',
  foto: fotoJoao,
  resumo: 'Estudante de Análise e Desenvolvimento de Sistemas na Escola SESI. Atuou na programação, manutenção e documentação da plataforma.',
  bio: [
    'João Victor Prange Hartmann nasceu em Florianópolis em 2008. Atualmente está no 3º ano do Ensino Médio integrado ao curso técnico em Análise e Desenvolvimento de Sistemas na Escola SESI.',
    'O integrante foi crucial para o desenvolvimento do projeto, pois auxiliou na parte da programação e manutenção da plataforma, além de auxiliar na área da documentação do projeto de forma eficaz.',
    'O estudante pretende entrar em uma universidade para cursar dentro da área da tecnologia. Possui experiência com diversos projetos acadêmicos envolvendo programação que incluem desde sites com o objetivo de promover o foco e cuidar da saúde mental até o projeto descrito nessa plataforma.',
  ],
};

const EQUIPES = [
  {
    ano: '2026',
    atual: true,
    descricao: 'Equipe responsável pelo desenvolvimento e evolução da plataforma',
    capa: grupo2026,
    legenda: 'Fernando Rateke Neto, Maria Eduarda Tessari e Júlia Veríssimo',
    integrantes: [FERNANDO, MARIA, JULIA],
  },
  {
    ano: '2025',
    atual: false,
    descricao: 'Equipe que deu origem ao projeto e o levou à final do Infomatrix 2025 e à final da FEBRACE.',
    capa: grupo2025,
    legenda: 'Maria Eduarda Tessari, Sara Rotenski Pereira e Fernando Rateke Neto',
    integrantes: [FERNANDO, MARIA, SARA],
  },
];

const FONT_GROUPS = [
  {
    title: 'Diretrizes internacionais',
    items: [
      { ref: 'WHO, 2018', desc: 'Environmental Noise Guidelines for the European Region.' },
    ],
  },
  {
    title: 'Literatura científica',
    items: [
      { ref: 'GERGES, S. N. Y.', desc: 'Ruído: fundamentos e controle.' },
      { ref: 'TROCHIDIS & PAPANIKOLAOU, 1984', desc: 'Transmissão sonora por frestas e aberturas.' },
      { ref: 'ASAKURA et al., 2009', desc: 'Transmissão por aberturas tipo fresta e redução por materiais porosos.' },
    ],
  },
  {
    title: 'Normas técnicas',
    items: [
      { ref: 'ABNT NBR 10152:2017 (corrigida 2020)', desc: 'Níveis de pressão sonora em ambientes internos.' },
      { ref: 'ABNT NBR 15575 — Partes 3 e 4', desc: 'Desempenho acústico de edificações habitacionais.' },
      { ref: 'ISO 12354-1:2017', desc: 'Estimativa de isolamento de ruído aéreo.' },
      { ref: 'ISO 12354-2:2017', desc: 'Estimativa de isolamento de ruído de impacto.' },
      { ref: 'ISO 16283-1', desc: 'Medição de isolamento aéreo em campo.' },
      { ref: 'ISO 16283-2:2020', desc: 'Medição de isolamento de impacto em campo.' },
      { ref: 'ISO 717-1:2020', desc: 'Classificação e ponderação de isolamento aéreo.' },
      { ref: 'ISO 717-2:2020', desc: 'Classificação e ponderação de isolamento de impacto.' },
      { ref: 'ISO 3382-2:2008', desc: 'Medição de tempo de reverberação.' },
      { ref: 'ISO 12999-1:2020', desc: 'Incerteza de medição em acústica de edificações.' },
      { ref: 'ANSI/ASA S12.60-2010/Part 1', desc: 'Critérios acústicos para escolas.' },
    ],
  },
];

export default function About() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  // Pessoa com a biografia aberta no modal (null = modal fechado).
  const [bioAberta, setBioAberta] = useState(null);

  return (
    <div className={styles.page}>
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <Header onMenuClick={() => setSidebarOpen(true)} />

      <section className={styles.hero}>
        <img src={cidadeWireframe} alt="" aria-hidden="true" className={styles.heroArt} />
        <div className={styles.heroInner}>
          <h1 className={styles.heroTitle}>
            Saiba mais sobre <span className={styles.highlight}>nós</span>
          </h1>
          <p className={styles.heroText}>
            A AcousticBuild nasceu da união entre tecnologia, engenharia e propósito: transformar a
            forma como o desempenho acústico é pensado nas edificações.
          </p>
        </div>
      </section>

      <section className={styles.equipe}>
        <Reveal className={styles.bloco}>
          <span className={styles.label}>Equipe</span>
          <h2 className={styles.sectionTitle}>Quem constrói o AcousticBuild:</h2>
        </Reveal>

        {EQUIPES.map((equipe, ei) => (
          <div key={equipe.ano} className={styles.anoBloco}>
            <Reveal>
              <div className={styles.anoHeader}>
                <div className={styles.anoTituloLinha}>
                  <span className={styles.anoNumero}>{equipe.ano}</span>
                  {equipe.atual && <span className={styles.anoBadge}>Equipe atual</span>}
                </div>
                <p className={styles.anoDesc}>{equipe.descricao}</p>
              </div>
            </Reveal>

            <Reveal>
              <figure className={styles.capa}>
                <img src={equipe.capa} alt={`Equipe de ${equipe.ano}`} loading="lazy" />
                <figcaption>{equipe.legenda}</figcaption>
              </figure>
            </Reveal>

            <div className={styles.integrantesGrid}>
              {equipe.integrantes.map((pessoa, index) => {
                // Quem participou dos dois anos já teve a biografia lida acima —
                // repetir os mesmos dois parágrafos cansa quem está lendo a página.
                const jaApresentado = EQUIPES.slice(0, ei)
                  .some((e) => e.integrantes.includes(pessoa));
                return (
                  <Reveal key={`${equipe.ano}-${pessoa.nome}`} delay={index * 80}>
                    <article className={styles.pessoaCard}>
                      <img src={pessoa.foto} alt={pessoa.nome} className={styles.pessoaFoto} loading="lazy" />
                      <h3 className={styles.pessoaNome}>{pessoa.nome}</h3>
                      {jaApresentado && (
                        <p className={styles.pessoaRepetido}>
                          Também integra a equipe atual — biografia na seção de 2026.
                        </p>
                      )}
                      {/* O card mostra só o resumo: o texto completo abre no modal. */}
                      <p className={styles.pessoaResumo}>{pessoa.resumo}</p>
                      <button
                        type="button"
                        className={styles.pessoaToggle}
                        onClick={() => setBioAberta(pessoa)}
                      >
                        Saiba mais →
                      </button>
                    </article>
                  </Reveal>
                );
              })}
            </div>
          </div>
        ))}

        {/* O João colaborou com o projeto mas não está nas fotos das equipes de
            2026 e 2025 — por isso ganha um bloco próprio, abaixo dos anos. */}
        <div className={styles.colabBloco}>
          <Reveal>
            <span className={styles.label}>Colaboração</span>
            <h3 className={styles.colabTitulo}>Também construiu o AcousticBuild</h3>
          </Reveal>

          <Reveal delay={80}>
            <article className={`${styles.pessoaCard} ${styles.colabCard}`}>
              <img src={JOAO.foto} alt={JOAO.nome} className={styles.colabFoto} loading="lazy" />
              <div className={styles.colabTexto}>
                <h3 className={styles.pessoaNome}>{JOAO.nome}</h3>
                <p className={styles.pessoaResumo}>{JOAO.resumo}</p>
                <button
                  type="button"
                  className={styles.pessoaToggle}
                  onClick={() => setBioAberta(JOAO)}
                >
                  Saiba mais →
                </button>
              </div>
            </article>
          </Reveal>
        </div>
      </section>

      <section id="metodologia" className={styles.fontes}>
        <Reveal className={styles.bloco}>
          <span className={styles.label}>Metodologia</span>
          <h2 className={styles.sectionTitle}>Em que os cálculos se baseiam</h2>
          <p>
            Cada cálculo da plataforma é fundamentado em diretrizes internacionais, literatura
            científica e normas técnicas reconhecidas. Abaixo estão as principais referências usadas
            no motor de cálculo e nos critérios normativos de classificação.
          </p>
        </Reveal>

        <div className={styles.fontesGrid}>
          {FONT_GROUPS.map((group, gi) => (
            <Reveal key={group.title} delay={gi * 100}>
              <div className={styles.fonteGrupo}>
                <h3 className={styles.fonteGrupoTitulo}>{group.title}</h3>
                <ul className={styles.fonteLista}>
                  {group.items.map((item) => (
                    <li key={item.ref}>
                      <strong>{item.ref}</strong>
                      <span>{item.desc}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </Reveal>
          ))}
        </div>
      </section>

      <Footer />

      <BioModal pessoa={bioAberta} onClose={() => setBioAberta(null)} />
    </div>
  );
}
