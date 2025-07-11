#importação de bibliotecas
import mysql.connector
# Importando uma função que multiplica matrizes e outra que as transp da biblioteca mumpy -> usadas nas funções de cripto e descriptografia
from numpy import matmul, transpose
import numpy as np
#importar biblioteca para limpar o terminal 
import os

# Declaração da tabela do alfabeto
T = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

#chave usada para a criptografia
chave = [[4,3],[1,2]]

#declarando a função de criptografia usada no código
def criptografia_palavras(chave, nome):

    # deixa a palavra recebida em maiuculo e remove os espaços, padronizando a entrada
    nome = nome.upper().replace(' ', '')

    # Vetor de indexação
    I = []

    # converte as letras da palavra em números de acordo com a posição do vetor T (alfabeto)
    for i in range (len(nome)):
        #obtém a posição do vetor T que corresponde a letra atual do loop do for
        pos = T.index(nome[i])
        if pos == '25':
            # atribui 0 se a letra for 'Z' (pos25)
            I.append(0)
        else:
            #atribui o valor + 1 ==> vetor começa com 0 e cifra de hill com 1
            I.append(pos+1)   

    # Caso a palavra tenha um tamanho ímpar, repete a última letra 
    if len(nome)%2 != 0:
        #pega a ultima letra da palavra
        pos = T.index(nome[-1])
        if pos == '25':
            I.append(0)
        else:
            I.append(pos+1)

    # Declarando a matriz de texto comum
    P = [[],[]]

    # converte o vetor de indexação em uma matriz 2xn
    for i in range(len(I)):
        if i%2 == 0:
            #atribui as letras de posição par na linha superior da matriz P
            P[0].append(I[i])
        else:
            #atribui as letras de posição impar na linha inferior da matriz P
            P[1].append(I[i])

    # Obtendo a matriz de texto cifrado pela multiplicação da chave pela matriz de texto comum P
    C = matmul(chave, P)

    # Convertendo os valores para os números existentes no conjunto alfabeto
    for i in range(len(C)):
        for j in range(len(C[0])):
            C[i][j] %= 26
            if C[i][j] == 0:
                C[i][j] = 26

    # vetor que armazenará as letras cifradas
    TC = []

    # Convertendo os números em letras
    for i in range(len(C)):
        for j in range(len(C[0])):
            #obtém a letra a partir do número convertido -1, no caso que representa o índice da letra no alfabeto (T)
            TC.append(T[C[i][j]-1])

    # Declarando a matriz a ser usada na exibição
    cripto = [[],[]]

    # Ajuste das posições das letras na matriz
    for i in range(int(len(TC)/2)):
        #atribui a primeira linha uma parte do texto ==> ex: carros = linha 0: car, linha 1: ros
        cripto[0].append(TC[i])
        #atribui a segunda linha a outra parte do texto
        cripto[1].append(TC[int(len(TC)/2)+i])

    # Transpondo a matriz para facilitar a exibição
    cripto = transpose(cripto)

    # Obtendo o texto criptografado
    texto_cripto = ''
    for i in range(len(cripto)):
        for j in range(len(cripto[0])):
            texto_cripto += cripto[i][j]

    # Retornando o texto criptografado
    return texto_cripto

