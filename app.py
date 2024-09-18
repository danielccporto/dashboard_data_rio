import streamlit as st
import pandas as pd
import time
import plotly.express as px

st.title("Dashboard de Turismo - Rio de Janeiro")

# Utilizando Session State para persistir dados
if "filtered_df" not in st.session_state:
    st.session_state["filtered_df"] = None

# Color Picker para personalizar cor de fundo e texto
bg_color = st.color_picker("Escolha a cor de fundo do painel", "#ffffff")
font_color = st.color_picker("Escolha a cor da fonte", "#000000")

# Definir estilo de fundo e cor da fonte no Streamlit
st.markdown(f"""
    <style>
    .reportview-container {{
        background-color: {bg_color};
        color: {font_color};
    }}
    </style>
    """, unsafe_allow_html=True)

# Função para carregar dados e utilizar cache
@st.cache_data
def load_data(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
        elif file_type in ["xls", "xlsx"]:
            # Determine the appropriate engine for the file type
            engine = 'openpyxl' if file_type == "xlsx" else 'xlrd'
            df = pd.read_excel(uploaded_file, engine=engine)
        else:
            raise ValueError("Tipo de arquivo não suportado")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        df = pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    return df

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload do arquivo de dados de turismo", type=["csv", "xls", "xlsx"])

if uploaded_file is not None:
    try:
        # Barra de progresso e spinner durante o carregamento dos dados
        with st.spinner('Carregando dados...'):
            progress_bar = st.progress(0)
            time.sleep(1)  # Simulando processamento para barra de progresso
            
            df = load_data(uploaded_file)
            progress_bar.progress(50)  # Atualizando barra de progresso
            
            st.success("Dados carregados com sucesso!")
            progress_bar.progress(100)

        if not df.empty:
            # Exibir as primeiras 5 linhas por padrão
            st.write(f"Exibindo as primeiras 5 linhas dos {len(df)} registros carregados.")
            st.dataframe(df.head())
            
            # Exibir colunas disponíveis
            st.write("Colunas disponíveis no dataset:")
            st.write(df.columns.tolist())
            
            # Seleção de colunas para visualizar
            selected_columns = st.multiselect("Selecione as colunas que deseja visualizar", df.columns.tolist(), default=df.columns.tolist())
            
            # Filtro de linhas: Radio para escolher quantas linhas exibir
            num_rows = st.radio("Selecione quantas linhas deseja visualizar", [5, 10, 20, 50, "Todas"])
            if num_rows == "Todas":
                st.session_state["filtered_df"] = df[selected_columns]
            else:
                st.session_state["filtered_df"] = df[selected_columns].head(num_rows)
            
            st.write(f"Exibindo {len(st.session_state['filtered_df'])} linhas.")

            # Tabela Interativa com verificação de tipos numéricos
            st.write("Tabela interativa:")
            try:
                # Tentar formatar apenas colunas numéricas
                styled_df = st.session_state["filtered_df"].copy()
                for col in styled_df.columns:
                    if pd.api.types.is_numeric_dtype(styled_df[col]):
                        styled_df[col] = styled_df[col].map(lambda x: f"{x:.2f}")
                st.dataframe(styled_df)
            except Exception as e:
                st.error(f"Erro ao formatar os dados: {e}")

            # Exibir Métricas Básicas
            st.write("Métricas Básicas:")
            st.metric("Número de Registros", len(st.session_state["filtered_df"]))
            for col in selected_columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    st.write(f"Média de {col}: {df[col].mean():.2f}")
                    st.write(f"Soma de {col}: {df[col].sum():.2f}")
            
            # Filtro de dados baseado em colunas (exemplo com uma coluna específica)
            if 'Ano' in df.columns:
                unique_years = df['Ano'].dropna().unique()
                selected_year = st.selectbox("Selecione o ano para filtrar os dados", unique_years)
                filtered_year_df = df[df['Ano'] == selected_year]
                st.write(f"Dados filtrados para o ano {selected_year}:")
                st.dataframe(filtered_year_df[selected_columns].head())

            # Serviço de download do CSV filtrado
            csv = st.session_state["filtered_df"].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Baixar dados filtrados em CSV",
                data=csv,
                file_name='dados_filtrados.csv',
                mime='text/csv'
            )

            # Gráficos Simples (Barras, Linhas, Pizza)
            st.write("Gráficos Simples:")
            graph_type = st.selectbox("Selecione o tipo de gráfico", ["Barras", "Linhas", "Pizza"])
            
            if graph_type == "Barras":
                bar_chart = px.bar(st.session_state["filtered_df"], x=st.session_state["filtered_df"].columns[0], y=st.session_state["filtered_df"].columns[1])
                st.plotly_chart(bar_chart)
            elif graph_type == "Linhas":
                line_chart = px.line(st.session_state["filtered_df"], x=st.session_state["filtered_df"].columns[0], y=st.session_state["filtered_df"].columns[1])
                st.plotly_chart(line_chart)
            elif graph_type == "Pizza":
                pie_chart = px.pie(st.session_state["filtered_df"], names=st.session_state["filtered_df"].columns[0], values=st.session_state["filtered_df"].columns[1])
                st.plotly_chart(pie_chart)

            # Gráficos Avançados (Histograma, Scatter Plot)
            st.write("Gráficos Avançados:")
            adv_graph_type = st.selectbox("Selecione o gráfico avançado", ["Histograma", "Scatter Plot"])
            
            if adv_graph_type == "Histograma":
                hist = px.histogram(st.session_state["filtered_df"], x=st.session_state["filtered_df"].columns[1])
                st.plotly_chart(hist)
            elif adv_graph_type == "Scatter Plot":
                scatter = px.scatter(st.session_state["filtered_df"], x=st.session_state["filtered_df"].columns[0], y=st.session_state["filtered_df"].columns[1])
                st.plotly_chart(scatter)

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.info("Por favor, faça o upload de um arquivo CSV, XLS ou XLSX.")
