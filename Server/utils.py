from re import S


def constroi_msgT2(identificador):
    # h0, h1, h2
    tipo = b'\x02\x00'

    h2 = identificador.to_bytes(1, byteorder= "big")

    h3 = b'\x00'

    h4 = b'\x00'
    h5 = b'\x00'

    h6 = b'\x01'

    # h6, h7, h8, h9
    zeros = b'\x00\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h2 + h3 + h4 + h5 + h6 + zeros + eop
    return datagrama

def constroi_msgT4(numero_ultimo_pacote):

    tipo = b'\x04\x00\x00'

    h3 = b'\x00'
    h4 = b'\x00'
    h5 = b'\x00'

    int_h6 = numero_ultimo_pacote + 1
    h6 = int_h6.to_bytes(1, byteorder="big")

    h7 = numero_ultimo_pacote.to_bytes(1, byteorder="big")

    # h8, h9
    zeros = b'\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h3 + h4 + h5 + h6 + h7 + zeros + eop
    return datagrama


def constroi_msgT5():
    # h0, h1, h2, h3
    tipo = b'\x05\x00\x00\x00'
    

    h4 = b'\x00'
    h5 = b'\x00'

    # h6, h7, h8, h9
    zeros = b'\x00\x00\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h4 + h5 + zeros + eop
    return datagrama
    

def constroi_msgT6(numero_ultimo_pacote):
    # h0, h1, h2
    tipo = b'\x06\x00\x00'
    h3 = b'\x00'

    h4 = b'\x00'
    h5 = b'\x00'

    # h6, h7, h8, h9
    int_h6 = numero_ultimo_pacote 
    int_h7 = numero_ultimo_pacote - 1
    h6 = int_h6.to_bytes(1, byteorder="big")
    h7 = int_h7.to_bytes(1, byteorder="big")
    

    zeros = b'\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h3 + h4 + h5 + h6 + h7 + zeros + eop
    return datagrama


# def constroi_log(msg, direction):
#     time = time.time()
#     tipo = msg[0]
#     size = len(msg)
#     if tipo == 3:
#         packID = msg[4]
#         len_pack = msg[3]
#         s = f"{time}/{direction}/{tipo}/{size}/{packID}/{len_pack}"
#     else:
#         s = f"{time}/{direction}/{tipo}/{size}"

#     return s

# def log(msg, direction, simulation):

#     txt = r"C:\Users\felip\Desktop\Insper 4\CFC\P3\CamadasPJ3\Server\Server{}.txt".format(simulation)
#     f = open(txt, "w")
#     f.write(constroi_log(msg,direction))
#     f.close()

#     return None