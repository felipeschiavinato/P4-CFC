from logging import exception
from socket import timeout
from utils import *
import random as rd
from enlace import *
import time
import numpy as np

#   python -m serial.tools.list_ports

serialName = "COM4"
simulation = 5

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
        timeout = com1.rx.getIsEmpty()
        if not timeout:
            rxBuffer, nRx = com1.getData(10, inicio_timer, 5)
        
        # timeout = False
        # if rxBuffer == -1:
        #     timeout = True
        
        if not timeout:
            if rxBuffer[0] == 1:
                print("Recebi uma msg tipo 1")
                rxBufferContent, nRx = com1.getData(4, inicio_timer, 5)

                log(rxBuffer+rxBufferContent, "receb", simulation)

                if rxBuffer[2] == identificador:
                    print(f"O identificador da msg:{rxBuffer[2]} é igual ao meu:{identificador}")
                    numPckg = rxBuffer[3]
                    ocioso = False
            else:
                print("Não recebi uma msg tipo 1")
                len_content = rxBuffer[5] + 4
                rxBufferContent, nRx = com1.getData(len_content, inicio_timer, 5)
                log(rxBuffer+rxBufferContent, "receb", simulation)
        else:
            print("timeout no get data")
            time.sleep(2)

    print("Nao esta mais ocioso")
    
    print("Envia msg tipo 2")
    msgT2 = constroi_msgT2(rxBuffer[2])
    com1.sendData(np.asarray(msgT2))
    log(msgT2, "envia", simulation)
    
    cont = 1
    imgBytes = b''

    com1.rx.clearBuffer()
    print("Começando a receber os pacotes")
    while cont<= numPckg:
        print("-"*50)
        print("Setando timer 1 e timer 2")
        print(f'Cont: {cont}')
        timer1 = time.time()
        timer2 = time.time()


        verifica = True
        com1.rx.clearBuffer()
        while verifica:
            inicio_timer = time.time()
            timeout = com1.rx.getIsEmpty()
            if not timeout:
                rxBuffer_head, nRx = com1.getData(10, inicio_timer, 10)
            

            # timeout = False
            # if rxBuffer_head == -1:
            #     print("timeout no get data do head")
            #     timeout = True

            # print(rxBuffer_head, len(rxBuffer_head))
            # print("Peguei o head")
            if not timeout:
                len_content = rxBuffer_head[5] + 4
            # print(f'h0: {rxBuffer_head[0]}')
            # print(f'h1: {rxBuffer_head[1]}')
            # print(f'h2: {rxBuffer_head[2]}')
            # print(f'h3: {rxBuffer_head[3]}')
            # print(f'h4: {rxBuffer_head[4]}')
            # print(f'h5: {rxBuffer_head[5]}')
            # print(f'h6: {rxBuffer_head[6]}')
            # print(f'h7: {rxBuffer_head[7]}')
            # print(f'h8: {rxBuffer_head[8]}')
            # print(f'h9: {rxBuffer_head[9]}')

            if not timeout:
                if rxBuffer_head[5] > 114:
                    print("Mensagem de erro")
                    msgT6 = constroi_msgT6(cont)
                    com1.sendData(np.asarray(msgT6))
                    break

           
            inicio_timer = time.time()
            if not timeout:
                rxBuffer_content, nRx = com1.getData(len_content, inicio_timer,5)
            
            # print("Lendo os dados")

            # timeoutContent = False
            # if rxBuffer_content == -1:
            #     print("timeout no get data do content")
            #     timeoutContent = True

            # print(rxBuffer_content)

            if not timeout:
                log(rxBuffer_head+rxBuffer_content, "receb", simulation)
                if rxBuffer_head[0]==3:
                    print("Msg tipo 3")
                    tamanho_payload = rxBuffer_head[5]
                    # print(f'eop: {rxBuffer_content[tamanho_payload:]}')
                    # print(f'rxBuffer 4: {rxBuffer_head[4]}')
                
                    if (cont == rxBuffer_head[4] and 
                        rxBuffer_content[tamanho_payload:] == b'\xAA\xBB\xCC\xDD'):
                        print("Pacote ok!")
                        imgBytes += rxBuffer_content[:tamanho_payload]
                        # print(rxBuffer_content[:tamanho_payload])
                        
                        print("Enviando msg tipo 4")
                        msgT4 = constroi_msgT4(cont)
                        com1.sendData(np.asarray(msgT4))
                        log(msgT4, "envia", simulation)

                        cont += 1
                        verifica = False
                    else:
                        print("Pacote defeituoso")
                        print("Enviando msg tipo 6")

                        msgT6 = constroi_msgT6(cont)
                        com1.sendData(np.asarray(msgT6))
                        log(msgT6, "envia", simulation)

                        verifica = False

                else:
                    time.sleep(1)

                    if (time.time() - timer2 > 20):
                        print("Timer 2 > 20 segundos")
                        ocioso = True

                        print("Enviando msg tipo 5")
                        msgT5 = constroi_msgT5()

                        inicio_timer = time.time()
                        com1.sendData(np.asarray(msgT5), inicio_timer)
                        log(msgT5, "envia", simulation)

                        print(":-(")
                        com1.disable()
                        return

                    elif (time.time() - timer1 > 2):
                        print("Timer 1 > 2 segundos")
                        print("Enviando msg tipo 6")
                        msgT6 = constroi_msgT6(cont)
                        com1.sendData(np.asarray(msgT6))
                        log(msgT6, "envia", simulation)

                        timer1 = time.time()
                        


    print("-"*50)
    print("Comunicação encerrada, escrevendo imagem")
    print("-"*50)
    imgW = r"C:\Users\paulo\Projetos_facul\CamFis\projetos\projeto4clone\P4-CFC\Server\file.jpg"
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