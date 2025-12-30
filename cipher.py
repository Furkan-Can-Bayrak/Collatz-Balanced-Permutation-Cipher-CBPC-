# cipher.py

class CollatzCipher:
    def __init__(self, seed):
        self.seed = seed

    def generate_balanced_stream(self, length):
        stream = []
        numbers = []
        n = self.seed
        needed_steps = (length // 2) + 1

        while len(stream) < needed_steps:
            if n % 2 == 0:
                n = n // 2
                stream.append(0)
            else:
                n = 3 * n + 1
                stream.append(1)
            numbers.append(n)

        balanced_bits = []
        for bit in stream:
            if bit == 0:
                balanced_bits.extend([0, 1])
            else:
                balanced_bits.extend([1, 0])

        return balanced_bits[:length], numbers

    def get_permutation_indices(self, length, numbers):
        indices = list(range(length))
        for i in range(len(indices)):
            swap_idx = numbers[i % len(numbers)] % len(indices)
            indices[i], indices[swap_idx] = indices[swap_idx], indices[i]
        return indices

    def encrypt(self, plaintext):
        binary_msg = ''.join(format(ord(c), '08b') for c in plaintext)
        bit_list = [int(b) for b in binary_msg]

        keystream, numbers = self.generate_balanced_stream(len(bit_list))
        indices = self.get_permutation_indices(len(bit_list), numbers)

        # 1. XOR
        xored_bits = [bit_list[i] ^ keystream[i] for i in range(len(bit_list))]
        # 2. Permütasyon
        encrypted_bits = [xored_bits[i] for i in indices]

        return encrypted_bits

    def decrypt(self, encrypted_bits):
        length = len(encrypted_bits)
        keystream, numbers = self.generate_balanced_stream(length)
        indices = self.get_permutation_indices(length, numbers)

        # 1. Ters Permütasyon
        xored_bits = [0] * length
        for i, original_pos in enumerate(indices):
            xored_bits[original_pos] = encrypted_bits[i]

        # 2. XOR
        original_bits = [xored_bits[i] ^ keystream[i] for i in range(length)]

        bit_str = ''.join(map(str, original_bits))
        chars = [chr(int(bit_str[i:i + 8], 2)) for i in range(0, len(bit_str), 8)]
        return ''.join(chars)