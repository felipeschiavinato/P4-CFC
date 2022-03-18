from struct import pack


def constroi_datagramas(imgBinary):
    datagramas = []
    lenB = len(imgBinary)

    len_datagramas = lenB/114 if lenB % 114 == 0 else int(lenB/114) + 1
    computado = 0

    numero = 1
    i = 0
    while computado <= lenB:
        j = i + 114
        if j > lenB:
            j = lenB
        
        
        # h0, h1, h2
        tipo = b'\x03\x00\x00'

        # h3, h4, h5
        h3 = len_datagramas.to_bytes(1, byteorder = "big")
        id_datagrama = numero.to_bytes(1, byteorder ="big")
        len_payload = len(imgBinary[i:j]).to_bytes(1, byteorder ="big")

        # h6, h7, h8, h9
        zeros = b'\x00\x00\x00\x00'
        
        EOP = b'\xAA\xBB\xCC\xDD'
        payload = tipo + h3 + id_datagrama + len_payload + zeros + imgBinary[i:j] + EOP
        
        # print(comando)
        # print(len(comando))
        # print(comando[0:2])
        # print(comando[2])
        # break
        datagramas.append(payload)
        i += 114
        numero += 1
        computado += 114

    return datagramas

def constroi_handshake(identificador, size_datagrama):
    # h0, h1, h2
    tipo = b'\x01\x00'
    h2 = identificador.to_bytes(1, byteorder= "big")
    h3 = size_datagrama.to_bytes(1, byteorder = "big")

    h4 = b'\x00'
    h5 = b'\xAB'

    # h6, h7, h8, h9
    zeros = b'\x00\x00\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h2 + h3 + h4 + h5 + zeros + eop
    return datagrama

def constroi_msgT5(size_datagrama):
    # h0, h1, h2
    tipo = b'\x05\x00\x00'
    h3 = size_datagrama.to_bytes(1, byteorder = "big")

    h4 = b'\x00'
    h5 = b'\x00'

    # h6, h7, h8, h9
    zeros = b'\x00\x00\x00\x00'
    eop = b'\xAA\xBB\xCC\xDD'

    datagrama = tipo + h3 + h4 + h5 + zeros + eop
    return datagrama

def constroi_log(msg, direction):
    time = time.time()
    tipo = msg[0]
    size = len(msg)
    if tipo == 3:
        packID = msg[4]
        len_pack = msg[3]
        s = f"{time}/{direction}/{tipo}/{size}/{packID}/{len_pack}"
    else:
        s = f"{time}/{direction}/{tipo}/{size}"

    return s
    
def log(msg, direction, simulation):
    
    txt = r"C:\Users\felip\Desktop\Insper 4\CFC\P3\CamadasPJ3\Server\Client{}.txt".format(simulation)
    f = open(txt, "w")
    f.write(constroi_log(msg,direction))
    f.close()

    return None

    
