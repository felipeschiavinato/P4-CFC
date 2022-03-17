from logging import exception
import random as rd
from enlace import *
import time
import numpy as np

#   python -m serial.tools.list_ports

serialName = "COM7"

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
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        print("Reception is about to start")
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        print("Waiting for data")

        # simulacao 2, servidor nao pronto para receber dados
        #time.sleep(30)
        timer = time.time()
        rxBuffer_handshakehead, nRx = com1.getData(10, timer, 10)
        lenComando = rxBuffer_handshakehead[2] + 4

        timer = time.time()
        rxBuffer_handshakeContent, nRx = com1.getData(lenComando, timer, 10)

        txBuffer = rxBuffer_handshakehead + rxBuffer_handshakeContent
        com1.sendData(np.asarray(txBuffer))
        print("Handshake was sent")

        imgBytes = b''

        n_comando = 1
        while True:
            timer = time.time()
            print('-'*50)
            print(f'N comando:{n_comando}')
            rxBuffer_head, nRx = com1.getData(10, timer, 6)

            n_comandoBytes = n_comando.to_bytes(2, byteorder="big")

            if rxBuffer_head == -1:
                com1.disable()
                print('-'*50)
                print("Erro ao receber dados")
                print('-'*50)
                return
            
            lenComando = rxBuffer_head[2] + 4
            rxBuffer_Content, nRx = com1.getData(lenComando, timer, 6)
            
            if rxBuffer_Content == -1:
                com1.disable()
                print('-'*50)
                print("Erro ao receber dados")
                print('-'*50)
                return
            
            if rxBuffer_head[:2] == rxBuffer_head[3:5] and rxBuffer_Content[lenComando-4:lenComando] == b'\x00\x01\x02\x03':
                print(f'Mandando {n_comandoBytes}')
                com1.sendData(np.asarray(n_comandoBytes))
                time.sleep(.05)
                print("Comando final")
                break

            print(f'buffer head {rxBuffer_head[:2]}')
            if (rxBuffer_head[:2] == n_comando.to_bytes(2, byteorder="big")
                and rxBuffer_Content[lenComando-4:lenComando] == b'\x00\x01\x02\x03'): 
                imgBytes += rxBuffer_Content[:lenComando-4]
            
                n_comando += 1
            else:
                n_comandoBytes = b'\x00\x00'

            print(f'Mandando {n_comandoBytes}')
            com1.sendData(np.asarray(n_comandoBytes))
            time.sleep(.05)

            


        print("-"*50)
        print("Comunicação encerrada, escrevendo imagem")
        print("-"*50)
        imgW = r"C:\Users\felip\Desktop\Insper 4\CFC\P3\CamadasPJ3\Server\file.jpg"
        f = open(imgW, "wb")
        f.write(imgBytes)
        f.close()

        com1.disable()

        

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()

if __name__ == "__main__":
    main()