from pulp import LpProblem, LpMaximize, LpVariable, lpSum, GLPK, LpInteger, value
import time

def maximize_profit(num_toys, num_specials, max_toys, toys, specials, toy_vars, special_vars, profit, totalToys):
    # Create the maximization problem
    prob = LpProblem("Maximize_Profit", LpMaximize)

    # Add the objective function
    prob += profit, "Profit"

    # Add the capacity constraint
    prob += totalToys <= max_toys, "Capacity"

    for i in range(num_toys):
        prob += toy_vars[i] <= toys[i][1], f"Toy_Limit_{i}"

    # Solve the problem
    prob.solve(GLPK(msg=0))

    # Retrieve the optimal values
    result = int(prob.objective.value())
        

    return result

def read_input():
    profit = 0
    totalToys = 0
    num_toys, num_specials, max_toys = map(int, input().split())
    toys, specials = [], []
    toy_vars = []
    special_vars = []

    for i in range(num_toys):
        toys.append([int(j) for j in input().split()])
        toy_vars.append(LpVariable(f"Toy_{i}", lowBound=0, upBound=toys[i][1], cat=LpInteger))
        profit += lpSum(toys[i][0] * toy_vars[i])
        totalToys += lpSum(toy_vars[i])

    for i in range(num_specials):
        specials.append([int(j) for j in input().split()])
        toys1 = value(toys[specials[i][0] - 1][1])
        toys2 = value(toys[specials[i][1] - 1][1])
        toys3 = value(toys[specials[i][2] - 1][1])
        zecarlos = min(toys1, toys2, toys3)

        special_vars.append(LpVariable(f"Special_{i}", lowBound=0, upBound = zecarlos, cat=LpInteger))
        profit += lpSum(specials[i][3] * special_vars[i])
        totalToys += lpSum(special_vars[i]) * 3
        toy_vars[specials[i][0] - 1] += special_vars[i]
        toy_vars[specials[i][1] - 1] += special_vars[i]
        toy_vars[specials[i][2] - 1] += special_vars[i]

    return num_toys, num_specials, max_toys, toys, specials, toy_vars, special_vars, profit, totalToys

if __name__ == "__main__":
    # Registra o tempo de início
    start_time = time.time()

    # Reading the input
    num_toys, num_specials, max_toys, toys, specials, toy_vars, special_vars, profit, totalToys = read_input()

    # Calling the function to maximize profit
    result = maximize_profit(num_toys, num_specials, max_toys, toys, specials, toy_vars, special_vars, profit, totalToys)

    # Registra o tempo de término
    end_time = time.time()

    # Calcula e imprime o tempo de execução
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")

    # Print the result
    print(result)