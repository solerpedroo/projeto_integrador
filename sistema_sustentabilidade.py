#entrada dos dados

data = input("Qual é a data (formato dd/mm/aaaa): ")
consumo_litros = int(input("Quantos litros de água você consumiu hoje? (Aprox, litros) "))
consumo_kwh = int(input("Quantos kWh de energia elétrica você cosumiu hoje? "))
geracao_residuos = int(input("Quantos KG de reíduos você gerou hoje? "))
transporte_publico = input("Você usou transporte público hoje? ")
bicicleta = input("Você usou bicicleta hoje? ") 
caminhada = input("Você caminhou hoje? ")
carro_comb_fossil = input("Você usou carro com combustível fóssil hoje? ")
carro_eletrico = input("Você usou carro elétrico hoje? ")
carona = input("Você usou carona compartilhada hoje? ")

# classificação de sustentabilidade

if consumo_litros > 200: 
    print(f"Baixa sustentabilidade")
else:
    if consumo_litros <= 150: 
        print(f"Alta sustentabilidade")
    else:
        print(f"Moderada sustentabilidade")


if geracao_residuos < 20: 
    print(f"Baixa sustentabilidade")
else:
    if geracao_residuos >= 50: 
        print(f"Alta sustentabilidade")
    else:
        print(f"Moderada sustentabilidade")

if consumo_kwh >= 10: 
    print(f"Baixa sustentabilidade")
elif consumo_kwh <= 5: 
        print(f"Alta sustentabilidade")
else:
        print(f"Moderada sustentabilidade")