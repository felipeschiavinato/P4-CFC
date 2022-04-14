
from enlace import *
import time
import numpy as np
from utils import *

#   python -m serial.tools.list_ports

# Abrindo imagem
enderecoImg = r"C:\Users\felip\Desktop\Insper 4\CFC\P4\Client\file.jpg"
imgBinary = open(enderecoImg, 'rb').read()
# print(imgBinary)

datagramas = constroi_datagramas(imgBinary)
numPck = len(datagramas)

print(f'''Quantidade de datagramas: {len(datagramas)}, 
          Tamanho primeiro datagrama: {len(datagramas[1])}, 
          EOP primeiro datagrama: {datagramas[1][-4:]}''')

print(datagramas)

serialName = "COM7"
simulation = 5

def main():
    com1 = enlace(serialName)
    com1.enable()
    print("Comunication open") 

    identificador_servidor = 1
    inicio = False
    msgT1 = constroi_handshake(identificador_servidor, numPck)

    # print(msgT1[0], type(msgT1[0]))

    while not inicio:
        print("rodei")
        inicio_timer = time.time()
        print(msgT1)
        com1.sendData(np.asarray(msgT1), inicio_timer)
        log(msgT1, "envia", simulation)

        print(f'''Mandando Handshake para servidor 
                com id: {identificador_servidor}''') 
        time.sleep(5)


        timeout = com1.rx.getIsEmpty()

        if not timeout:
            inicio_timer = time.time()
            rxBuffer, nRx = com1.getData(len(msgT1), inicio_timer, 2)

        # timeout = False
        # if rxBuffer == -1:
        #     timeout = True


        # print(rxBuffer)
        if not timeout:

            log(rxBuffer, "receb", simulation)
            if rxBuffer[0] == 2 and rxBuffer[2]==identificador_servidor:
                inicio = True
        
    print("Saiu do inicio")
    print("Envio do arquivo vai começar")
    cont = 1

    while cont <= numPck:
        msgT3 = datagramas[cont]
        print(msgT3)

        timer1 = time.time()
        timer2 = time.time()
        com1.sendData(np.asarray(msgT3), timer1)
        time.sleep(1)
        log(msgT3, "envia", simulation)
        print("-"*50)
        print(f"Enviando msg tipo 3 com indice: {cont}")

        verifica = True
        while verifica:

            # print("Inciando verificações")

            timeout = com1.rx.getIsEmpty()

            if not timeout:
                inicio_timer = time.time()
                rxBuffer, nRx = com1.getData(10, inicio_timer, 10)

            # timeout = False
            # if rxBuffer == -1:
            #     print("Time out get head")
            #     timeout = True

            # print(rxBuffer)

            len_content = 0
            if not timeout:
                len_content = rxBuffer[5] + 4

            if not timeout:
                inicio_timer = time.time()
                rxBuffer_content, nRx = com1.getData(len_content, inicio_timer, 2)

            # timeout_content = False
            # if rxBuffer_content == -1:
            #     print("Time out get content")
            #     timeout_content = True

            msgTipo4 = False
            if not timeout:
                log(rxBuffer+rxBuffer_content, "receb", simulation)


                if rxBuffer[0] == 4:
                    print("Cliente recebeu msg tipo 4!")
                    verifica = False
                    msgTipo4 = True
                    cont+=1
                
            if (time.time() - timer1) > 5 and not msgTipo4:
                print("Timer 1 maior que 5 segundos")
                print("Reenviando msg tipo 3")
                timer1 = time.time()
                print(msgT3)
                com1.sendData(np.asarray(msgT3), timer1)
                log(msgT3, "envia", simulation)

            if (time.time()-timer2) > 20 and not msgTipo4:
                print("Timer 2 maior que 20 segundos")
                print("Enviando msg tipo 5")
                msgT5 = constroi_msgT5(numPck)
                print(msgT5)
                inicio_timer = time.time()
                com1.sendData(np.asarray(msgT5), inicio_timer)
                log(msgT3, "envia", simulation)

                print(":-(")
                com1.disable()
                return
            if not timeout:
                if rxBuffer[0] == 6:
                    print("Recebeu msg tipo 6 (erro)")
                    print(f"Redefinindo cont:{cont} para {rxBuffer[6]}")
                    print("Reenviando msg tipo 3 com cont corrigido")
                    print("Resetando os dois timers")
                    cont = rxBuffer[6]
                    timer1 = time.time()
                    timer2 = time.time()

                    msgT3 = datagramas[cont]
                    print(msgT3)

                    com1.sendData(np.asarray(msgT3), timer1)
                    log(msgT3, "envia", simulation)
            # else:
            #     verifica = False

    
    print("Sucesso!!!")
    com1.disable()
        
        # tempo_inicial = time.time()
        # #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # #para declarar esse objeto é o nome da porta.
        # com1 = enlace(serialName)
        
    
        # # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        # com1.enable()
        
        # #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        # print("Comunication open") 

        # #handshake
        # while True:
        #     handshake = b'\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x02\x03'
            

            
        #     txBuffer = handshake
        #     print(txBuffer)
        #     print("\n-------------------------")
        
        #     print("Handshake")

        #     print("\n-------------------------")


        #     inicio_timer = time.time()
        #     com1.sendData(np.asarray(txBuffer), inicio_timer)
            

        #     print("Command sent")  
        #     print("-------------------------")

            
        #     print("\n-------------------------")
        #     print(f"{len(txBuffer)} bytes were sent")
        #     print(txBuffer)
        #     print("-------------------------\n")

        
            
        #     rxBuffer, nRx = com1.getData(len(txBuffer), inicio_timer, 5)
        #     if rxBuffer == -1:
        #         while True:
        #             resp = input("Servidor inativo. Tentar novamente? S/N\n")
        #             if resp == "N":
        #                 com1.disable()
        #                 return
        #             elif resp == "S":
        #                 break
                
            
        #     else:
        #         print("\n-------------------------")
        #         print(f"Server sent {len(rxBuffer)} bytes")
        #         print(rxBuffer)
        #         print("-------------------------\n")

        #         if rxBuffer == txBuffer:
        #             print('-'*50)
        #             print("Handshake was successful :)")
        #             print('-'*50)
                
        #         else:
        #             print('-'*50)
        #             print("Handshake wasn't successful :(")
        #             print('-'*50)
        #         break
            
        # # transmissao da imagem em datagramas certo

        # # simulacao 3 cliente manda número de datagrama errado
        # # size = len(imgBinary[0:114]).to_bytes(1, byteorder ="big")
        # # n_comando = b'\xFF\xFF'
        # # zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        # # tail = b'\x00\x01\x02\x03'
        # # comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        # # datagramas = [comando_errado]

        # # simulacao 4 tamanho do comando enviado está errado
        # # size = len(imgBinary[0:89]).to_bytes(1, byteorder ="big")
        # # n_comando = b'\x00\x01'
        # # zeros = b'\x00\x00\x00\x00\x00\x00\x00'
        # # tail = b'\x00\x01\x02\x03'
        # # comando_errado = n_comando + size + zeros + imgBinary[0:114] + tail
        # # datagramas = [comando_errado]

        # enviados = 0
        # erros = 0
        # while enviados < len(datagramas):
        #     print('-'*50)
        #     print(f'Enviados:{enviados + 1}')
        #     print(f'Erros:{erros}')
        #     inicio_timer = time.time()
        #     txBuffer = datagramas[enviados]
        #     com1.sendData(np.asarray(txBuffer), inicio_timer)
        #     time.sleep(.27)
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

        # # inicio_timer = time.time()
        # # txBuffer = b'\x00\x00\x00\xFF\xFF\xFF\xFF\xFF\xFF\xFF\x00\x01\x02\x03'
        # # com1.sendData(np.asarray(txBuffer), inicio_timer)

        # print("-"*50)
        # print("Sucesso no envio dos dados")
        # print("-"*50)
        # com1.disable()

            

       

    # except Exception as erro:
    #     print("ops! :-\\")
    #     print(erro)
    #     com1.disable()

    
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()