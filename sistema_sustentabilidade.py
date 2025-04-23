#importação de bibliotecas
import mysql.connector
import os

#definição dos valores de S e N
S = 1 
s = 1
N = 0
n = 0

#conexão com o BD
conexao = mysql.connector.connect(
host="localhost", # IP ou hostname do servidor MySQL
user="root", # "login"
password="@Contardi19", # senha
database="ProjetoSustentabilidade" # nome do banco (tem que existir)
)
cursor = conexao.cursor()

#tela de bem-vindo

print('\n\n\t=-=-=-=-= BEM VINDO(A) AO SISTEMA PARA CONTROLE DE SUSTENTABILIDADE =-=-=-=-=\n\n')
print('O sistema calculará as informações fornecidas para você e te retornará\n')
print("Para as perguntas sobre transporte responder com S (sim) ou N (não)\n")
input('\n\t<< Tecle Enter para continuar >>')

os.system('cls' if os.name == 'nt' else 'clear')

#perguntas gerais
print("\n========================================================================\n")
print("\t=-=-=-=-= Perguntas gerais =-=-=-=-=\n\n")

data = input("\nQual é a data (formato dd/mm/aaaa): ")
consumo_litros = float(input("\n1. Quantos litros de água você consumiu hoje? (Aprox, litros) "))
consumo_kwh = float(input("\n2. Quantos kWh de energia elétrica você cosumiu hoje? "))
geracao_residuos = float(input("\n3. Quantos KG de resíduos você gerou hoje? "))
residuos_reciclaveis = float(input("\n4. Quantos KG de resíduos recicláveis você gerou hoje? "))

os.system('cls' if os.name == 'nt' else 'clear')

#perguntas meio de transporte
print("\n========================================================================\n")
print("\t=-=-=-=-= Perguntas sobre uso de transporte =-=-=-=-=\n\n")
print("\t=-=-=-=-= Responder com S (sim) ou N (não) =-=-=-=-=\n\n")

# Dicionário com os inputs
respostas_meio_transporte = {
    "transporte_publico": input("\n5. Você usou transporte público hoje? "),
    "bicicleta": input("\n6. Você usou bicicleta hoje? "), 
    "caminhada": input("\n7. Você caminhou hoje? "),
    "carro_comb_fossil": input("\n8. Você usou seu carro com combustível fóssil hoje? "),
    "carro_eletrico": input("\n9. Você usou carro elétrico hoje? "),
    "carona": input("\n10. Você usou carona compartilhada hoje? ")
}

# Atribuição das variáveis individuais para manter a lógica existente funcionando
transporte_publico = respostas_meio_transporte["transporte_publico"]
bicicleta = respostas_meio_transporte["bicicleta"]
caminhada = respostas_meio_transporte["caminhada"]
carro_comb_fossil = respostas_meio_transporte["carro_comb_fossil"]
carro_eletrico = respostas_meio_transporte["carro_eletrico"]
carona = respostas_meio_transporte["carona"]

print("========================================================================")

# insert dentro do BD

sql = "INSERT INTO ProjetoDeSustentabilidade (DataEntrada, LitrosConsumidos, KWHConsumido, KgNaoReciclaveis, PorcentagemResiduos, MeioDeTransporte) VALUES (%s, %s, %s, %s, %s, %s)"

# Monta string com os meios de transporte usados
meios_usados = []

for meio, resposta in respostas_meio_transporte.items():
    if resposta.lower() == 's':
        if meio == "transporte_publico":
            meios_usados.append("Transporte público")
        elif meio == "bicicleta":
            meios_usados.append("Bicicleta")
        elif meio == "caminhada":
            meios_usados.append("Caminhada")
        elif meio == "carro_comb_fossil":
            meios_usados.append("Carro com combustível fóssil")
        elif meio == "carro_eletrico":
            meios_usados.append("Carro elétrico")
        elif meio == "carona":
            meios_usados.append("Carona compartilhada")

# Junta os meios de transporte usados com separador "; "
meios_de_transporte_str = "; ".join(meios_usados)

