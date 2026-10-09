"""Script de semeadura do catálogo confiável da Calculadora AcousticBuild.

Princípios aplicados (Fase 2 do Relatório Mestre):
1. Qualidade e confiabilidade documental > quantidade de registros.
2. Material não possui desempenho acústico (sem Rw em materiais individuais).
3. Dados acústicos pertencem aos sistemas, nunca aos materiais isolados.
4. Cada valor declara a sua procedência real, e o rótulo de confiabilidade
   acompanha essa procedência:
     - "referencia_literatura": valor de referência técnica, de faixa
       publicada ou de literatura da área. NÃO é ensaio deste sistema.
     - "ensaio_laboratorio": só para valor vindo de relatório de ensaio
       identificado, que se possa pedir e ler.
   Dos dez sistemas, somente as duas paredes drywall têm hoje fonte
   pública rastreável (manual setorial da Associação Brasileira do
   Drywall). Os outros oito são valores de referência aguardando um
   relatório de ensaio de verdade — e dizem isso na própria fonte, em vez
   de inventar um número de relatório.
"""
from database import SessionLocal, engine
from models import (
    Base,
    CamadaSistema,
    DadoAcustico,
    Material,
    SistemaConstrutivo,
    VariacaoMaterial,
)


def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Se já houver materiais cadastrados, não duplica
        if db.query(Material).count() > 0:
            print("Catálogo já existente no banco de dados. Pulando seed.")
            return

        print("Populando catálogo de materiais com propriedades físicas e procedência declarada...")

        # -------------------------------------------------------------
        # 1. MATERIAIS INDIVIDUAIS
        # -------------------------------------------------------------
        mat_bloco_cer = Material(
            nome="Bloco cerâmico de vedação",
            categoria="alvenaria",
            subcategoria="ceramico",
            # Densidade APARENTE do bloco vazado (barro + vazios), que é o que
            # interessa para massa superficial — não a do barro cozido maciço.
            # Antes havia 1200 kg/m³ aqui: multiplicado pela espessura, dava
            # 168 kg/m² no bloco de 14 cm, 53% acima dos 110 kg/m² que a própria
            # variação declara. Os vazios do bloco explicam a diferença.
            densidade=780.0,
            unidade_densidade="kg/m³",
            descricao="Bloco vazado cerâmico de furos horizontais para alvenaria de vedação. A densidade informada é a aparente do bloco, já descontados os vazios.",
            fonte="Densidade aparente derivada da massa de 110 kg/m² da variação de 14 cm (autoria própria: 110 ÷ 0,14 ≈ 780 kg/m³). O barro cozido maciço fica entre 1000 e 2000 kg/m³ pela ABNT NBR 15220-2, Anexo B — faixa que NÃO se aplica ao bloco vazado."
        )

        mat_bloco_conc = Material(
            nome="Bloco de concreto vazado",
            categoria="alvenaria",
            subcategoria="concreto",
            densidade=1400.0,
            unidade_densidade="kg/m³",
            descricao="Bloco de concreto simples vazado para alvenaria. Densidade aparente do bloco, já descontados os vazios.",
            fonte="Valor típico de densidade aparente de bloco de concreto vazado — confirmar na ficha técnica do bloco especificado. A ABNT NBR 15220-2, Anexo B, tabela o concreto maciço (2200 a 2400 kg/m³), não o bloco vazado."
        )

        mat_argamassa = Material(
            nome="Argamassa de cimento e areia",
            categoria="revestimento",
            subcategoria="argamassa",
            densidade=1900.0,
            unidade_densidade="kg/m³",
            descricao="Argamassa comum para reboco/emboço e assentamento.",
            fonte="ABNT NBR 15220-2, Anexo B — argamassa comum: faixa de 1800 a 2100 kg/m³. Adotado o valor central da faixa."
        )

        mat_concreto = Material(
            nome="Concreto armado maciço",
            categoria="concreto",
            subcategoria="estrutural",
            # 2400 kg/m³ é o valor da NBR 6118 para concreto SIMPLES; para
            # concreto ARMADO a mesma norma manda usar 2500. O material aqui é
            # armado (laje e parede estrutural), então 2400 contrariava a
            # própria norma citada e subestimava a massa — e a massa é o que a
            # lei da massa usa para prever isolamento. A NBR 15220-2 traz 2200
            # a 2400 kg/m³, mas em contexto térmico e para concreto sem
            # armadura: por isso saiu da fonte.
            densidade=2500.0,
            unidade_densidade="kg/m³",
            descricao="Concreto armado estrutural de densidade normal.",
            fonte="ABNT NBR 6118, item 8.2.2 — concreto armado: 2500 kg/m³ (concreto simples: 2400 kg/m³)."
        )

        mat_gesso = Material(
            nome="Placa de gesso acartonado (Drywall)",
            categoria="sistema_leve",
            subcategoria="gesso",
            # 800 kg/m³ × 12,5 mm = 10,0 kg/m², mas a variação da chapa declara
            # 9,5 kg/m². Ajustado para que os dois campos contem a mesma história.
            densidade=760.0,
            unidade_densidade="kg/m³",
            descricao="Placa standard (ST) para sistemas de paredes e forros leves.",
            fonte="Densidade derivada da massa de 9,5 kg/m² da chapa ST de 12,5 mm (autoria própria: 9,5 ÷ 0,0125 = 760 kg/m³). A ABNT NBR 14715-1 fixa as exigências da chapa, não um valor único de densidade."
        )

        mat_la_vidro = Material(
            nome="Lã de vidro para isolamento acústico",
            categoria="isolamento",
            subcategoria="resiliente",
            densidade=14.0,
            unidade_densidade="kg/m³",
            descricao="Painel fonoabsorvente para preenchimento de cavidade em sistemas leves.",
            fonte="Valor típico de painel de lã de vidro para cavidade (faixa usual de 10 a 20 kg/m³) — confirmar na ficha técnica do produto especificado. A lã atua por absorção, não por massa: sua parcela na massa superficial é desprezível."
        )

        mat_manta_pe = Material(
            nome="Manta acústica de polietileno expandido",
            categoria="isolamento",
            subcategoria="manta_piso",
            densidade=30.0,
            unidade_densidade="kg/m³",
            descricao="Manta resiliente para atenuação de ruído de impacto sob piso flutuante.",
            fonte="Valor típico de manta de polietileno expandido (faixa usual de 25 a 35 kg/m³) — confirmar na ficha técnica do produto especificado."
        )

        mat_contrapiso = Material(
            nome="Contrapiso regularizado de argamassa",
            categoria="contrapiso",
            subcategoria="argamassa",
            densidade=2000.0,
            unidade_densidade="kg/m³",
            descricao="Camada de regularização para recebimento de acabamento de piso.",
            fonte="ABNT NBR 15220-2, Anexo B — argamassa comum: faixa de 1800 a 2100 kg/m³. Adotado 2000 kg/m³ para contrapiso regularizado."
        )

        mat_vinilico = Material(
            nome="Piso vinílico em réguas (colado)",
            categoria="piso",
            subcategoria="vinilico",
            densidade=1300.0,
            unidade_densidade="kg/m³",
            descricao="Revestimento vinílico flexível LVT colado sobre contrapiso.",
            fonte="Valor típico de régua vinílica LVT — confirmar na ficha técnica do produto especificado."
        )

        mat_ceramica = Material(
            nome="Piso cerâmico / Porcelanato",
            categoria="piso",
            subcategoria="ceramico",
            densidade=2200.0,
            unidade_densidade="kg/m³",
            descricao="Revestimento cerâmico esmaltado assentado com argamassa colante.",
            fonte="Valor típico de placa cerâmica/porcelanato (faixa usual de 2000 a 2400 kg/m³) — confirmar na ficha técnica. A faixa da ABNT NBR 15220-2 para cerâmica (1000 a 2000 kg/m³) é de tijolo e telha, não de porcelanato prensado."
        )

        db.add_all([
            mat_bloco_cer, mat_bloco_conc, mat_argamassa, mat_concreto,
            mat_gesso, mat_la_vidro, mat_manta_pe, mat_contrapiso,
            mat_vinilico, mat_ceramica
        ])
        db.flush()

        # -------------------------------------------------------------
        # 2. VARIAÇÕES DOS MATERIAIS
        # -------------------------------------------------------------
        var_bloco_cer_14 = VariacaoMaterial(
            material_id=mat_bloco_cer.id,
            nome_variacao="14 cm",
            espessura=0.14,
            massa_superficial=110.0,
            descricao="Bloco cerâmico vedação 14x19x29 cm",
            fonte="Valor típico de alvenaria de bloco cerâmico vazado de 14 cm, com juntas de assentamento — confirmar pesando o bloco especificado (massa do bloco ÷ área da face)."
        )
        var_bloco_cer_19 = VariacaoMaterial(
            material_id=mat_bloco_cer.id,
            nome_variacao="19 cm",
            espessura=0.19,
            massa_superficial=145.0,
            descricao="Bloco cerâmico vedação 19x19x29 cm",
            fonte="Valor típico de alvenaria de bloco cerâmico vazado de 19 cm, com juntas de assentamento — confirmar pesando o bloco especificado (massa do bloco ÷ área da face)."
        )

        var_argamassa_15 = VariacaoMaterial(
            material_id=mat_argamassa.id,
            nome_variacao="1,5 cm",
            espessura=0.015,
            massa_superficial=28.5,
            descricao="Reboco padrão 15 mm",
            fonte="ABNT NBR 15220-2, Anexo B (1900 kg/m³ × 0,015 m = 28,5 kg/m²)"
        )

        var_concreto_10 = VariacaoMaterial(
            material_id=mat_concreto.id,
            nome_variacao="10 cm",
            espessura=0.10,
            massa_superficial=250.0,
            descricao="Laje ou parede de concreto maciço 10 cm",
            fonte="ABNT NBR 6118, item 8.2.2 (2500 kg/m³ × 0,10 m = 250 kg/m²)"
        )
        var_concreto_14 = VariacaoMaterial(
            material_id=mat_concreto.id,
            nome_variacao="14 cm",
            espessura=0.14,
            massa_superficial=350.0,
            descricao="Laje ou parede de concreto maciço 14 cm",
            fonte="ABNT NBR 6118, item 8.2.2 (2500 kg/m³ × 0,14 m = 350 kg/m²)"
        )
        var_concreto_15 = VariacaoMaterial(
            material_id=mat_concreto.id,
            nome_variacao="15 cm",
            espessura=0.15,
            massa_superficial=375.0,
            descricao="Parede de concreto maciço 15 cm",
            fonte="ABNT NBR 6118, item 8.2.2 (2500 kg/m³ × 0,15 m = 375 kg/m²)"
        )

        var_gesso_125 = VariacaoMaterial(
            material_id=mat_gesso.id,
            nome_variacao="12,5 mm ST",
            espessura=0.0125,
            massa_superficial=9.5,
            descricao="Chapa Standard de gesso acartonado 12,5 mm",
            fonte="Massa típica de chapa ST de 12,5 mm (faixa usual de 9 a 10 kg/m²) — confirmar na ficha técnica do fabricante especificado."
        )

        var_la_50 = VariacaoMaterial(
            material_id=mat_la_vidro.id,
            nome_variacao="50 mm",
            espessura=0.05,
            massa_superficial=0.7,
            descricao="Painel de lã de vidro espessura 50 mm",
            fonte="Massa derivada da densidade típica de 14 kg/m³ (autoria própria: 14 × 0,05 = 0,7 kg/m²). Parcela desprezível na massa do sistema."
        )

        var_manta_5 = VariacaoMaterial(
            material_id=mat_manta_pe.id,
            nome_variacao="5 mm",
            espessura=0.005,
            massa_superficial=0.15,
            descricao="Manta acústica PE expandido 5 mm",
            fonte="Massa derivada da densidade típica de 30 kg/m³ (autoria própria: 30 × 0,005 = 0,15 kg/m²). O efeito acústico da manta vem da sua elasticidade, não da massa."
        )

        var_contrapiso_3 = VariacaoMaterial(
            material_id=mat_contrapiso.id,
            nome_variacao="3 cm",
            espessura=0.03,
            massa_superficial=60.0,
            descricao="Contrapiso argamassa 3 cm",
            fonte="ABNT NBR 15220-2, Anexo B (2000 kg/m³ × 0,03 m = 60 kg/m²)"
        )
        var_contrapiso_5 = VariacaoMaterial(
            material_id=mat_contrapiso.id,
            nome_variacao="5 cm",
            espessura=0.05,
            massa_superficial=100.0,
            descricao="Contrapiso armado 5 cm para piso flutuante",
            fonte="ABNT NBR 15220-2, Anexo B (2000 kg/m³ × 0,05 m = 100 kg/m²)"
        )

        var_vinilico_2 = VariacaoMaterial(
            material_id=mat_vinilico.id,
            nome_variacao="2 mm",
            espessura=0.002,
            massa_superficial=2.6,
            descricao="Piso vinílico colado 2 mm",
            fonte="Massa derivada da densidade típica de 1300 kg/m³ (autoria própria: 1300 × 0,002 = 2,6 kg/m²) — confirmar na ficha técnica do produto."
        )

        db.add_all([
            var_bloco_cer_14, var_bloco_cer_19, var_argamassa_15,
            var_concreto_10, var_concreto_14, var_concreto_15,
            var_gesso_125, var_la_50, var_manta_5,
            var_contrapiso_3, var_contrapiso_5, var_vinilico_2
        ])
        db.flush()

        print("Cadastrando os 10 sistemas do catálogo, cada dado com a sua procedência...")

        # -------------------------------------------------------------
        # 3. SISTEMAS CONSTRUTIVOS & DADOS ACÚSTICOS
        # -------------------------------------------------------------

        # Sistema 1: PAR-CER-014
        sis_1 = SistemaConstrutivo(
            codigo="PAR-CER-014",
            nome="Alvenaria de bloco cerâmico 14 cm revestida com argamassa 1,5 cm",
            tipo_elemento="parede",
            descricao="Alvenaria de vedação convencional com bloco cerâmico 14x19x29 cm e reboco nas duas faces.",
            espessura_total=0.17,
            massa_superficial_total=167.0
        )
        db.add(sis_1)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_1.id, material_id=mat_argamassa.id, variacao_id=var_argamassa_15.id, ordem=1, espessura=0.015, posicao="revestimento_int"),
            CamadaSistema(sistema_id=sis_1.id, material_id=mat_bloco_cer.id, variacao_id=var_bloco_cer_14.id, ordem=2, espessura=0.14, posicao="nucleo"),
            CamadaSistema(sistema_id=sis_1.id, material_id=mat_argamassa.id, variacao_id=var_argamassa_15.id, ordem=3, espessura=0.015, posicao="revestimento_ext"),
            DadoAcustico(
                sistema_id=sis_1.id,
                tipo_ruido="aereo",
                rw=40.0,
                condicao_ensaio="Valor de referência para alvenaria de bloco cerâmico vazado de 14 cm revestida nas duas faces. Não é ensaio deste sistema: nenhum relatório de laboratório foi localizado para esta composição.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 2: PAR-CER-019
        sis_2 = SistemaConstrutivo(
            codigo="PAR-CER-019",
            nome="Alvenaria de bloco cerâmico 19 cm revestida com argamassa 1,5 cm",
            tipo_elemento="parede",
            descricao="Alvenaria de bloco cerâmico 19x19x29 cm com reboco em ambas as faces.",
            espessura_total=0.22,
            massa_superficial_total=202.0
        )
        db.add(sis_2)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_2.id, material_id=mat_argamassa.id, variacao_id=var_argamassa_15.id, ordem=1, espessura=0.015, posicao="revestimento_int"),
            CamadaSistema(sistema_id=sis_2.id, material_id=mat_bloco_cer.id, variacao_id=var_bloco_cer_19.id, ordem=2, espessura=0.19, posicao="nucleo"),
            CamadaSistema(sistema_id=sis_2.id, material_id=mat_argamassa.id, variacao_id=var_argamassa_15.id, ordem=3, espessura=0.015, posicao="revestimento_ext"),
            DadoAcustico(
                sistema_id=sis_2.id,
                tipo_ruido="aereo",
                rw=44.0,
                condicao_ensaio="Valor de referência para alvenaria de bloco cerâmico vazado de 19 cm revestida nas duas faces. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 3: PAR-CON-010
        sis_3 = SistemaConstrutivo(
            codigo="PAR-CON-010",
            nome="Parede de concreto maciço 10 cm",
            tipo_elemento="parede",
            descricao="Parede estrutural moldada in loco de concreto armado maciço 10 cm.",
            espessura_total=0.10,
            massa_superficial_total=250.0
        )
        db.add(sis_3)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_3.id, material_id=mat_concreto.id, variacao_id=var_concreto_10.id, ordem=1, espessura=0.10, posicao="nucleo"),
            DadoAcustico(
                sistema_id=sis_3.id,
                tipo_ruido="aereo",
                rw=45.0,
                condicao_ensaio="Valor de referência para parede de concreto armado maciço de 10 cm. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 4: PAR-CON-015
        sis_4 = SistemaConstrutivo(
            codigo="PAR-CON-015",
            nome="Parede de concreto maciço 15 cm",
            tipo_elemento="parede",
            descricao="Parede de concreto armado maciço 15 cm.",
            espessura_total=0.15,
            massa_superficial_total=375.0
        )
        db.add(sis_4)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_4.id, material_id=mat_concreto.id, variacao_id=var_concreto_15.id, ordem=1, espessura=0.15, posicao="nucleo"),
            DadoAcustico(
                sistema_id=sis_4.id,
                tipo_ruido="aereo",
                rw=49.0,
                condicao_ensaio="Valor de referência para parede de concreto armado maciço de 15 cm. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 5: PAR-DRY-073
        sis_5 = SistemaConstrutivo(
            codigo="PAR-DRY-073",
            nome="Parede Drywall 73/48 (1 placa ST 12,5 mm cada face + lã de vidro 50 mm)",
            tipo_elemento="parede",
            descricao="Sistema de vedação leve com montantes M48 e uma chapa de gesso de cada lado.",
            espessura_total=0.073,
            massa_superficial_total=19.7
        )
        db.add(sis_5)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_5.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=1, espessura=0.0125, posicao="face_int"),
            CamadaSistema(sistema_id=sis_5.id, material_id=mat_la_vidro.id, variacao_id=var_la_50.id, ordem=2, espessura=0.05, posicao="nucleo"),
            CamadaSistema(sistema_id=sis_5.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=3, espessura=0.0125, posicao="face_ext"),
            DadoAcustico(
                sistema_id=sis_5.id,
                tipo_ruido="aereo",
                rw=43.0,
                norma_ensaio="ABNT NBR ISO 10140-2 / ISO 717-1",
                condicao_ensaio="Faixa de Rw publicada em manual setorial, consolidada de ensaios de laboratório de fabricantes: 40 a 44 dB para o sistema 73/48 com uma chapa ST de 12,5 mm por face e lã de vidro de 50 mm na cavidade. Adotados 43 dB, dentro da faixa.",
                confiabilidade="referencia_literatura",
                fonte="Desempenho Acústico em Sistemas Drywall, 3. ed. Associação Brasileira do Drywall, com revisão técnica da ProAcústica — faixa de 40 a 44 dB para esta configuração."
            )
        ])

        # Sistema 6: PAR-DRY-098
        sis_6 = SistemaConstrutivo(
            codigo="PAR-DRY-098",
            nome="Parede Drywall 98/48 (2 placas ST 12,5 mm cada face + lã mineral 50 mm)",
            tipo_elemento="parede",
            descricao="Sistema de alto desempenho acústico leve com chapeamento duplo em ambas as faces.",
            espessura_total=0.098,
            massa_superficial_total=38.7
        )
        db.add(sis_6)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_6.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=1, espessura=0.0125, posicao="face_int_1"),
            CamadaSistema(sistema_id=sis_6.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=2, espessura=0.0125, posicao="face_int_2"),
            CamadaSistema(sistema_id=sis_6.id, material_id=mat_la_vidro.id, variacao_id=var_la_50.id, ordem=3, espessura=0.05, posicao="nucleo"),
            CamadaSistema(sistema_id=sis_6.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=4, espessura=0.0125, posicao="face_ext_1"),
            CamadaSistema(sistema_id=sis_6.id, material_id=mat_gesso.id, variacao_id=var_gesso_125.id, ordem=5, espessura=0.0125, posicao="face_ext_2"),
            DadoAcustico(
                sistema_id=sis_6.id,
                tipo_ruido="aereo",
                rw=51.0,
                norma_ensaio="ABNT NBR ISO 10140-2 / ISO 717-1",
                condicao_ensaio="Faixa de Rw publicada em manual setorial, consolidada de ensaios de laboratório de fabricantes: 50 a 54 dB para duas chapas ST de 12,5 mm por face com lã mineral na cavidade. Adotados 51 dB, dentro da faixa.",
                confiabilidade="referencia_literatura",
                fonte="Desempenho Acústico em Sistemas Drywall, 3. ed. Associação Brasileira do Drywall, com revisão técnica da ProAcústica — faixa de 50 a 54 dB para esta configuração."
            )
        ])

        # Sistema 7: LAJ-MAC-010
        sis_7 = SistemaConstrutivo(
            codigo="LAJ-MAC-010",
            nome="Laje maciça de concreto armado 10 cm (sem atenuador acústico)",
            tipo_elemento="piso_laje",
            descricao="Laje estrutural básica de concreto maciço 10 cm.",
            espessura_total=0.10,
            massa_superficial_total=250.0
        )
        db.add(sis_7)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_7.id, material_id=mat_concreto.id, variacao_id=var_concreto_10.id, ordem=1, espessura=0.10, posicao="nucleo"),
            DadoAcustico(
                sistema_id=sis_7.id,
                tipo_ruido="aereo",
                rw=45.0,
                condicao_ensaio="Valor de referência para laje maciça de concreto armado de 10 cm, nua. A atribuição anterior a uma tabela do Anexo A da NBR 15575-3 foi retirada: não foi possível confirmar que a norma traga essa tabela de valores.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            ),
            DadoAcustico(
                sistema_id=sis_7.id,
                tipo_ruido="impacto",
                ln_w=80.0,
                delta_lw=0.0,
                condicao_ensaio="Valor de referência para laje nua de 10 cm, sem revestimento resiliente (por isso ΔLw = 0). A atribuição anterior ao Anexo A da NBR 15575-3 foi retirada: não foi possível confirmar essa tabela.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 8: LAJ-MAC-014
        sis_8 = SistemaConstrutivo(
            codigo="LAJ-MAC-014",
            nome="Laje maciça de concreto armado 14 cm (sem atenuador acústico)",
            tipo_elemento="piso_laje",
            descricao="Laje estrutural de concreto maciço 14 cm.",
            espessura_total=0.14,
            massa_superficial_total=350.0
        )
        db.add(sis_8)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_8.id, material_id=mat_concreto.id, variacao_id=var_concreto_14.id, ordem=1, espessura=0.14, posicao="nucleo"),
            DadoAcustico(
                sistema_id=sis_8.id,
                tipo_ruido="aereo",
                rw=49.0,
                condicao_ensaio="Valor de referência para laje maciça de concreto armado de 14 cm, nua. A atribuição anterior a uma tabela do Anexo A da NBR 15575-3 foi retirada: não foi possível confirmar que a norma traga essa tabela de valores.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            ),
            DadoAcustico(
                sistema_id=sis_8.id,
                tipo_ruido="impacto",
                ln_w=76.0,
                delta_lw=0.0,
                condicao_ensaio="Valor de referência para laje nua de 14 cm, sem revestimento resiliente (por isso ΔLw = 0). É a base dos dois sistemas seguintes: 76 dB menos a melhoria do revestimento.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 9: LAJ-FLU-014
        sis_9 = SistemaConstrutivo(
            codigo="LAJ-FLU-014",
            nome="Laje maciça 14 cm com piso flutuante (manta acústica 5 mm + contrapiso 5 cm)",
            tipo_elemento="piso_laje",
            descricao="Sistema de piso flutuante de alto desempenho para isolamento de impacto e aéreo.",
            espessura_total=0.195,
            massa_superficial_total=450.15
        )
        db.add(sis_9)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_9.id, material_id=mat_concreto.id, variacao_id=var_concreto_14.id, ordem=1, espessura=0.14, posicao="base_estrutural"),
            CamadaSistema(sistema_id=sis_9.id, material_id=mat_manta_pe.id, variacao_id=var_manta_5.id, ordem=2, espessura=0.005, posicao="camada_resiliente"),
            CamadaSistema(sistema_id=sis_9.id, material_id=mat_contrapiso.id, variacao_id=var_contrapiso_5.id, ordem=3, espessura=0.05, posicao="contrapiso_flutuante"),
            DadoAcustico(
                sistema_id=sis_9.id,
                tipo_ruido="aereo",
                rw=52.0,
                condicao_ensaio="Valor de referência para laje de 14 cm com contrapiso de 5 cm desacoplado nas bordas. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            ),
            DadoAcustico(
                sistema_id=sis_9.id,
                tipo_ruido="impacto",
                ln_w=56.0,
                # ΔLw é a melhoria que o piso flutuante traz SOBRE a laje nua, e
                # o ln_w acima JÁ a inclui: laje de 14 cm nua = 76 dB; 76 - 20 = 56.
                # É informação declarada, não entra na conta — subtrair de novo
                # contaria a manta duas vezes.
                delta_lw=20.0,
                rigidez_dinamica=25.0,
                condicao_ensaio="Valor de referência para contrapiso flutuante de 5 cm sobre manta resiliente de 5 mm, com bordas desacopladas. Não é ensaio deste sistema. A rigidez dinâmica de 25 MN/m³ também é valor típico de manta de 5 mm — confirmar na ficha do produto especificado.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        # Sistema 10: LAJ-VIN-014
        sis_10 = SistemaConstrutivo(
            codigo="LAJ-VIN-014",
            nome="Laje maciça 14 cm com contrapiso 3 cm e piso vinílico colado 2 mm",
            tipo_elemento="piso_laje",
            descricao="Sistema de laje de concreto com acabamento vinílico resiliente colado.",
            espessura_total=0.172,
            massa_superficial_total=412.6
        )
        db.add(sis_10)
        db.flush()
        db.add_all([
            CamadaSistema(sistema_id=sis_10.id, material_id=mat_concreto.id, variacao_id=var_concreto_14.id, ordem=1, espessura=0.14, posicao="base_estrutural"),
            CamadaSistema(sistema_id=sis_10.id, material_id=mat_contrapiso.id, variacao_id=var_contrapiso_3.id, ordem=2, espessura=0.03, posicao="regularizacao"),
            CamadaSistema(sistema_id=sis_10.id, material_id=mat_vinilico.id, variacao_id=var_vinilico_2.id, ordem=3, espessura=0.002, posicao="revestimento"),
            DadoAcustico(
                sistema_id=sis_10.id,
                tipo_ruido="aereo",
                rw=50.0,
                condicao_ensaio="Valor de referência para laje de 14 cm com contrapiso de 3 cm e piso vinílico colado. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            ),
            DadoAcustico(
                sistema_id=sis_10.id,
                tipo_ruido="impacto",
                ln_w=68.0,
                # Mesma relação do sistema 9: laje nua 76 dB - 8 dB do vinílico
                # = 68 dB. O ΔLw já está embutido no ln_w; não subtrair outra vez.
                delta_lw=8.0,
                condicao_ensaio="Valor de referência para piso vinílico de 2 mm colado sobre contrapiso. Não é ensaio deste sistema.",
                confiabilidade="referencia_literatura",
                fonte="Valor típico de literatura técnica de acústica de edificações — fonte a confirmar. Não citar como ensaio."
            )
        ])

        db.commit()
        print("Catálogo de 10 sistemas semeado com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"Erro durante a semeadura: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
