import { useEffect, useRef } from 'react';
import { IconCircleX } from './IconSet';
import styles from '../style/BioModal.module.css';

// Modal de tela cheia com a biografia completa de um integrante. O card da
// equipe mostra só o resumo; o texto inteiro vive aqui.
// Recebe `pessoa` (nome, foto, bio) e `onClose`; com `pessoa` nulo não desenha nada.
export default function BioModal({ pessoa, onClose }) {
  const fecharRef = useRef(null);

  useEffect(() => {
    if (!pessoa) return undefined;

    // Guarda quem abriu para devolver o foco quando o modal fecha.
    const quemAbriu = document.activeElement;
    const overflowAnterior = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    fecharRef.current?.focus();

    const onKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    document.addEventListener('keydown', onKeyDown);

    return () => {
      document.removeEventListener('keydown', onKeyDown);
      document.body.style.overflow = overflowAnterior;
      quemAbriu?.focus?.();
    };
  }, [pessoa, onClose]);

  if (!pessoa) return null;

  return (
    <div className={styles.overlay} role="presentation" onClick={onClose}>
      <div
        className={styles.dialog}
        role="dialog"
        aria-modal="true"
        aria-labelledby="bio-titulo"
        onClick={(e) => e.stopPropagation()}
      >
        <button
          ref={fecharRef}
          type="button"
          className={styles.close}
          onClick={onClose}
          aria-label="Fechar"
        >
          <IconCircleX size={28} color="#FFFFFF" />
        </button>

        <div className={styles.conteudo}>
          <img src={pessoa.foto} alt={pessoa.nome} className={styles.foto} />

          <div className={styles.texto}>
            <span className={styles.label}>Equipe AcousticBuild</span>
            <h2 id="bio-titulo" className={styles.nome}>{pessoa.nome}</h2>
            {pessoa.bio.map((paragrafo, i) => (
              <p key={i} className={styles.paragrafo}>{paragrafo}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
