def coin_probability(target_heads, condition):
    outcomes = [(c1, c2, c3) for c1 in ['H', 'T'] for c2 in ['H', 'T'] for c3 in ['H', 'T']]
    total = len(outcomes)
    favorable = 0

    for c1, c2, c3 in outcomes:
        heads = [c1, c2, c3].count('H')

        if condition == "equal" and heads == target_heads:
            favorable += 1
        elif condition == "greater" and heads > target_heads:
            favorable += 1
        elif condition == "less" and heads < target_heads:
            favorable += 1

    print("Probability:", favorable / total)


def bayes_coins():
    cond = input("Condition: ")
    target = int(input("Target heads: "))
    first = input("First flip (H/T): ")

    count_b = 0
    count_ab = 0

    for c1 in ['H', 'T']:
        for c2 in ['H', 'T']:
            for c3 in ['H', 'T']:
                heads = [c1, c2, c3].count('H')

                A = (heads == target)
                B = (c1 == first)

                if B:
                    count_b += 1
                    if A:
                        count_ab += 1

    if count_b != 0:
        print("P(A|B):", count_ab / count_b)


def joint_inference():
    table = [[float(input()) for _ in range(2)] for _ in range(2)]

    print("Marginal C1:", [sum(row) for row in table])
    print("Marginal C2:", [sum(table[i][j] for i in range(2)) for j in range(2)])


mode = input("1.Basic 2.Bayes 3.Joint: ")

if mode == "1":
    coin_probability(int(input()), input())
elif mode == "2":
    bayes_coins()
else:
    joint_inference()