#declaração da matriz de descriptografia usada no código
def descriptografia_palavras(chave, nome_cifrado):
    # Tabela que armazena os determinantes que possuem inverso no conjunto Z26 e seus respectivos inversos.
    # Exemplo: O número 3 tem como inverso o número 9 no conjunto módulo 26.
    TABELA = [[1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25],  # determinantes possíveis
              [1, 9, 21, 15, 3, 19, 7, 23, 11, 5, 17, 25]]  # inversos correspondentes

    # Vetor auxiliar que associa cada letra do alfabeto a uma posição (A=0, B=1, ..., Z=25)
    T = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    # Calculando o determinante da matriz de chave
    det = chave[0][0] * chave[1][1] - chave[0][1] * chave[1][0]

    # Ajustando o determinante para o módulo 26 (Z26)
    det = det % 26

    # Tentando encontrar o inverso do determinante na tabela
    try:
        indice_inverso = TABELA[0].index(det)
    except ValueError:
        # Se o determinante não tiver inverso, não é possível descriptografar
        raise ValueError("Determinante não tem inverso módulo 26")

    # Obtém o inverso do determinante a partir da tabela
    inverso = TABELA[1][indice_inverso]

    # Calcula a matriz inversa no conjunto Z26
    matriz_inversa = [
        [(chave[1][1] * inverso) % 26, (-chave[0][1] * inverso) % 26],
        [(-chave[1][0] * inverso) % 26, (chave[0][0] * inverso) % 26]
    ]

    # Padroniza a palavra cifrada: transforma em maiúsculas e remove espaços
    nome_cifrado = nome_cifrado.upper().replace(' ', '')

    # Cria um vetor para armazenar as posições numéricas das letras cifradas
    V = []

    # Converte cada letra para o seu valor numérico (A=1, B=2, ..., Z=26)
    for letra in nome_cifrado:
        pos = T.index(letra)  # Encontra a posição da letra no vetor T
        V.append(pos + 1)     # Soma 1 para o sistema começar em A=1

    # Cria a matriz P, que separa os números em duas linhas de forma alternada
    P = [[], []]
    for i in range(len(V)):
        P[i % 2].append(V[i])  # Alterna entre as linhas 0 e 1

    # Se houver um elemento a mais na primeira linha, adiciona um zero na segunda para equilibrar a matriz
    if len(P[0]) > len(P[1]):
        P[1].append(0)

    # Cria a matriz M que armazenará o resultado da multiplicação da matriz inversa pela matriz P
    M = [[], []]
    for j in range(len(P[0])):
        # Calcula manualmente o produto das matrizes e aplica módulo 26
        M[0].append((matriz_inversa[0][0] * P[0][j] + matriz_inversa[0][1] * P[1][j]) % 26)
        M[1].append((matriz_inversa[1][0] * P[0][j] + matriz_inversa[1][1] * P[1][j]) % 26)

    # Substitui valores zero por 26 para garantir que a letra Z seja corretamente mapeada
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j] == 0:
                M[i][j] = 26

    # Converte os números da matriz M de volta para letras
    texto_descripto = ''
    for j in range(len(M[0])):
        for i in range(len(M)):
            texto_descripto += T[M[i][j] - 1]  # Subtrai 1 pois o vetor T começa em zero

    # Remove padding: se a última letra for repetida, provavelmente foi adicionada para completar a matriz
    if len(texto_descripto) > 1 and texto_descripto[-1] == texto_descripto[-2]:
        texto_descripto = texto_descripto[:-1]

    # Caso o texto descriptografado corresponda a uma das mensagens esperadas, adiciona o espaço correto
    if texto_descripto == 'BAIXASUSTENTABILIDADE':
        texto_descripto = 'BAIXA SUSTENTABILIDADE'
    elif texto_descripto == 'MODERADASUSTENTABILIDADE':
        texto_descripto = 'MODERADA SUSTENTABILIDADE'
    elif texto_descripto == 'ALTASUSTENTABILIDADE':
        texto_descripto = 'ALTA SUSTENTABILIDADE'

    # Retorna o texto final descriptografado
    return texto_descripto

#definição dos valores de S e N
S = 1 
s = 1
N = 0
n = 0

opcao = ""

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

