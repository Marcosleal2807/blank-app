import streamlit as st
import pandas as pd

# Configurações iniciais da página
st.set_page_config(page_title="Bolão Copa do Mundo 2026", layout="wide")

# -------------------------------------------------------------------------
# DATABASE SIMULADO (Em produção, substitua por Banco de Dados Real/Streamlit Secrets)
# -------------------------------------------------------------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "123", "usuario1": "senha1"}

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Palpites salvos: { usuario: { id_jogo: (gols_casa, gols_fora) } }
if "palpites" not in st.session_state:
    st.session_state.palpites = {}

# Dados reais dos jogos da 1ª rodada (Exemplo para o Grupo A)
# Modifique ou adicione os demais jogos da Copa conforme o calendário oficial
jogos_copa = [
    {"id": 1, "grupo": "Grupo A", "casa": "México", "fora": "África do Sul", "placar_casa": None, "placar_fora": None},
    {"id": 2, "grupo": "Grupo A", "casa": "Coreia do Sul", "fora": "Tchéquia", "placar_casa": None, "placar_fora": None},
]

# Resultados Oficiais Simulados (Modificado pelo Admin para calcular os pontos)
# Exemplo: O primeiro jogo aconteceu e terminou México 2 x 1 África do Sul
jogos_oficiais = {
    1: (2, 1),  # id: (gols_casa, gols_fora)
    2: None     # Ainda não aconteceu
}

# -------------------------------------------------------------------------
# LÓGICA DE PONTUAÇÃO
# -------------------------------------------------------------------------
# Vitória/Empate simples = 1 ponto | Placar Exato = 3 pontos
def calcular_pontos(palpite, oficial):
    if not palpite or not oficial:
        return 0
    g_casa_p, g_fora_p = palpite
    g_casa_o, g_fora_o = oficial
    
    # Placar exato
    if g_casa_p == g_casa_o and g_fora_p == g_fora_o:
        return 3
        
    # Acertou apenas o vencedor ou o empate (Vitória simples)
    if (g_casa_p > g_fora_p and g_casa_o > g_fora_o) or \
       (g_casa_p < g_fora_p and g_casa_o < g_fora_o) or \
       (g_casa_p == g_fora_p and g_casa_o == g_fora_o):
        return 1
        
    return 0

# -------------------------------------------------------------------------
# TELA DE LOGIN / CADASTRO
# -------------------------------------------------------------------------
def tela_login():
    st.title("🏆 Bolão Copa do Mundo 2026")
    
    aba_login, aba_cadastro = st.tabs(["🔐 Login", "📝 Cadastrar Nova Conta"])
    
    with aba_login:
        user = st.text_input("Usuário", key="login_user")
        password = st.text_input("Senha", type="password", key="login_pass")
        if st.button("Entrar", use_container_width=True):
            if user in st.session_state.users and st.session_state.users[user] == password:
                st.session_state.logged_in_user = user
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")
                
    with aba_cadastro:
        new_user = st.text_input("Escolha um Usuário", key="new_user")
        new_password = st.text_input("Escolha uma Senha", type="password", key="new_pass")
        if st.button("Cadastrar", use_container_width=True):
            if new_user in st.session_state.users:
                st.error("Este usuário já existe.")
            elif new_user == "" or new_password == "":
                st.error("Preencha todos os campos.")
            else:
                st.session_state.users[new_user] = new_password
                st.success("Cadastro realizado com sucesso! Vá para a aba de Login.")

