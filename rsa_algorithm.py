import random
import time


def euclidean(num1, num2):
    while num2 != 0:
        num1, num2 = num2, num1 % num2

    return num1


def extended_euclidean(num1, num2):
    (x0, y0, x, y) = (1, 0, 0, 1)
    n = 1
    while num1 % num2:
        (x0, y0, x, y) = (x, y, x0 + x*(num1//num2), y0 + y*(num1//num2))
        num1, num2 = num2, num1 % num2 
        n += 1

    return (num2, x * (-1)**n, y * (-1)**(n+1))



def fme(number, exponent, modulus):
    szorzat = 1
    b = number
    for i in "{0:b}".format(exponent)[::-1]:
        if int(i):
            szorzat *= b
        b = b**2 % modulus

    return szorzat % modulus


def miller_rabin(number):
    (a, s, p) = (2, 0, number-1)
    while not p % 2:
        s += 1
        p = p // 2

    elso = fme(a, p, number)
    if elso == 1 or elso == number-1:
        return True

    for _ in range(1, s):
        elso = (elso ** 2) % number
        if elso == number-1:
            return True
    
    return False


def generate_random_prime():
    random_szam2 = random.randrange(1000, 1500) 
    i = 2**random_szam2 +1
    while True:
        if miller_rabin(i):
            return i
        else:
            i += 2


def generate_keys(prime1, prime2):
    n = prime1 * prime2
    fi_n = (prime1-1) * (prime2-1)
    e = 0
    for i in range(2, 5000):
        if euclidean(fi_n, i) == 1:
            e = i
            break

    return((n, e), (n, extended_euclidean(fi_n, e)[2] % fi_n))


def encrypt(message, public_key):
    return fme(message, public_key[1], public_key[0])


def fme_decrypt(encrypted_message, private_key):
    return fme(encrypted_message, private_key[1], private_key[0])


def chinese_remainder_decrypt(encrypted_message, private_key, prime1, prime2):
    c1, c2 = fme(encrypted_message, (private_key[1] % (prime2-1)), prime2), fme(encrypted_message, (private_key[1] % (prime1-1)), prime1)
    x1, x2 = extended_euclidean(prime1, prime2)[1:]

    return (c1*prime1*x1 + c2*prime2*x2) % private_key[0]


def main():
    start = time.time()
    gyors = time.time()
    prime1, prime2 = generate_random_prime(), generate_random_prime()
    print("Első prím:", prime1)
    print()
    print("Második prím:", prime2)
    print("Generálási idő:", time.time()-gyors)
    print()
    gyors = time.time()
    public_key, private_key = generate_keys(prime1, prime2)
    titkos = encrypt(124125426582348273569235872938, public_key)
    print(f"Publikus kulcspár: {public_key}")
    print()
    print(f"Privát kulcspár: {private_key}")
    print("Eltelt idő:", time.time()-gyors)
    print()
    gyors = time.time()
    print(f"Titkosított üzenet: {titkos}")
    print("Eltelt idő:", time.time()-gyors)
    print()
    gyors = time.time()
    print(f"Visszafejtett üzenet gyorshatványozással: {fme_decrypt(titkos, private_key)}")
    print("Eltelt idő:", time.time()-gyors)
    print()
    gyors = time.time()
    print(f"Visszafejtett üzenet kínai maradéktétellel: {chinese_remainder_decrypt(titkos, private_key, prime1, prime2)}")
    print("Eltelt idő:", time.time()-gyors)
    print()
    print("Összes eltelt idő:", time.time()-start)


##########################


if __name__ == "__main__":
    main()