# Loop de menu enquanto a opção for diferente de "6"
while opcao != "6":
    print("\n--- MENU ---\n")
    print("\t1. Inserir registros")
    print("\t2. Alterar registros")
    print("\t3. Apagar registros")
    print("\t4. Listar registros")
    print("\t5. Listar médias")
    print("\t6. Sair")

    # Solicita a opção do usuário
    opcao = input("\n\tEscolha uma opção: ")
    os.system('cls' if os.name == 'nt' else 'clear')

    #opção de inserir os dados
    if opcao == "1":

        #perguntas gerais
        print("\n========================================================================\n")
        print("\t=-=-=-=-= Inserir novo registro =-=-=-=-=\n\n")
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
        # os.system('cls' if os.name == 'nt' else 'clear')
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

        valores_niveis = (id_usuario, 
                          criptografia_palavras(chave, nivel_agua), 
                          criptografia_palavras(chave, nivel_energia), 
                          criptografia_palavras(chave, nivel_residuos), 
                          criptografia_palavras(chave, nivel_transporte))
        
        cursor.execute(sql_insert_niveis, valores_niveis)
        conexao.commit()

        print("\nNíveis de sustentabilidade inseridos com sucesso na tabela Manipulacao_Dados!\n")

    #opção de alterar dados
    elif opcao == "2":
        print("\n=-=-=-=-= Alterar registros =-=-=-=-=\n")
        
        # Mostrar todos os registros
        cursor.execute("SELECT * FROM ProjetoDeSustentabilidade")
        resultado = cursor.fetchall()

        print('\n\033[1m=-=-=-=-= Registros disponíveis: =-=-=-=-=\033[0m\n')
        print('='*143)
        print(f'\033[1m{"| ID ":^5}', end='|')
        print(f'{"Data de registro":^20}', end='|')
        print(f'{"Consumo de água (L)":^20}', end='|')
        print(f'{"Consumo de energia (kWh)":^25}', end='|')
        print(f'{"Lixo não reciclável (Kg)":^25}', end='|')
        print(f'{"% Resíduos recicláveis":^25}', end='|')
        print(f'{"Meio de transporte":^50}', end='|\033[0m\n')
        print('='*143)

        for linha in resultado:
            print(f'{linha[0]:^5}', end='|')
            print(f'{linha[1]:^20}', end='|')
            print(f'{str(linha[2]) + " L":^20}', end='|')
            print(f'{str(linha[3]) + " kWh":^25}', end='|')
            print(f'{str(linha[4]) + " Kg":^25}', end='|')
            print(f'{str(linha[5]) + " %":^25}', end='|')
            print(f'{linha[6]:^20}', end='|\n')
            print('-'*143)
        
        # Selecionar ID para alteração
        id_alterar = input("\nDigite o ID do registro que deseja alterar: ")
        
        # Verificar se o ID existe
        cursor.execute("SELECT * FROM ProjetoDeSustentabilidade WHERE ID = %s", (id_alterar,))
        registro = cursor.fetchone()
        
        if not registro:
            print("\nID não encontrado!")
            input('\n\t<< Tecle Enter para continuar >>')
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        
        # Mostrar dados do registro selecionado
        print("\n=-=-=-=-= Registro selecionado =-=-=-=-=")
        print(f"ID: {registro[0]}")
        print(f"Data: {registro[1]}")
        print(f"Consumo de água: {registro[2]} L")
        print(f"Consumo de energia: {registro[3]} kWh")
        print(f"Resíduos não recicláveis: {registro[4]} kg")
        print(f"Resíduos recicláveis: {registro[5]}%")
        print(f"Meios de transporte: {registro[6]}")
        
        # Menu de alteração
        print("\nOpções de alteração:")
        print("1. Alterar todos os dados")
        print("2. Alterar dado específico")
        opcao_alteracao = input("\nEscolha uma opção: ")
        
        if opcao_alteracao == "1":
            # Alterar todos os dados - refazer todas as perguntas
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\n=-=-=-=-= Alterar todos os dados =-=-=-=-=\n")
            
            # Perguntas gerais
            print("\t=-=-=-=-= Perguntas gerais =-=-=-=-=\n\n")
            nova_data = input("\nQual é a nova data (formato dd/mm/aaaa): ")
            novo_consumo_litros = float(input("\n1. Quantos litros de água você consumiu hoje? (Aprox, litros) "))
            novo_consumo_kwh = float(input("\n2. Quantos kWh de energia elétrica você consumiu hoje? "))
            novo_geracao_residuos = float(input("\n3. Quantos KG de resíduos você gerou hoje? "))
            novo_residuos_reciclaveis = float(input("\n4. Quantos KG de resíduos recicláveis você gerou hoje? "))

            os.system('cls' if os.name == 'nt' else 'clear')

            # Perguntas meio de transporte
            print("\n=-=-=-=-= Perguntas sobre uso de transporte =-=-=-=-=\n\n")
            print("\t=-=-=-=-= Responder com S (sim) ou N (não) =-=-=-=-=\n\n")

            novo_transporte_publico = input("\n5. Você usou transporte público hoje? ")
            nova_bicicleta = input("\n6. Você usou bicicleta hoje? ") 
            nova_caminhada = input("\n7. Você caminhou hoje? ")
            novo_carro_comb_fossil = input("\n8. Você usou seu carro com combustível fóssil hoje? ")
            novo_carro_eletrico = input("\n9. Você usou carro elétrico hoje? ")
            nova_carona = input("\n10. Você usou carona compartilhada hoje? ")

            # Montar string de meios de transporte
            meios_usados = []
            if novo_transporte_publico.lower() == 's':
                meios_usados.append("Transporte público")
            if nova_bicicleta.lower() == 's':
                meios_usados.append("Bicicleta")
            if nova_caminhada.lower() == 's':
                meios_usados.append("Caminhada")
            if novo_carro_comb_fossil.lower() == 's':
                meios_usados.append("Carro com combustível fóssil")
            if novo_carro_eletrico.lower() == 's':
                meios_usados.append("Carro elétrico")
            if nova_carona.lower() == 's':
                meios_usados.append("Carona compartilhada")

            meios_de_transporte_str = "; ".join(meios_usados)

            # Atualizar registro principal
            sql_update = """
            UPDATE ProjetoDeSustentabilidade 
            SET DataEntrada = %s, 
                LitrosConsumidos = %s, 
                KWHConsumido = %s, 
                KgNaoReciclaveis = %s, 
                PorcentagemResiduos = %s, 
                MeioDeTransporte = %s
            WHERE ID = %s
            """
            valores_update = (
                nova_data,
                novo_consumo_litros,
                novo_consumo_kwh,
                novo_geracao_residuos,
                novo_residuos_reciclaveis,
                meios_de_transporte_str,
                id_alterar
            )
            cursor.execute(sql_update, valores_update)
            conexao.commit()
            
            # Calcular novos níveis de sustentabilidade
            # Nível de água
            if float(novo_consumo_litros) > 200:
                nivel_agua = "Baixa sustentabilidade"
            elif float(novo_consumo_litros) <= 150:
                nivel_agua = "Alta sustentabilidade"
            else:
                nivel_agua = "Moderada sustentabilidade"
            
            # Nível de energia
            if float(novo_consumo_kwh) >= 10:
                nivel_energia = "Baixa sustentabilidade"
            elif float(novo_consumo_kwh) <= 5:
                nivel_energia = "Alta sustentabilidade"
            else:
                nivel_energia = "Moderada sustentabilidade"
            
            # Nível de resíduos
            if float(novo_geracao_residuos) > 0:
                percentual_lixo = (float(novo_residuos_reciclaveis) / float(novo_geracao_residuos)) * 100
            else:
                percentual_lixo = 0
                
            if percentual_lixo < 20:
                nivel_residuos = "Baixa sustentabilidade"
            elif percentual_lixo > 50:
                nivel_residuos = "Alta sustentabilidade"
            else:
                nivel_residuos = "Moderada sustentabilidade"
            
            # Nível de transporte
            if ('público' in meios_de_transporte_str.lower() or 
                'bicicleta' in meios_de_transporte_str.lower() or 
                'caminhada' in meios_de_transporte_str.lower() or 
                'elétrico' in meios_de_transporte_str.lower()):
                if ('combustível' in meios_de_transporte_str.lower() or 
                    'carona' in meios_de_transporte_str.lower()):
                    nivel_transporte = "Moderada sustentabilidade"
                else:
                    nivel_transporte = "Alta sustentabilidade"
            elif ('combustível' in meios_de_transporte_str.lower() or 
                'carona' in meios_de_transporte_str.lower()):
                nivel_transporte = "Baixa sustentabilidade"
            else:
                nivel_transporte = "nenhum"
            
            # Atualizar tabela Manipulacao_Dados
            sql_update_niveis = """
            UPDATE Manipulacao_Dados 
            SET Nivel_LitrosConsumidos = %s,
                Nivel_KWHConsumido = %s,
                Nivel_KgNaoReciclaveis = %s,
                Nivel_MeioDeTransporte = %s
            WHERE ID_Usuario = %s
            """
            valores_niveis = (criptografia_palavras(chave, nivel_agua), criptografia_palavras(chave, nivel_energia), criptografia_palavras(chave, nivel_residuos), criptografia_palavras(chave, nivel_transporte), id_alterar)
            cursor.execute(sql_update_niveis, valores_niveis)
            conexao.commit()
            
            print("\n=-=-=-=-= Novos níveis de sustentabilidade =-=-=-=-=")
            print(f"\nConsumo de água: {nivel_agua}")
            print(f"Consumo de energia: {nivel_energia}")
            print(f"Resíduos recicláveis: {nivel_residuos}")
            print(f"Meios de transporte: {nivel_transporte}")
            
            print("\nRegistro e níveis de sustentabilidade atualizados com sucesso!")
            
        elif opcao_alteracao == "2":
            # Alterar dado específico
            alterar_mais = True
            while alterar_mais:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("\n=-=-=-=-= Alterar dado específico =-=-=-=-=\n")
                print("Selecione o campo que deseja alterar:")
                print("1. Data")
                print("2. Consumo de água (litros)")
                print("3. Consumo de energia (kWh)")
                print("4. Resíduos não recicláveis (kg)")
                print("5. Resíduos recicláveis (%)")
                print("6. Meios de transporte")
                
                campo_alterar = input("\nDigite o número do campo que deseja alterar: ")
                
                # Obter valores atuais para recálculo
                cursor.execute("SELECT LitrosConsumidos, KWHConsumido, KgNaoReciclaveis, PorcentagemResiduos, MeioDeTransporte FROM ProjetoDeSustentabilidade WHERE ID = %s", (id_alterar,))
                dados_atuais = cursor.fetchone()
                
                consumo_litros = float(dados_atuais[0])
                consumo_kwh = float(dados_atuais[1])
                geracao_residuos = float(dados_atuais[2])
                residuos_reciclaveis = float(dados_atuais[3])
                meios_transporte = dados_atuais[4]
                
                novo_valor = None
                campo_nome = ""
                if campo_alterar == "1":
                    campo_nome = "DataEntrada"
                    novo_valor = input("Nova data (dd/mm/aaaa): ")
                elif campo_alterar == "2":
                    campo_nome = "LitrosConsumidos"
                    novo_valor = float(input("Novo consumo de água (litros): "))
                    consumo_litros = float(novo_valor)
                elif campo_alterar == "3":
                    campo_nome = "KWHConsumido"
                    novo_valor = float(input("Novo consumo de energia (kWh): "))
                    consumo_kwh = float(novo_valor)
                elif campo_alterar == "4":
                    campo_nome = "KgNaoReciclaveis"
                    novo_valor = float(input("Novos resíduos não recicláveis (kg): "))
                    geracao_residuos = float(novo_valor)
                elif campo_alterar == "5":
                    campo_nome = "PorcentagemResiduos"
                    novo_valor = float(input("Novos resíduos recicláveis (%): "))
                    residuos_reciclaveis = float(novo_valor)
                elif campo_alterar == "6":
                    campo_nome = "MeioDeTransporte"
                    print("\nResponda com S (sim) ou N (não) para cada meio de transporte:")
                    transporte_publico = input("Usou transporte público? ")
                    bicicleta = input("Usou bicicleta? ")
                    caminhada = input("Caminhou? ")
                    carro_comb_fossil = input("Usou carro com combustível fóssil? ")
                    carro_eletrico = input("Usou carro elétrico? ")
                    carona = input("Usou carona compartilhada? ")
                    
                    meios_usados = []
                    if transporte_publico.lower() == 's':
                        meios_usados.append("Transporte público")
                    if bicicleta.lower() == 's':
                        meios_usados.append("Bicicleta")
                    if caminhada.lower() == 's':
                        meios_usados.append("Caminhada")
                    if carro_comb_fossil.lower() == 's':
                        meios_usados.append("Carro com combustível fóssil")
                    if carro_eletrico.lower() == 's':
                        meios_usados.append("Carro elétrico")
                    if carona.lower() == 's':
                        meios_usados.append("Carona compartilhada")
                    
                    novo_valor = "; ".join(meios_usados)
                    meios_transporte = novo_valor
                else:
                    print("Opção inválida!")
                    continue
                
                # Executar atualização no registro principal
                if campo_alterar != "6":
                    sql_update = f"UPDATE ProjetoDeSustentabilidade SET {campo_nome} = %s WHERE ID = %s"
                    cursor.execute(sql_update, (novo_valor, id_alterar))
                else:
                    sql_update = "UPDATE ProjetoDeSustentabilidade SET MeioDeTransporte = %s WHERE ID = %s"
                    cursor.execute(sql_update, (novo_valor, id_alterar))
                conexao.commit()
                
                # Calcular novos níveis de sustentabilidade
                # Nível de água
                if float(consumo_litros) > 200:
                    nivel_agua = "Baixa sustentabilidade"
                elif float(consumo_litros) <= 150:
                    nivel_agua = "Alta sustentabilidade"
                else:
                    nivel_agua = "Moderada sustentabilidade"
                
                # Nível de energia
                if float(consumo_kwh) >= 10:
                    nivel_energia = "Baixa sustentabilidade"
                elif float(consumo_kwh) <= 5:
                    nivel_energia = "Alta sustentabilidade"
                else:
                    nivel_energia = "Moderada sustentabilidade"
                
                # Nível de resíduos
                if float(geracao_residuos) > 0:
                    percentual_lixo = (float(residuos_reciclaveis) / float(geracao_residuos)) * 100
                else:
                    percentual_lixo = 0
                    
                if percentual_lixo < 20:
                    nivel_residuos = "Baixa sustentabilidade"
                elif percentual_lixo > 50:
                    nivel_residuos = "Alta sustentabilidade"
                else:
                    nivel_residuos = "Moderada sustentabilidade"
                
                # Nível de transporte
                if ('público' in meios_transporte.lower() or 
                    'bicicleta' in meios_transporte.lower() or 
                    'caminhada' in meios_transporte.lower() or 
                    'elétrico' in meios_transporte.lower()):
                    if ('combustível' in meios_transporte.lower() or 
                        'carona' in meios_transporte.lower()):
                        nivel_transporte = "Moderada sustentabilidade"
                    else:
                        nivel_transporte = "Alta sustentabilidade"
                elif ('combustível' in meios_transporte.lower() or 
                    'carona' in meios_transporte.lower()):
                    nivel_transporte = "Baixa sustentabilidade"
                else:
                    nivel_transporte = "Sem dados suficientes"
                
                # Atualizar tabela Manipulacao_Dados
                sql_update_niveis = """
                UPDATE Manipulacao_Dados 
                SET Nivel_LitrosConsumidos = %s,
                    Nivel_KWHConsumido = %s,
                    Nivel_KgNaoReciclaveis = %s,
                    Nivel_MeioDeTransporte = %s
                WHERE ID_Usuario = %s
                """
                valores_niveis = (criptografia_palavras(chave, nivel_agua), criptografia_palavras(chave, nivel_energia), criptografia_palavras(chave, nivel_residuos), criptografia_palavras(chave, nivel_transporte), id_alterar)
                cursor.execute(sql_update_niveis, valores_niveis)
                conexao.commit()
                
                print("\n=-=-=-=-= Novos níveis de sustentabilidade =-=-=-=-=")
                print(f"\nConsumo de água: {nivel_agua}")
                print(f"Consumo de energia: {nivel_energia}")
                print(f"Resíduos recicláveis: {nivel_residuos}")
                print(f"Meios de transporte: {nivel_transporte}")
                
                print("\nCampo e níveis de sustentabilidade atualizados com sucesso!")
                
                # Perguntar se deseja alterar mais algo
                continuar = input("\nDeseja alterar mais algum campo neste registro? (S/N): ")
                if continuar.lower() != 's':
                    alterar_mais = False
        else:
            print("Opção inválida!")
        
        input('\n\t<< Tecle Enter para continuar >>')
        os.system('cls' if os.name == 'nt' else 'clear')

    elif opcao == "3":      
        cursor.execute("SELECT * FROM ProjetoDeSustentabilidade")
        resultado = cursor.fetchall()

        print('\n\033[1m=-=-=-=-= Apagar registros: =-=-=-=-=\033[0m\n')
        print('='*143)
        print(f'\033[1m{"| ID ":^5}', end='|')
        print(f'{"Data de registro":^20}', end='|')
        print(f'{"Consumo de água (L)":^20}', end='|')
        print(f'{"Consumo de energia (kWh)":^25}', end='|')
        print(f'{"Lixo não reciclável (Kg)":^25}', end='|')
        print(f'{"% Resíduos recicláveis":^25}', end='|')
        print(f'{"Meio de transporte":^50}', end='|\033[0m\n')
        print('='*143)

        for linha in resultado:
            print(f'{linha[0]:^5}', end='|')
            print(f'{linha[1]:^20}', end='|')
            print(f'{str(linha[2]) + " L":^20}', end='|')
            print(f'{str(linha[3]) + " kWh":^25}', end='|')
            print(f'{str(linha[4]) + " Kg":^25}', end='|')
            print(f'{str(linha[5]) + " %":^25}', end='|')
            print(f'{linha[6]:^20}', end='|\n')
            print('-'*143)
        
        # Selecionar ID para apagar
        id_apagar = input("\nDigite o ID do registro que deseja apagar: ")
        
        # Verificar se o ID existe
        cursor.execute("SELECT * FROM ProjetoDeSustentabilidade WHERE ID = %s", (id_apagar,))
        registro = cursor.fetchone()
        
        if not registro:
            print("\nID não encontrado!")
            input('\n\t<< Tecle Enter para continuar >>')
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        
        # Mostrar dados do registro selecionado
        print("\n=-=-=-=-= Registro selecionado =-=-=-=-=")
        print(f"ID: {registro[0]}")
        print(f"Data: {registro[1]}")
        print(f"Consumo de água: {registro[2]} L")
        print(f"Consumo de energia: {registro[3]} kWh")
        print(f"Resíduos não recicláveis: {registro[4]} kg")
        print(f"Resíduos recicláveis: {registro[5]}%")
        print(f"Meios de transporte: {registro[6]}")
        
        # Menu de apagar
        print("\nOpções de apagar:")
        print("1. Apagar todos os dados (registro completo)")
        # print("2. Apagar dado específico")
        print("2. Cancelar")
        opcao_apagar = input("\nEscolha uma opção: ")
        
        if opcao_apagar == "1":
            # Confirmar apagar tudo
            confirmacao = input("\nTem certeza que deseja apagar TODOS os dados deste registro? Esta ação não pode ser desfeita. (S/N): ")
            if confirmacao.lower() == 's':
                try:
                    # Primeiro apagar da tabela de níveis (filha)
                    cursor.execute("DELETE FROM Manipulacao_Dados WHERE ID_Usuario = %s", (id_apagar,))
                    # Depois apagar da tabela principal (pai)
                    cursor.execute("DELETE FROM ProjetoDeSustentabilidade WHERE ID = %s", (id_apagar,))
                    conexao.commit()
                    print("\nRegistro apagado com sucesso!")
                except mysql.connector.Error as err:
                    conexao.rollback()
                    print(f"\nErro ao apagar registro: {err}")
            else:
                print("\nOperação cancelada.")
        # opção de cancelar
        elif opcao_apagar == "2":
            print("\nOperação cancelada.")
        else:
            print("\nOpção inválida!")
        
        input('\n\t<< Tecle Enter para continuar >>')
        os.system('cls' if os.name == 'nt' else 'clear')

    # opção de listar registros
    elif opcao == "4":
        # Coleta os dados dos registros
        cursor.execute("SELECT * FROM ProjetoDeSustentabilidade")
        resultado = cursor.fetchall()

        print('\n\033[1m=-=-=-=-= Exibição dos dados inseridos: =-=-=-=-=\033[0m\n')
        print('='*143)
        print(f'\033[1m{"| ID ":^5}', end='|')
        print(f'{"Data de registro":^20}', end='|')
        print(f'{"Consumo de água (L)":^20}', end='|')
        print(f'{"Consumo de energia (kWh)":^25}', end='|')
        print(f'{"Lixo não reciclável (Kg)":^25}', end='|')
        print(f'{"% Resíduos recicláveis":^25}', end='|')
        print(f'{"Meio de transporte":^50}', end='|\033[0m\n')
        print('='*143)

        for linha in resultado:
            print(f'{linha[0]:^5}', end='|')
            print(f'{linha[1]:^20}', end='|')
            print(f'{str(linha[2]) + " L":^20}', end='|')
            print(f'{str(linha[3]) + " kWh":^25}', end='|')
            print(f'{str(linha[4]) + " Kg":^25}', end='|')
            print(f'{str(linha[5]) + " %":^25}', end='|')
            print(f'{linha[6]:^20}', end='|\n')
            print('-'*143)

        # Aqui você deve adicionar a consulta para Manipulacao_Dados
        cursor.execute("SELECT * FROM Manipulacao_Dados")
        resultado_class2 = cursor.fetchall()

        print('\n\033[1m=-=-=-=-= Exibição da classificação dos dados armazenados: =-=-=-=-=\033[0m\n')
        print('='*143)
        print(f'\033[1m{"| ID ":^5}', end='|')
        print(f'{"Consumo de água ":^30}', end='|')
        print(f'{"Consumo de energia ":^30}', end='|')
        print(f'{"% de lixo reciclável gerado ":^32}', end='|')
        print(f'{"Meios de transportes utilizados":^41}', end='|\033[0m\n')
        print('='*143)

        for i, linha in enumerate(resultado_class2):
            id_usuario = linha[0]
            consumo_agua = descriptografia_palavras(chave, linha[1])
            consumo_energia = descriptografia_palavras(chave, linha[2])
            lixo_reciclavel = descriptografia_palavras(chave, linha[3])
            meio_transporte = descriptografia_palavras(chave, linha[4])

            print(f'|{id_usuario:^4}', end='|')
            print(f'{consumo_agua:^30}', end='|')
            print(f'{consumo_energia:^30}', end='|')
            print(f'{lixo_reciclavel:^32}', end='|')
            print(f'{meio_transporte:^41}', end='|\n')
            print('-'*143)

    #opção para listar a média dos registros
    elif opcao == "5":
        print('='*50)
        print('Média dos dados coletados')
        print('='*50)

        # Média Água
        cursor.execute("SELECT AVG(LitrosConsumidos) FROM ProjetoDeSustentabilidade")
        media_agua = cursor.fetchone()[0]
        print(f'\nMédia do consumo de água: {media_agua:.2f} L')
        if media_agua >= 150:
            if media_agua > 200:
                print("Classificação do consumo de água: Baixa sustentabilidade\n")
            else:
                print("Classificação do consumo de água: Moderada sustentabilidade\n")
        else:
            print("Classificação do consumo de água: Alta sustentabilidade\n")

        # Média Energia
        cursor.execute("SELECT AVG(KWHConsumido) FROM ProjetoDeSustentabilidade")
        media_energia = cursor.fetchone()[0]
        print(f'Média do consumo de energia: {media_energia:.2f} kWh')
        if media_energia >= 300:
            print("Classificação do consumo de energia: Baixa sustentabilidade\n")
        elif media_energia >= 100:
            print("Classificação do consumo de energia: Moderada sustentabilidade\n")
        else:
            print("Classificação do consumo de energia: Alta sustentabilidade\n")

        # Média Porcentagem de resíduos recicláveis
        cursor.execute("SELECT AVG(PorcentagemResiduos) FROM ProjetoDeSustentabilidade")
        media_residuos = cursor.fetchone()[0]
        print(f'Média da porcentagem de resíduos recicláveis: {media_residuos:.2f}%')
        if media_residuos <= 20:
            print("Classificação dos resíduos recicláveis: Baixa sustentabilidade\n")
        elif media_residuos <= 50:
            print("Classificação dos resíduos recicláveis: Moderada sustentabilidade\n")
        else:
            print("Classificação dos resíduos recicláveis: Alta sustentabilidade\n")

        # Análise dos meios de transporte
        cursor.execute("SELECT MeioDeTransporte FROM ProjetoDeSustentabilidade")
        dados_transporte = cursor.fetchall()

        class_transporte = []
        for linha in dados_transporte:
            transporte = linha[0].lower() if linha[0] else ""

            usa_publico = 'público' in transporte
            usa_bicicleta = 'bicicleta' in transporte
            usa_caminhada = 'caminhada' in transporte
            usa_eletrico = 'elétrico' in transporte
            usa_combustivel = 'combustível' in transporte
            usa_carro = 'carro' in transporte and 'elétrico' not in transporte and 'carona' not in transporte

            if (usa_publico or usa_bicicleta or usa_caminhada or usa_eletrico) and (usa_combustivel or usa_carro):
                class_transporte.append(2)  # Moderada
            elif usa_publico or usa_bicicleta or usa_caminhada or usa_eletrico:
                class_transporte.append(1)  # Alta
            else:
                class_transporte.append(3)  # Baixa

        print('Média da classificação de transportes: ', end='')
        if all(c == 1 for c in class_transporte):
            print('Alta sustentabilidade\n')
        elif all(c == 3 for c in class_transporte):
            print('Baixa sustentabilidade\n')
        else:
            print('Moderada sustentabilidade\n')

    # Opção para finalizar o programa 
    elif opcao == '6':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Encerrando o programa. Até logo!")

    # Opção inválida
    else:
        print("\nOpção inválida. Tente novamente.")