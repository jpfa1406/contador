"""
Criado em 07/Fevereiro/2022

@autor: Marco Mello e Paulo Santos


Regras:

1) O Arquivo ASM.txt não pode conter linhas iniciadas com caracter ' ' ou '\n')
2) Linhas somente com comentários são excluídas 
3) Instruções sem comentário no arquivo ASM receberão como comentário no arquivo BIN a própria instrução
4) Exemplo de codigo invalido:
                            0.___JSR @14 #comentario1
                            1.___#comentario2           << Invalido ( Linha somente com comentário )
                            2.___                       << Invalido ( Linha vazia )
                            3.___JMP @5  #comentario3
                            4.___JEQ @9
                            5.___NOP
                            6.___NOP
                            7.___                       << Invalido ( Linha vazia )
                            8.___LDI $5                 << Invalido ( Linha iniciada com espaço (' ') )
                            9.___ STA $0
                            10.__CEQ @0
                            11.__JMP @2  #comentario4
                            12.__NOP
                            13.__ LDI $4                << Invalido ( Linha iniciada com espaço (' ') )
                            14.__CEQ @0
                            15.__JEQ @3
                            16.__#comentario5           << Invalido ( Linha somente com comentário )
                            17.__JMP @13
                            18.__NOP
                            19.__RET
                                
5) Exemplo de código válido (Arquivo ASM.txt):
                            0.___JSR @14 #comentario1
                            1.___JMP @5  #comentario3
                            2.___JEQ @9
                            3.___NOP
                            4.___NOP
                            5.___LDI $5
                            6.___STA $0
                            7.___CEQ @0
                            8.___JMP @2  #comentario4
                            9.___NOP
                            10.__LDI $4
                            11.__CEQ @0
                            12.__JEQ @3
                            13.__JMP @13
                            14.__NOP
                            15.__RET
                            
6) Resultado do código válido (Arquivo BIN.txt):
                            0.__tmp(0) := x"90E"; -- comentario1
                            1.__tmp(1) := x"605"; -- comentario3
                            2.__tmp(2) := x"709"; -- JEQ @9
                            3.__tmp(3) := x"000"; -- NOP
                            4.__tmp(4) := x"000"; -- NOP
                            5.__tmp(5) := x"405"; -- LDI $5
                            6.__tmp(6) := x"500"; -- STA $0
                            7.__tmp(7) := x"800"; -- CEQ @0
                            8.__tmp(8) := x"602"; -- comentario4
                            9.__tmp(9) := x"000"; -- NOP
                            10._tmp(10) := x"404"; -- LDI $4
                            11._tmp(11) := x"800"; -- CEQ @0
                            12._tmp(12) := x"703"; -- JEQ @3
                            13._tmp(13) := x"60D"; -- JMP @13
                            14._tmp(14) := x"000"; -- NOP
                            15._tmp(15) := x"A00"; -- RET

"""



assembly = 'ASM.txt' #Arquivo de entrada de contem o assembly
destinoBIN = 'BIN.txt' #Arquivo de saída que contem o binário formatado para VHDL

#definição dos mnemônicos e seus
#respectivo OPCODEs (em Hexadecimal)
mne =	{ 
       "NOP":   "0000",
       "LDA":   "0001",
       "SOMA":  "0010",
       "SUB":   "0011",
       "LDI":   "0100",
       "STA":   "0101",
       "JMP":   "0110",
       "JEQ":   "0111",
       "CEQ":   "1000",
       "JSR":   "1001",
       "RET":   "1010",
       "ANDI":   "1011",
       "CGT":   "1100",
       "JGT":   "1101",
       "ADDI":  "1110",
       "SUBI":  "1111"
}

#definição dos enderecos, variáveis e constantes
#dos respectivos inputs e outputs (em Decimal)
mapa = {
        "LEDR7": 256,
        "LEDR8": 257,
        "LEDR9": 258,

        "HEX0": 288,
        "HEX1": 289,
        "HEX2": 290,
        "HEX3": 291,
        "HEX4": 292,
        "HEX5": 293,

        "SW7": 320,
        "SW8": 321,
        "SW9": 322,

        "KEY0": 352,
        "KEY1": 353,
        "KEY2": 354,
        "KEY3": 355,
        "FPGA_RESET": 356,

        "SUNI": 0,
        "SDEC": 1,
        "MUNI": 2,
        "MDEC": 3,
        "HUNI": 4,
        "HDEC": 5,

        "VAR1": 7,
        "VAR10": 8,
        "VAR6": 9,
        "VAR3": 10,
        "VAR5": 11,
        "VAR9": 12,
        "VAR4": 13,
        "VAR2": 14,

        "FLAG": 15,

        "CLR0": 511,
        "CLR1": 510,
        "CLR2": 509,
        "CLR3": 508,
        "CLRR": 507,
}

# definição dos registradores (em decimal)
regis = {
        "R0" : 0, #Reg pra uso geral
        "R1" : 1, 
        "R2" : 2, 
        "R3" : 3, 
        "R4" : 4, 
        "R5" : 5, 
        "R6" : 6, 
        "R7" : 7, #Segura 0
}

