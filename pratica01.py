from multiprocessing import Process, Pipe
import time
import random

INTERVALO_INI_PROD = 1
INTERVALO_FIM_PROD = 2
INTERVALO_INI_CONS = 1
INTERVALO_FIM_CONS = 2

inicio = time.time()

def produtor(conn):
    for i in range(3):
        send_start = time.time()
        print(f"[\33[92m{send_start - inicio:.4f}s\33[0m] Produtor iniciou produção do item {i}")
        time.sleep(random.uniform(INTERVALO_FIM_PROD, INTERVALO_FIM_PROD))
        send_end = time.time()
        print(f"[\33[92m{send_end - inicio:.4f}s\33[0m] Produtor finalizou produção do item {i} - \33[92mTempo de produção: {send_end - send_start:.2f} segundos\33[0m")
        conn.send(i)

    send_finalizacao = time.time()
    print(f"[\33[92m{send_finalizacao - inicio:.4f}s\33[0m] Produtor enviou sinal de finalização")
    conn.send('fim')
    conn.close()


def consumidor(conn):
    while True:
        produto = conn.recv()

        if produto == 'fim':
            recv_finalizacao = time.time()
            print(f"[\33[92m{recv_finalizacao - inicio:.4f}s\33[0m] Consumidor recebeu sinal de finalização")
            break

        recv_start = time.time()
        print(f"[\33[92m{recv_start - inicio:.4f}s\33[0m] Consumidor recebeu o item {produto}")

        time.sleep(random.uniform(INTERVALO_INI_CONS, INTERVALO_FIM_CONS))
        recv_end = time.time()
        print(f"[\33[92m{recv_end - inicio:.4f}s\33[0m] Consumidor finalizou consumo do item {produto} - \33[92mTempo de consumo: {recv_end - recv_start:.2f} segundos\33[0m")


if __name__ == '__main__':
    prod_conn, cons_conn = Pipe()

    proc_prod = Process(target=produtor, args=(prod_conn,))
    proc_cons = Process(target=consumidor, args=(cons_conn,))
    
    proc_prod.start()
    proc_cons.start()

    proc_prod.join()
    proc_cons.join()

    print("Processos finalizados.")
