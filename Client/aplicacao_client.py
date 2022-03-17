from cmath import inf
import random as rd
from enlace import *
import time
import numpy as np
#   python -m serial.tools.list_ports

# Abrindo imagem
enderecoImg = r"C:\Users\paulo\Projetos_facul\CamFis\projetos\projeto3\Client\file.jpg"
imgBinary = open(enderecoImg, 'rb').read()
# print(imgBinary)

comandos = []
lenB = len(imgBinary)

tamanho = lenB/114 if lenB % 114 == 0 else int(lenB/114) + 1
computado = 0

numero = 1
i = 0
while computado <= lenB:
    j = i + 114
    if j > lenB:
        j = lenB
    
    size = len(imgBinary[i:j]).to_bytes(1, byteorder ="big")
    n_comando = numero.to_bytes(2, byteorder ="big")
    lenComandos = tamanho.to_bytes(2, byteorder = "big")
    zeros = b'\x00\x00\x00\x00\x00'
    tail = b'\x00\x01\x02\x03'
    comando = n_comando + size + lenComandos +zeros + imgBinary[i:j] + tail
    
    # print(comando)
    # print(len(comando))
    # print(comando[0:2])
    # print(comando[2])
    # break
    comandos.append(comando)
    i += 114
    numero += 1
    computado += 114

# print(len(comandos[0]), comandos[-1][3:5], comandos[-1][0:2])

serialName = "COM4"

def main():
    try:
        tempo_inicial = time.time()
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Comunication open") 

        #handshake
        while True:
            handshake = b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x02\x03'
            

            
            txBuffer = handshake
            print(txBuffer)
            print("\n-------------------------")
        
            print("Handshake")

            print("\n-------------------------")


            inicio_timer = time.time()
            com1.sendData(np.asarray(txBuffer), inicio_timer)
            

            print("Command sent")  
            print("-------------------------")

            
            print("\n-------------------------")
            print(f"{len(txBuffer)} bytes were sent")
            print(txBuffer)
            print("-------------------------\n")

        
            
            rxBuffer, nRx = com1.getData(len(txBuffer), inicio_timer, 5)
            if rxBuffer == -1:
                while True:
                    resp = input("Servidor inativo. Tentar novamente? S/N\n")
                    if resp == "N":
                        com1.disable()
                        return
                    elif resp == "S":
                        break
                
            
            else:
                print("\n-------------------------")
                print(f"Server sent {len(rxBuffer)} bytes")
                print(rxBuffer)
                print("-------------------------\n")

                if rxBuffer == txBuffer:
                    print('-'*50)
                    print("Handshake was successful :)")
                    print('-'*50)
                
                else:
                    print('-'*50)
                    print("Handshake wasn't successful :(")
                    print('-'*50)
                break
            
        # transmissao da imagem em pacotes certo

        # simulacao 3 cliente manda número de pacote errado
        # size = len(imgBinary[0:114]).to_bytes(1, byteorder ="big")
        # n_comando = b'\xFF\xFF'
        # zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        # tail = b'\x00\x01\x02\x03'
        # comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        # comandos = [comando_errado]

        # simulacao 4 tamanho do comando enviado está errado
        size = len(imgBinary[0:89]).to_bytes(1, byteorder ="big")
        n_comando = b'\x00\x01'
        zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        tail = b'\x00\x01\x02\x03'
        comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        comandos = [comando_errado]

        enviados = 0
        erros = 0
        while enviados < len(comandos):
            print('-'*50)
            print(f'Enviados:{enviados + 1}')
            print(f'Erros:{erros}')
            inicio_timer = time.time()
            txBuffer = comandos[enviados]
            com1.sendData(np.asarray(txBuffer), inicio_timer)
            time.sleep(.27)
            index = txBuffer[:2]
            print(f'index cliente:{index}')

            indexServer, nRx = com1.getData(2, inicio_timer, 0.5)
            print(f'index servidor:{indexServer}')

            if index == indexServer:
                enviados += 1
                erros = 0
            else:
                erros += 1
            if erros > 8:
                com1.disable()
                print('-'*50)
                print("Erro ao enviar dados")
                print('-'*50)
                return

        # inicio_timer = time.time()
        # txBuffer = b'\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x01\x02\x03'
        # com1.sendData(np.asarray(txBuffer), inicio_timer)

        print("-"*50)
        print("Sucesso no envio dos dados")
        print("-"*50)
        com1.disable()

        # simulacao 3 cliente manda número de pacote errado
        # size = len(imgBinary[0:114]).to_bytes(1, byteorder ="big")
        # n_comando = b'\xFF\xFF'
        # zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        # tail = b'\x00\x01\x02\x03'
        # comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        # comandos = [comando_errado]
        # enviados = 0
        # erros = 0
        # while enviados < len(comandos):
        #     print('-'*50)
        #     print(f'Enviados:{enviados + 1}')
        #     print(f'Erros:{erros}')
        #     inicio_timer = time.time()
        #     txBuffer = comandos[enviados]
        #     com1.sendData(np.asarray(txBuffer), inicio_timer)
        #     time.sleep(.05)
        #     index = txBuffer[:2]
        #     print(f'index cliente:{index}')

        #     indexServer, nRx = com1.getData(2, inicio_timer, 0.5)
        #     print(f'index servidor:{indexServer}')

        #     if index == indexServer:
        #         enviados += 1
        #         erros = 0
        #     else:
        #         erros += 1
        #     if erros > 8:
        #         com1.disable()
        #         print('-'*50)
        #         print("Erro ao enviar dados")
        #         print('-'*50)
        #         return
        
        # simulacao 4 tamanho do comando enviado está errado
        # size = len(imgBinary[0:89]).to_bytes(1, byteorder ="big")
        # n_comando = b'\x00\x01'
        # zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        # tail = b'\x00\x01\x02\x03'
        # comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        # comandos = [comando_errado]
        # enviados = 0
        # erros = 0
        # while enviados < len(comandos):
        #     print('-'*50)
        #     print(f'Enviados:{enviados + 1}')
        #     print(f'Erros:{erros}')
        #     inicio_timer = time.time()
        #     txBuffer = comandos[enviados]
        #     com1.sendData(np.asarray(txBuffer), inicio_timer)
        #     time.sleep(.05)
        #     index = txBuffer[:2]
        #     print(f'index cliente:{index}')

        #     indexServer, nRx = com1.getData(2, inicio_timer, 0.5)
        #     print(f'index servidor:{indexServer}')

        #     if index == indexServer:
        #         enviados += 1
        #         erros = 0
        #     else:
        #         erros += 1
        #     if erros > 8:
        #         com1.disable()
        #         print('-'*50)
        #         print("Erro ao enviar dados")
        #         print('-'*50)
        #         return



            

       

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

    
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()