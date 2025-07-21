from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, to_date, datediff, current_date,
    date_format, count, avg, floor
)
from pyspark.sql.types import DoubleType


# SparkSession
spark = (SparkSession.builder
          .appName("sicredi_pipeline_csv")
          .getOrCreate())

# Função para leitura
def read_csv(name):
    return (spark.read
            .option("header", True)
            .option("delimiter", ";")
            .csv(f"input/{name}.csv")) # Caminho relativo ao working_dir /app

# Leitura dos dados brutos
df_cooperativa = read_csv("base_cooperativa")
df_associado   = read_csv("base_associado")
df_conta       = read_csv("base_conta")
df_operacao    = read_csv("base_operacao")


# Tratamento da Camada Silver – Limpeza & tipos

# Cooperativa
df_cooperativa = df_cooperativa.withColumn("cod_entidade", col("cod_entidade").cast("string"))

# Associado
df_associado = (df_associado
    .withColumn("data_nascimento", to_date("data_nascimento", "dd/MM/yyyy"))
    .withColumn("idade", (datediff(current_date(), col("data_nascimento")) / 365).cast("int"))
    .withColumn("cpf_cnpj", col("cpf_cnpj").cast("string")))

# Conta
df_conta = (df_conta
    .withColumn("data_abertura", to_date("data_abertura", "dd/MM/yyyy"))
    .withColumn("cod_conta", col("cod_conta").cast("string"))
    .filter(col("data_abertura").isNotNull()))

# Operação
df_operacao = (df_operacao
    .withColumn("data_liberacao",    to_date("data_liberacao", "dd/MM/yyyy"))
    .withColumn("data_vencimento",   to_date("data_vencimento", "dd/MM/yyyy"))
    .withColumn("data_referencia",   to_date("data_referencia", "dd/MM/yyyy"))
    .withColumn("valor_operacao",    col("valor_operacao").cast(DoubleType()))
    .withColumn("valor_atualizado", col("valor_atualizado").cast(DoubleType()))
    .withColumn("taxa_juros",        col("taxa_juros").cast(DoubleType())))


# Camada Silver – Salvar em CSV
(df_cooperativa.write.mode("overwrite").option("header", True)
 .csv("datalake/silver/dim_cooperativa")) 

(df_associado.write.mode("overwrite").option("header", True)
 .csv("datalake/silver/dim_associado")) 

(df_conta.write.mode("overwrite").option("header", True)
 .csv("datalake/silver/dim_conta")) 

(df_operacao.write.mode("overwrite").option("header", True)
 .csv("datalake/silver/fct_operacao_credito")) 


# Tratamento da Camada Gold – Análises e Agregações

# Inadimplência mensal
df_inadimplencia = (df_operacao
    .filter(col("situacao_atualizada") == "INADIMPLENTE")
    .withColumn("ano_mes", date_format("data_referencia", "yyyy-MM"))
    .groupBy("ano_mes")
    .agg(count("*").alias("qtd_inadimplente")))

(df_inadimplencia.write.mode("overwrite").option("header", True)
 .csv("datalake/gold/inadimplencia_mensal")) 

# Inadimplência por cooperativa
df_inadimplencia_coop = (df_operacao
    .filter(col("situacao_atualizada") == "INADIMPLENTE")
    .groupBy("id_cooperativa") 
    .agg(count("*").alias("qtd_inadimplente")))

(df_inadimplencia_coop.write.mode("overwrite").option("header", True)
 .csv("datalake/gold/inadimplencia_por_cooperativa")) 

# Média de idade por faixa etária (Ex: 20-29, 30-39, etc)
df_faixa_etaria = (df_associado
    .withColumn("faixa_etaria", (floor(col("idade") / 10) * 10))
    .groupBy("faixa_etaria")
    .agg(avg("idade").alias("media_idade")))

(df_faixa_etaria.write.mode("overwrite").option("header", True)
 .csv("datalake/gold/media_idade_por_faixa")) 


# Fim do Pipeline
print("Pipeline concluído com sucesso!")
# Encerrando a sessão Spark
spark.stop()