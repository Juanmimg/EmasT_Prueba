from collections import Counter #Cuenta cuantas veces aparece cada elemento en un iterable
 
# ----------------------------
# Reto 1: Ordenar arreglo por frecuencia descendente y valor ascendente
# ----------------------------
def ordenar_por_frecuencia(nums):
    conteo = Counter(nums)
    return sorted(nums, key=lambda x: (-conteo[x], x))

# ----------------------------
# Reto 3: Primer carácter no repetido (ignorar espacios y case-insensitive)
# ----------------------------
def primer_no_repetido(texto):
    texto_limpio = texto.replace(" ", "").lower()
    conteo = Counter(texto_limpio)
    for i, char in enumerate(texto):
        if char != " " and conteo[char.lower()] == 1:
            return i  # posición del primer caracter único
    return -1  # si no hay


if __name__ == "__main__":
    # Reto 1
    nums = [4, 6, 2, 2, 6, 4, 4, 4, 3]
    print("Reto 1:", ordenar_por_frecuencia(nums))

    # Reto 3
    texto = "Abzb aCad"
    print("Reto 3:", primer_no_repetido(texto))
