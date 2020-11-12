"""viết hàm in ra các số nguyên tố"""

import math as m

def nguyento(known_primes=[1]):
    print(1)
    i = 1
    while True:
        i += 1
        is_prime = True
        for check in range(2, int(m.sqrt(i))+1):
            if i % check == 0:
                is_prime = False
                break
        if not is_prime:
            continue
        else:
            print(i)
            known_primes.append(i)

