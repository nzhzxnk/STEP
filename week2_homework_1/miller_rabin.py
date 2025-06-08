import random
def find_prime(number):
        if number <= 2:
            return 2
        # adjust if number is not odd.
        if number % 2 == 0:
            n = number+1
        else:
            n = number
        # return n if MillerRabin == True
        while True:
            if miller_rabin(n,k=5):
                return n
            else:
                n += 2

def miller_rabin(n,k=5):
        # exclude non-prime numbers.
        if n == 1:
            return False
        if n == 2 or n == 3:
            return True
        if n % 2 == 0:
            return False
        # find d and s. (n-1 = 2^s * d)
        d = n-1
        s = 0
        while d%2 == 0:
            d //= 2
            s += 1
        # Run the test k times.
        for _ in range(k):
            # Question: Why doesn't need "random.seed(n)"??
            # Question: (2,n-1) is 2 <= random <= n-1 ??
            a = random.randint(2,n-1)
            x = pow(a,d,n)
            if x == 1 or x == n-1:
                continue
            maybe_prime = False
            for _ in range(s-1):
                x = pow(x,2,n)
                if x == n-1:
                    maybe_prime = True
                    break
                if x == 1:
                    return False
            if not maybe_prime:
                return False
        return True

print(find_prime(200))