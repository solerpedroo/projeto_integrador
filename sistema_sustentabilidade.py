#definição dos valores de S e N

S = 1
s = 1
N = 0
n = 1
1
#entrada dos dados (input)

print("Início do programa")
print("========================================================================")

print("Para as perguntas sobre transporte responder com S (sim) ou N (não)")

data = input("\nQual é a data (formato dd/mm/aaaa): ")
consumo_litros = float(input("\nQuantos litros de água você consumiu hoje? (Aprox, litros) "))
consumo_kwh = float(input("\nQuantos kWh de energia elétrica você cosumiu hoje? "))
geracao_residuos = float(input("\nQuantos KG de reíduos você gerou hoje? "))
percentual_lixo = float(input("\nQual a porcentagem de resíduos reciclados no total (em %)? "))

print("========================================================================")
print("Perguntas sobre uso de transporte")

transporte_publico = input("\nVocê usou transporte público hoje? ")
bicicleta = input("\nVocê usou bicicleta hoje? ") 
caminhada = input("\nVocê caminhou hoje? ")
carro_comb_fossil = input("\nVocê usou seu carro com combustível fóssil hoje? ")
carro_eletrico = input("\nVocê usou carro elétrico hoje? ")
carona = input("\nVocê usou carona compartilhada hoje? ")

print("========================================================================")

# classificação de sustentabilidade

#lógica para água
if consumo_litros > 200: 
    print(f"\nNível de sustentabildiade de consumo de água: ")
    print(f"\tBaixa sustentabilidade")
else:
    if consumo_litros <= 150: 
        print(f"\nNível de sustentabildiade de consumo de água: ")
        print(f"\tAlta sustentabilidade")
    else:
        print(f"\nNível de sustentabildiade de consumo de água: ")
        print(f"\tModerada sustentabilidade")

#lógica para resíduos
if percentual_lixo < 20: 
    print(f"\nNível de sustentabildiade de percentual de resíduos: ")
    print(f"\tBaixa sustentabilidade")
    print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")
else:
    if percentual_lixo > 50: 
        print(f"\nNível de sustentabildiade de percentual de resíduos: ")
        print(f"\tAlta sustentabilidade")
        print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")
    else:
        print(f"\nNível de sustentabildiade de percentual de resíduos: ")
        print(f"\tModerada sustentabilidade")
        print(f"\tA quantidade de KG de resíduos de lixo foi {geracao_residuos}")

# #lógica para energia
if consumo_kwh >= 10: 
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tBaixa sustentabilidade")
elif consumo_kwh <= 5: 
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tAlta sustentabilidade")
else:
    print(f"\nNível de sustentabildiade de gasto com energia elétrica: ")
    print(f"\tModerada sustentabilidade")

#lógica para transporte
if (transporte_publico == "S" or transporte_publico == "s") or (bicicleta == "S" or bicicleta == "s") or (caminhada == "S" or caminhada == "s"):
    if (carro_comb_fossil == "S" or carro_comb_fossil == "s") or (carona == "S" or carona == "s"):
        print(f"\nNível de sustentabilidade de uso de transporte: ")
        print(f"\tModerado nível de sustentabilidade")
    else:
        print(f"\nNível de sustentabilidade de uso de transporte: ")
        print(f"\tAlto nível de sustentabilidade")
elif (carro_comb_fossil == "S" or carro_comb_fossil == "s") or (carona == "S" or carona == "s"):
    print(f"\nNível de sustentabilidade de uso de transporte: ")
    print(f"\tBaixo nível de sustentabilidade")