# -------------------------------------------------------------------------
# TELA PRINCIPAL (APÓS LOGIN)
# -------------------------------------------------------------------------
def tela_principal():
    usuario_atual = st.session_state.logged_in_user
    
    # Barra Superior
    col_user, col_logout = st.columns([8, 2])
    col_user.markdown(f"👋 Bem-vindo, **{usuario_atual}**!")
    if col_logout.button("Sair da Conta", subheader=None):
        st.session_state.logged_in_user = None
        st.rerun()
        
    st.title("⚽ Dashboard do Bolão")
    st.write("---")
    
    # Abas do Menu Principal
    tab1, tab2, tab3 = st.tabs(["📊 Classificação dos Grupos", "✍️ Registrar Palpites", "🏅 Ranking Geral"])
    
    # ---------------------------------------------------------------------
    # ABA 1: Classificação dos Grupos (Conforme o Modelo Solicitado)
    # ---------------------------------------------------------------------
    with tab1:
        st.subheader("Classificação - Copa do Mundo")
        grupo_selecionado = st.selectbox("Escolha o Grupo", ["Grupo A", "Grupo B", "Grupo C", "Grupo D"])
        
        # Dados estáticos simulando a tabela enviada na imagem
        # Em um sistema real, essa tabela seria calculada dinamicamente com base nos 'jogos_oficiais'
        if grupo_selecionado == "Grupo A":
            dados_grupo = {
                "Equipe": ["🇲🇽 México", "🇿🇦 África do Sul", "🇰🇷 Coreia do Sul", "🇨🇿 Tchéquia"],
                "PJ": [0, 0, 0, 0],
                "VIT": [0, 0, 0, 0],
                "E": [0, 0, 0, 0],
                "DER": [0, 0, 0, 0],
                "SG": [0, 0, 0, 0],
                "Pts": [0, 0, 0, 0]
            }
            df = pd.DataFrame(dados_grupo)
            df.index = df.index + 1 # Começar o ranking do 1
            st.table(df)
        else:
            st.info(f"Dados do {grupo_selecionado} estarão disponíveis assim que definidos.")

    # ---------------------------------------------------------------------
    # ABA 2: Registrar Palpites
    # ---------------------------------------------------------------------
    with tab2:
        st.subheader("Preencha seus palpites para os jogos abaixo:")
        
        if usuario_atual not in st.session_state.palpites:
            st.session_state.palpites[usuario_atual] = {}
            
        with st.form("form_palpites"):
            for jogo in jogos_copa:
                st.markdown(f"#### {jogo['grupo']}")
                col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 2, 3])
                
                with col1:
                    st.write(f"**{jogo['casa']}**")
                with col2:
                    # Carrega palpite anterior se houver
                    prev_casa = st.session_state.palpites[usuario_atual].get(jogo['id'], (0,0))[0]
                    gols_c = st.number_input("", min_value=0, max_value=20, value=prev_casa, key=f"c_{jogo['id']}")
                with col3:
                    st.write("X")
                with col4:
                    prev_fora = st.session_state.palpites[usuario_atual].get(jogo['id'], (0,0))[1]
                    gols_f = st.number_input("", min_value=0, max_value=20, value=prev_fora, key=f"f_{jogo['id']}")
                with col5:
                    st.write(f"**{jogo['fora']}**")
                    
                # Salva no dicionário temporário do formulário
                st.session_state.palpites[usuario_atual][jogo['id']] = (gols_c, gols_f)
                st.write("---")
                
            botao_salvar = st.form_submit_button("Gravar Meus Palpites", use_container_width=True)
            if botao_salvar:
                st.success("Palpites gravados com sucesso!")

    # ---------------------------------------------------------------------
    # ABA 3: Ranking de Participantes
    # ---------------------------------------------------------------------
    with tab3:
        st.subheader("🏅 Classificação Geral do Bolão")
        
        ranking_dados = []
        
        # Calcula a pontuação para cada usuário cadastrado
        for user in st.session_state.users.keys():
            total_pontos = 0
            user_palpites = st.session_state.palpites.get(user, {})
            
            for jogo_id, oficial in jogos_oficiais.items():
                if oficial is not None: # Jogo já aconteceu
                    palpite = user_palpites.get(jogo_id)
                    total_pontos += calcular_pontos(palpite, oficial)
                    
            ranking_dados.append({"Participante": user, "Pontos Ganhos": total_pontos})
            
        # Ordena o ranking do maior para o menor ponto
        df_ranking = pd.DataFrame(ranking_dados).sort_values(by="Pontos Ganhos", ascending=False)
        df_ranking.index = range(1, len(df_ranking) + 1)
        
        st.dataframe(df_ranking, use_container_width=True)

# -------------------------------------------------------------------------
# CONTROLE DE FLUXO
# -------------------------------------------------------------------------
if st.session_state.logged_in_user is None:
    tela_login()
else:
    tela_principal()