jumps = ["JMP", "JEQ", "JSR", "RET", "JGT"]

#Converte o valor após o caractere arroba '@'
#em um valor hexadecimal de 2 dígitos (8 bits)
def converteArroba(line):
    line = line.split('@')[1]
    if ', ' in line:
        line = line.split(', ')[0]
    if line in mapa.keys():
        line = mapa[line]

    return f"{int(line):09b}"

# Consulta o dicionário de registradores e "converte"
# o registrador em seu respectivo valor em binário
def converteReg(line):
    line = line.split(' ')
    if len(line) > 2:
        if '@' in line[1]:
            return f"{regis[line[2]]:03b}"
        else:
            return f"{regis[line[2]]:03b}"
    else:
        return "000"
 
#Converte o valor após o caractere cifrão'$'
#em um valor hexadecimal de 2 dígitos (8 bits) 
def converteCifrao(line):
    line = line.split('$')
    n = line[1]
    n = n.split(',')
    return f"{int(n[0]):09b}"
        
#Define a string que representa o comentário
#a partir do caractere cerquilha '#'
def defineComentario(line):
    if '#' in line:
        line = line.split('#')
        line = line[0] + "\t#" + line[1]
        return line
    else:
        return line

#Remove o comentário a partir do caractere cerquilha '#',
#deixando apenas a instrução
def defineInstrucao(line):
    line = line.split('#')
    line = line[0]
    return line
    
#Consulta o dicionário e "converte" o mnemônico em
#seu respectivo valor em hexadecimal
def trataMnemonico(line):
    line = line.replace("\n", "") #Remove o caracter de final de linha
    line = line.replace("\t", "") #Remove o caracter de tabulacao
    line = line.split(' ')
    op = line[0]
    line[0] = mne[line[0]]
    line = "".join(line)
    return line, op

with open(assembly, "r") as f: #Abre o arquivo ASM
    lines = f.readlines() #Verifica a quantidade de linhas
    
    
with open(destinoBIN, "w") as f:  #Abre o destino BIN

    cont = 0 #Cria uma variável para contagem

    #Verificar labels e guardar seus endereços
    for line in lines:
        #Verificar se tem comentarios ou linhas em branco para ignorar e nao afetar a contagem
        if (line.startswith('\n') or line.startswith(' ') or line.startswith('#')):
            cont-=1
        #Identifica label e guarda a sua linha
        elif ':' in line:
            line = line.split(':')
            mapa[line[0]] = cont
            cont-=1
        cont+=1
    
    cont = 0 #Reset variável para contagem

    for line in lines:        
        
        #Verifica se a linha começa com alguns caracteres invalidos ('\n' ou ' ' ou '#')
        if (line.startswith('\n') or line.startswith(' ') or line.startswith('#')):
            line = line.replace("\n", "")
            #print("-- Sintaxe invalida" + ' na Linha: ' + ' --> (' + line + ')') #Print apenas para debug
            #pass
        
        #Verifica se tem label na linha
        elif ':' in line:
            line = line.split(':')
            line = '\n-- ' + line[0] + '\n'
            f.write(line) # Escreve no arquivo BIN.txt

        #Se a linha for válida para conversão, executa
        else:
            
            #Exemplo de linha => 1. JSR @14 #comentario1
            comentarioLine = defineComentario(line).replace("\n","") #Define o comentário da linha. Ex: #comentario1
            instrucaoLine = defineInstrucao(line).replace("\n","") #Define a instrução. Ex: JSR @14
            
            opcode, op = trataMnemonico(instrucaoLine) #Trata o mnemonico. Ex(JSR @14): x"9" @14

            if op in jumps:
                reg = "000"
            else:
                reg = converteReg(instrucaoLine)
                  
            if '@' in instrucaoLine: #Se encontrar o caractere arroba '@' 
                imediato = converteArroba(instrucaoLine) #converte o número após o caractere Ex(JSR @14): x"9" x"0E"
                    
            elif '$' in instrucaoLine: #Se encontrar o caractere cifrao '$' 
                imediato = converteCifrao(instrucaoLine) #converte o número após o caractere Ex(LDI $5): x"4" x"05"
                
            else: #Senão, se a instrução nao possuir nenhum imediator, ou seja, nao conter '@' ou '$'
                imediato = '000000000' #Acrescenta o valor x"00". Ex(RET): x"A" x"00"
                
            #construir line de acordo com a memoria rom onde o '1' é instrucaoLine[2]
            line = 'tmp(' + str(cont) + ') := "' + opcode[:4] + '" & "' + reg  + '" & "' + imediato + '";\t-- ' + comentarioLine + '\n'  #Formata para o arquivo BIN
                                                                                                       #Entrada => 1. JSR @14 #comentario1
                                                                                                       #Saída =>   1. tmp(0) := "1001" & '0' & x"0E";	-- JSR @14 	#comentario1
                                        
            cont+=1 #Incrementa a variável de contagem, utilizada para incrementar as posições de memória no VHDL
            f.write(line) #Escreve no arquivo BIN.txt
            
            #print(line,end = '') #Print apenas para debug

