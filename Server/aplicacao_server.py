from logging import exception
from utils import *
import random as rd
from enlace import *
import time
import numpy as np

#   python -m serial.tools.list_ports

serialName = "COM11"
simulation = 1

def main():
    identificador = 1
    com1 = enlace(serialName)
    com1.enable()

    print("Comunication open")
    print("Reception is about to start")
    print("Waiting for data")

    ocioso = True

    while ocioso:
        inicio_timer = time.time()
        rxBuffer, nRx = com1.getData(10, inicio_timer, 5)
        
        if rxBuffer[0] == 1:
            rxBufferContent, nRx = com1.getData(4, inicio_timer, 5)

            log(rxBuffer+rxBufferContent, "receb", simulation)

            if rxBuffer[2] == identificador:
                numPckg = rxBuffer[3]
                ocioso = False
        else:
            len_content = rxBuffer[5] + 4
            rxBufferContent, nRx = com1.getData(len_content, inicio_timer, 5)
            log(rxBuffer+rxBufferContent, "receb", simulation)

    print("Nao esta mais ocioso")
                
    msgT2 = constroi_msgT2(rxBuffer[2])
    com1.sendData(np.asarray(msgT2))
    log(msgT2, "envia", simulation)
    
    cont = 1
    imgBytes = b''

    while cont<= numPckg:
        timer1 = time.time()
        timer2 = time.time()


        verifica = True
        while verifica:

            inicio_timer = time.time()
            rxBuffer_head, nRx = com1.getData(10, inicio_timer, 5)
            len_content = rxBuffer[5] + 4
            inicio_timer = time.time()
            rxBuffer_content, nRx = com1.getData(len_content, inicio_timer, 2)
            log(rxBuffer_head+rxBuffer_content, "receb", simulation)

            if rxBuffer_head[0]==3:
                tamanho_payload = rxBuffer_head[5]
                if (cont == rxBuffer_head[4] and 
                    rxBuffer_content[tamanho_payload-4:] == b'\xAA\xBB\xCC\xDD'):

                    imgBytes += rxBuffer_content[:tamanho_payload-4]
                    
                    msgT4 = controi_msgT4(cont)
                    com1.sendData(np.asarray(msgT4))
                    log(msgT4, "envia", simulation)

                    cont += 1
                    verifica = False
                else:
                    msgT6 = constroi_msgT6(cont)
                    com1.sendData(np.asarray(msgT6))
                    log(msgT6, "envia", simulation)

            else:
                time.sleep(1)

                if (time.time() - timer2 > 20):
                    ocioso = True

                    msgT5 = constroi_msgT5()

                    inicio_timer = time.time()
                    com1.sendData(np.asarray(msgT5), inicio_timer)
                    log(msgT5, "envia", simulation)

                    print(":-(")
                    com1.disable()
                    return

                elif (time.time() - timer1 > 2):
                    msgT4 = controi_msgT4(cont)
                    com1.sendData(np.asarray(msgT4))
                    log(msgT4, "envia", simulation)

                    timer1 = time.time()








    print("-"*50)
    print("Comunicação encerrada, escrevendo imagem")
    print("-"*50)
    imgW = r"C:\Users\felip\Desktop\Insper 4\CFC\P3\CamadasPJ3\Server\file.jpg"
    f = open(imgW, "wb")
    f.write(imgBytes)
    f.close()
    print("SUCESSO!")

    com1.disable()
    



            

            
        

        # tempo_inicial = time.time()
        # #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # #para declarar esse objeto é o nome da porta.
        # com1 = enlace(serialName)
        
    
        # # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        # com1.enable()
        # #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        # print("Comunication open")
        
        # #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        # #Observe o que faz a rotina dentro do thread RX
        # #print um aviso de que a recepção vai começar.

        # print("Reception is about to start")
        
        # #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        # #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        # #acesso aos bytes recebidos
        # print("Waiting for data")

        # # simulacao 2, servidor nao pronto para receber dados
        # #time.sleep(30)
        # timer = time.time()
        # rxBuffer_handshakehead, nRx = com1.getData(10, timer, 10)
        # lenComando = rxBuffer_handshakehead[2] + 4

        # timer = time.time()
        # rxBuffer_handshakeContent, nRx = com1.getData(lenComando, timer, 10)

        # txBuffer = rxBuffer_handshakehead + rxBuffer_handshakeContent
        # com1.sendData(np.asarray(txBuffer))
        # print("Handshake was sent")

        # imgBytes = b''

        # n_comando = 1
        # while True:
        #     timer = time.time()
        #     print('-'*50)
        #     print(f'N comando:{n_comando}')
        #     rxBuffer_head, nRx = com1.getData(10, timer, 6)

        #     n_comandoBytes = n_comando.to_bytes(2, byteorder="big")

        #     if rxBuffer_head == -1:
        #         com1.disable()
        #         print('-'*50)
        #         print("Erro ao receber dados")
        #         print('-'*50)
        #         return
            
        #     lenComando = rxBuffer_head[2] + 4
        #     rxBuffer_Content, nRx = com1.getData(lenComando, timer, 6)
            
        #     if rxBuffer_Content == -1:
        #         com1.disable()
        #         print('-'*50)
        #         print("Erro ao receber dados")
        #         print('-'*50)
        #         return
            
        #     if rxBuffer_head[:2] == rxBuffer_head[3:5] and rxBuffer_Content[lenComando-4:lenComando] == b'\x00\x01\x02\x03':
        #         print(f'Mandando {n_comandoBytes}')
        #         com1.sendData(np.asarray(n_comandoBytes))
        #         time.sleep(.05)
        #         print("Comando final")
        #         break

        #     print(f'buffer head {rxBuffer_head[:2]}')
        #     if (rxBuffer_head[:2] == n_comando.to_bytes(2, byteorder="big")
        #         and rxBuffer_Content[lenComando-4:lenComando] == b'\x00\x01\x02\x03'): 
        #         imgBytes += rxBuffer_Content[:lenComando-4]
            
        #         n_comando += 1
        #     else:
        #         n_comandoBytes = b'\x00\x00'

        #     print(f'Mandando {n_comandoBytes}')
        #     com1.sendData(np.asarray(n_comandoBytes))
        #     time.sleep(.05)

            


        # print("-"*50)
        # print("Comunicação encerrada, escrevendo imagem")
        # print("-"*50)
        # imgW = r"C:\Users\felip\Desktop\Insper 4\CFC\P3\CamadasPJ3\Server\file.jpg"
        # f = open(imgW, "wb")
        # f.write(imgBytes)
        # f.close()

        # com1.disable()

        

    # except Exception as erro:
    #     print("ops! :-\\")
    #     print(erro)
    #     com1.disable()

if __name__ == "__main__":
    main()