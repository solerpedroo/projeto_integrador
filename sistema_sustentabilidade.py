#definição dos valores de S e N

S = 1
F = 0

#entrada dos dados (input)

print("Início do programa")
print("========================================================================")

print("Para as perguntas sobre transporte responder com S (sim) ou N (não)")

data = input("\nQual é a data (formato dd/mm/aaaa): ")
consumo_litros = int(input("\nQuantos litros de água você consumiu hoje? (Aprox, litros) "))
consumo_kwh = int(input("\nQuantos kWh de energia elétrica você cosumiu hoje? "))
geracao_residuos = int(input("\nQuantos KG de reíduos você gerou hoje? "))

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
if geracao_residuos < 20: 
    print(f"\nNível de sustentabildiade de geração de resíduos: ")
    print(f"\tBaixa sustentabilidade")
else:
    if geracao_residuos >= 50: 
        print(f"\nNível de sustentabildiade de geração de resíduos: ")
        print(f"\tAlta sustentabilidade")
    else:
        print(f"\nNível de sustentabildiade de geração de resíduos: ")
        print(f"\tModerada sustentabilidade")

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

# #lógica para transporte
if (transporte_publico or bicicleta or caminhada == "S") and carro_comb_fossil == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tModerado nível de sustentabilidade")
elif transporte_publico == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tAlto nível de sustentabilidade")
elif bicicleta == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tAlto nível de sustentabilidade")
elif caminhada == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tAlto nível de sustentabilidade")
elif carro_eletrico == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tAlto nível de sustentabilidade")
elif carona == "S":
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tModerado nível de sustentabilidade")
if carro_comb_fossil == "S":    
    print(f"\nNível de sustentabildiade de uso de transporte: ")
    print(f"\tBaixo nível de sustentabilidade")