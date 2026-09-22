import { Link } from 'react-router-dom';
import { IconWaveform, IconSpeakerWave, IconBriefcase, IconChartBars } from './IconSet';
import Reveal from './Reveal';
import stylesProduct from '../style/ProductSection.module.css';
import styles from '../style/WhatWeAreSection.module.css';



export default function ProductSection() {
  return (
    <section className={stylesProduct.section}>
      <Reveal>
        <span className={stylesProduct.label}>Produto</span>
        <h2 className={styles.title}>
          Ferramentas completas para engenharia <span className={styles.highlight}>acústica</span>.
        </h2>
        <p className={styles.description}>
            Confira nossa calculadora em ação, que inclui: Análise do isolamento acústico entre ambientes; avaliação de materiais
            e desempenho acústico; cálculo de previsão de ruído de impacto e aéreo; geração automática de relatórios e análise acústica no planejamento de sistemas  construtivos
          </p>
      </Reveal>

    
    </section>
  );
}
