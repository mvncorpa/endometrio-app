import streamlit as st

# Configuração de layout da página
st.set_page_config(page_title="Laudo Endométrio", layout="wide")

# Função que gera o texto do laudo
def gerar_laudo(fase, cd56, cd16, cd163, plasmocitos, fibras_nervosas, escore_h):
    laudo = ["BIÓPSIA DE ENDOMÉTRIO:", f"ENDOMÉTRIO {fase.upper()}"]

    if cd56 is not None:
        laudo.append(f"PRESENÇA DE CÉLULAS NK CD56-POSITIVAS EM {cd56}% DAS CÉLULAS ESTROMAIS")
    if cd16 is not None:
        laudo.append(f"PRESENÇA DE CÉLULAS NK CD16-POSITIVAS EM {cd16}% DAS CÉLULAS ESTROMAIS")
    if cd163 is not None:
        laudo.append(f"PRESENÇA DE CÉLULAS CD163-POSITIVAS EM {cd163}% DAS CÉLULAS ESTROMAIS")

    if plasmocitos > 0:
        termo = "PLASMÓCITO" if plasmocitos == 1 else "PLASMÓCITOS"
        laudo.append(f"PRESENÇA DE {plasmocitos} {termo} EM 2 MILÍMETROS QUADRADOS")
    else:
        laudo.append("AUSÊNCIA DE PLASMÓCITOS")

    if fibras_nervosas != "Não constar no laudo":
        laudo.append(f"{fibras_nervosas.upper()} DE FIBRAS NERVOSAS PGP9.5 POSITIVAS NO ESTROMA")

    if escore_h is not None:
        escore_h_formatado = f"{escore_h:.1f}".replace(".", ",")
        laudo.append(f"ESCORE H = {escore_h_formatado} PARA BCL6")

    cabecalho = laudo[0]
    corpo_numerado = [f"{idx}. {linha}" for idx, linha in enumerate(laudo[1:], 1)]
    return cabecalho + "\n" + "\n".join(corpo_numerado)

# Título do app
st.title("🧬 Laudo de Endométrio")

# Organização em colunas
col1, col2 = st.columns(2)

# Coluna 1: marcadores imunohistoquímicos
with col1:
    fase = st.radio("Fase do Endométrio", ["Secretor", "Proliferativo"])

    cd56 = st.number_input("CD56 (%)", min_value=0, max_value=100, step=1, format="%d")

    cd16 = st.number_input("CD16 (%)", min_value=0, max_value=100, step=1, format="%d")

    incluir_cd163 = st.checkbox("Inserir CD163?")
    cd163 = None
    if incluir_cd163:
        cd163 = st.number_input("CD163 (%)", min_value=0, max_value=100, step=1, format="%d")

# Coluna 2: plasmócitos, fibras nervosas e escore H
with col2:
    plasmocitos = st.number_input("Plasmócitos por 2mm²", min_value=0, step=1)

    fibras_nervosas = st.selectbox(
        "Fibras nervosas PGP9.5 no estroma",
        ["Não constar no laudo", "Ausência", "Presença"]
    )

    incluir_hscore = st.checkbox("Inserir escore H para BCL6?")
    escore_h = None
    if incluir_hscore:
        escore_h = st.number_input("Escore H", min_value=0.0, max_value=300.0, step=0.1, format="%.1f")

# Botão de geração do laudo
st.markdown("---")
if st.button("✅ Gerar Laudo"):
    laudo_final = gerar_laudo(fase, cd56, cd16, cd163, plasmocitos, fibras_nervosas, escore_h)

    st.subheader("📄 Laudo Gerado")
    st.text_area("Laudo", laudo_final, height=250)

    st.download_button(
        label="💾 Baixar como .txt",
        data=laudo_final,
        file_name="laudo_endometrio.txt"
    )

    st.info("🔍 Copie o texto manualmente ou use o botão de download para salvar o laudo.")
