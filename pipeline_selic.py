import requests
import pandas as pd
from sqlalchemy import create_engine

# -------------------------------------------------------------
# 1. CONFIGURAÇÃO DA CONEXÃO COM O SUPABASE (POSTGRESQL)
# -------------------------------------------------------------
# Substitua o texto entre aspas abaixo com o seu texto do Supabase + sua senha real:
DATABASE_URL = "postgresql://postgres.qvvmeggtdhtoselbzouv:JesusSalva2026@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# -------------------------------------------------------------
# 2. EXTRAÇÃO DE DADOS (API DO BANCO CENTRAL)
# -------------------------------------------------------------
def extrair_dados_selic():
    """Busca o histórico recente da Taxa SELIC acumulada no mês (código 4390 no SGS/BCB)."""
    print("Iniciando a extração de dados da API do Banco Central...")
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4390/dados?formato=json"
    
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        print(f"Extração concluída com sucesso! Total de registros baixados: {len(dados)}")
        return dados
    else:
        raise Exception(f"Erro ao acessar API do Banco Central: Status {response.status_code}")

# -------------------------------------------------------------
# 3. TRANSFORMAÇÃO DE DADOS (PANDAS)
# -------------------------------------------------------------
def transformar_dados(dados_brutos):
    """Limpa e padroniza os dados para o formato adequado do banco de dados."""
    print("Iniciando a transformação dos dados...")
    df = pd.DataFrame(dados_brutos)
    
    # Renomeia colunas para padrão SQL
    df.rename(columns={'data': 'dt_posicao', 'valor': 'vl_taxa_selic'}, inplace=True)
    
    # Converte coluna de data para o padrão do banco (YYYY-MM-DD)
    df['dt_posicao'] = pd.to_datetime(df['dt_posicao'], format='%d/%m/%Y')
    
    # Converte valor para formato numérico
    df['vl_taxa_selic'] = df['vl_taxa_selic'].astype(float)
    
    # Adiciona data/hora de ingestão
    df['dt_ingestao'] = pd.Timestamp.now()
    
    print("Transformação concluída com sucesso!")
    return df

# -------------------------------------------------------------
# 4. CARGA DE DADOS (POSTGRESQL / SUPABASE)
# -------------------------------------------------------------
def carregar_dados(df):
    """Insere o DataFrame tratado na tabela 'tb_taxa_selic' no Supabase."""
    print("Conectando ao Supabase e inserindo os dados...")
    engine = create_engine(DATABASE_URL)
    
    # Envia os dados para a tabela no Supabase
    df.to_sql('tb_taxa_selic', con=engine, if_exists='replace', index=False)
    print("Dados carregados com sucesso no banco de dados!")

# -------------------------------------------------------------
# EXECUÇÃO DO PIPELINE
# -------------------------------------------------------------
if __name__ == "__main__":
    try:
        dados_raw = extrair_dados_selic()
        df_tratado = transformar_dados(dados_raw)
        carregar_dados(df_tratado)
        print("🎉 Pipeline executado com sucesso de ponta a ponta!")
    except Exception as e:
        print(f"❌ Falha na execução do pipeline: {e}")