# Valores finais para inserção no BD
valores = (data, consumo_litros, consumo_kwh, geracao_residuos, residuos_reciclaveis, meios_de_transporte_str)

# Executa o INSERT na tabela principal
cursor.execute(sql, valores)
conexao.commit()
print("\nDados inseridos com sucesso no banco de dados!\n")

# Captura o ID inserido
id_usuario = cursor.lastrowid

# classificação de sustentabilidade
os.system('cls' if os.name == 'nt' else 'clear')
print("\n========================================================================\n")
print("\t=-=-=-=-= Níveis de sustentabilidade =-=-=-=-=\n\n")

#lógica para água
if consumo_litros > 200: 
    print(f"\nNível de sustentabildiade de consumo de água: ")
    print(f"\tBaixa sustentabilidade")
    nivel_agua = "Baixa sustentabilidade"
else:
    if consumo_litros <= 150: 
        print(f"\nNível de sustentabildiade de consumo de água: ")
        print(f"\tAlta sustentabilidade")
        nivel_agua = "Alta sustentabilidade"
    else:
        print(f"\nNível de sustentabildiade de consumo de água: ")
        print(f"\tModerada sustentabilidade")
        nivel_agua = "Moderada sustentabilidade"

#lógica para resíduos
percentual_lixo = (residuos_reciclaveis /geracao_residuos) *100

if percentual_lixo < 20: 
    print(f"\nNível de sustentabildiade de percentual de resíduos: ")
    print(f"\tBaixa sustentabilidade")
    print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")
    print(f"\tO percentual de lixo reciclável gerado foi de {percentual_lixo}%")
    nivel_residuos = "Baixa sustentabilidade"
else:
    if percentual_lixo > 50: 
        print(f"\nNível de sustentabildiade de percentual de resíduos: ")
        print(f"\tAlta sustentabilidade")
        print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")
        print(f"\tO percentual de lixo reciclável gerado foi de {percentual_lixo}%")
        nivel_residuos = "Alta sustentabilidade"
    else:
        print(f"\nNível de sustentabildiade de percentual de resíduos: ")
        print(f"\tModerada sustentabilidade")
        print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")
        print(f"\tO percentual de lixo reciclável gerado foi de {percentual_lixo}%")
        nivel_residuos = "Moderada sustentabilidade"

# #lógica para energia
if consumo_kwh >= 10: 
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tBaixa sustentabilidade")
    nivel_energia = "Baixa sustentabilidade"
elif consumo_kwh <= 5: 
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tAlta sustentabilidade")
    nivel_energia = "Alta sustentabilidade"
else:
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tModerada sustentabilidade")
    nivel_energia = "Moderada sustentabilidade"

#lógica para transporte
print(f"\nNível de sustentabilidade de uso de transporte: ")

if (transporte_publico.lower() == "s" or bicicleta.lower() == "s" or caminhada.lower() == "s"):
    if (carro_comb_fossil.lower() == "s" or carona.lower() == "s"):
        nivel_transporte = "Moderada sustentabilidade"
    else:
        nivel_transporte = "Alta sustentabilidade"
elif (carro_comb_fossil.lower() == "s" or carona.lower() == "s"):
    nivel_transporte = "Baixa sustentabilidade"
else:
    nivel_transporte = "Sem dados suficientes"

print(f"\t{nivel_transporte}")

# Agora inserimos na tabela Manipulacao_Dados
sql_insert_niveis = """
INSERT INTO Manipulacao_Dados (ID_Usuario, Nivel_LitrosConsumidos, Nivel_KWHConsumido, Nivel_KgNaoReciclaveis, Nivel_MeioDeTransporte)
VALUES (%s, %s, %s, %s, %s)
"""

valores_niveis = (id_usuario, nivel_agua, nivel_energia, nivel_residuos, nivel_transporte)
cursor.execute(sql_insert_niveis, valores_niveis)
conexao.commit()

print("\nNíveis de sustentabilidade inseridos com sucesso na tabela Manipulacao_Dados!\n")

# Finaliza a conexão
cursor.close()
conexao.close()