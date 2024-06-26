# -*- coding: utf-8 -*-
"""Ad_Scheduling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1979Px40KhHeSBNV6kd9i62OVnnSqbkrV
"""

!pip install pulp

!pip install pyqubo

!pip install dwave-neal

from pulp import LpVariable, LpMinimize, LpProblem, LpBinary

# Sample Data
M = 4
N = 4
S = [[0, 1, 0,1], [1, 0, 1,0],[1,0,0,1], [0, 1, 0,1]]  # Similarity matrix

prob = LpProblem("AdScheduling", LpMinimize)

# Define Decision Variables
x = LpVariable.dicts("x", (range(M), range(N)), cat='Binary')
y = LpVariable.dicts("y", (range(M), range(M), range(N)), cat='Binary')

# Objective Function
objective = sum(S[i][k] * y[i][k][j] for i in range(M) for k in range(M) for j in range(N))
prob += objective

# Constraints:
for i in range(M):
    for k in range(M):
        for j in range(N):
            prob += y[i][k][j] <= x[i][j]#in one slot we cannot have 2 ads
            prob += y[i][k][j] <= x[k][j]#iin 1 ad cannot be repeated in multiple slot at same time
            prob += y[i][k][j] >= x[i][j] + x[k][j] - 1#no repeatation in one slot
            prob += y[i][k][j] != x[i][i] or x[j][j] or x[k][k]

for i in range(M):
    prob += sum(x[i][j] for j in range(N)) == 1

prob.solve()


for i in range(M):
    for j in range(N):
        if x[i][j].value() == 1:
            print(f"Advertisement {i} is scheduled in slot {j}")
arr = []
for i in range(M):
    for j in range(N):
        #x[i][j].value().int
        arr.append(x[i][j].value())
        ## x[0][1] = 1
print(arr)

from pyqubo import Array
from neal import SimulatedAnnealingSampler

# Sample Data
M = 4  # Number of advertisements
N = 5  # Number of ad slots in a break
S = [[0, 1, 0,1], [1, 0, 1,0],[1,0,0,1], [0, 1, 0,1]]

x = Array.create('x', shape=(M, N), vartype="BINARY")

# Objective Function:
objective = sum(S[i][k] * x[i][j] * x[k][j] for i in range(M) for k in range(M) for j in range(N))

constraints = [sum(x[i][j] for j in range(N)) - 1 for i in range(M)]

H = objective + sum(constraint**2 for constraint in constraints)

model = H.compile()
qubo, offset = model.to_qubo()

sampler = SimulatedAnnealingSampler()
response = sampler.sample_qubo(qubo)
solution = response.first.sample

decoded_solution = model.decode_sample(solution, vartype="BINARY")

print(decoded_solution)

for i in range(M):
    for j in range(N):
        if decoded_solution.array('x', (i, j)) == 1:
            print(f"Advertisement {i} is scheduled in slot {j}")

from pyqubo import Array
from neal import SimulatedAnnealingSampler

# Sample data
ads = [
    {"name": "ZARA", "duration": 15, "time": "06:18:45"},
    {"name": "H&M", "duration": 15, "time": "06:07:35"},
    {"name": "Levis", "duration": 10, "time": "06:19:35"},
    {"name": "Rupa frontline", "duration": 10, "time": "06:08:40"},
    {"name": "J&J", "duration": 10, "time": "06:19:05"},
    {"name": "Fuaark", "duration": 10, "time": "06:08:30"}
]

M = len(ads)
N = len(set(ad["time"] for ad in ads)


       )

S = [[1 if ads[i]["name"] == ads[j]["name"] and i != j else 0 for j in range(M)] for i in range(M)]

x = Array.create('x', shape=(M, N), vartype="BINARY")

# Objective Function:
objective = sum(S[i][k] * x[i][j] * x[k][j] for i in range(M) for k in range(M) for j in range(N))

constraints = [sum(x[i][j] for j in range(N)) - 1 for i in range(M)]

H = objective + sum(constraint**2 for constraint in constraints)

model = H.compile()
qubo, offset = model.to_qubo()

sampler = SimulatedAnnealingSampler()
response = sampler.sample_qubo(qubo)
solution = response.first.sample

decoded_solution = model.decode_sample(solution, vartype="BINARY")

for i in range(M):
    for j in range(N):
        if decoded_solution.array('x', (i, j)) == 1:
            print(f"Advertisement '{ads[i]['name']}' scheduled at {ads[i]['time']} is placed in slot {j}")

# Extracting relevant data from the provided dataset
ads = [
    {"product": "ZARA", "duration": 15, "time": "06:18:45"},
    {"product": "H&M", "duration": 15, "time": "06:07:35"},
    {"product": "Levis", "duration": 10, "time": "06:19:35"},
    {"product": "Rupa frontline", "duration": 10, "time": "06:08:40"},
    {"product": "J&J", "duration": 10, "time": "06:19:05"},
    {"product": "Fuaark", "duration": 10, "time": "06:08:30"}
]

from pyqubo import Array
from neal import SimulatedAnnealingSampler

M = len(ads)
N = len(set(ad["time"] for ad in ads))

S = [[1 if ads[i]["product"] == ads[j]["product"] and i != j else 0 for j in range(M)] for i in range(M)]

x = Array.create('x', shape=(M, N), vartype="BINARY")
objective = sum(S[i][k] * x[i][j] * x[k][j] for i in range(M) for k in range(M) for j in range(N))

constraints = [sum(x[i][j] for j in range(N)) - 1 for i in range(M)]


H = objective + sum(constraint**2 for constraint in constraints)

model = H.compile()
qubo, offset = model.to_qubo()

sampler = SimulatedAnnealingSampler()
response = sampler.sample_qubo(qubo)
solution = response.first.sample

decoded_solution = model.decode_sample(solution, vartype="BINARY")

for i in range(M):
    for j in range(N):
        if decoded_solution.array('x', (i, j)) == 1:
            print(f"Advertisement for product '{ads[i]['product']}' scheduled at {ads[i]['time']} is placed in slot {j}")

from pyqubo import Array
from neal import SimulatedAnnealingSampler

# Sample Data
M = 4  # Number of advertisements
N = 4  # Number of ad slots in a break
S = [[0, 1, 0,1], [1, 0, 1,0],[1,0,0,1], [0, 1, 0,1]]

x = Array.create('x', shape=(M, N), vartype="BINARY")

# Objective Function:
objective = sum(S[i][k] * x[i][j] * x[k][j] for i in range(M) for k in range(M) for j in range(N))

constraints = [sum(x[i][j] for j in range(N)) - 1 for i in range(M)]

H = objective + sum(constraint**2 for constraint in constraints)

model = H.compile()
qubo, offset = model.to_qubo()
print(qubo)

sampler = SimulatedAnnealingSampler()
response = sampler.sample_qubo(qubo)
solution = response.first.sample

decoded_solution = model.decode_sample(solution, vartype="BINARY")

for i in range(M):
    for j in range(N):
        if decoded_solution.array('x', (i, j)) == 1:
            print(f"Advertisement {i} is scheduled in slot {j}")

print (decoded_solution)
print (solution)

pip install qiskit==0.46.0

pip install qiskit-optimization

import qiskit

qiskit.__qiskit_version__

import numpy as np
import copy
import qiskit_algorithms

# Problem modelling imports
from docplex.mp.model import Model

import qiskit_algorithms

# Qiskit imports
from qiskit_algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.primitives import Sampler
from qiskit.utils.algorithm_globals import algorithm_globals
from qiskit_optimization.algorithms import MinimumEigenOptimizer, CplexOptimizer
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.problems.variable import VarType
from qiskit_optimization.converters.quadratic_program_to_qubo import QuadraticProgramToQubo
from qiskit_optimization.translators import from_docplex_mp
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import CplexOptimizer

import numpy as np
def create_problem(s, M: int = 3, N: int = 5):
    """Solve the quadratic program using docplex."""

    mdl = Model()
    x = [[mdl.binary_var(f"x{i}_{j}") for j in range(len(s))] for i in range(len(s))]

    # Define the objective and constraints
    objective = mdl.sum(s[i][k] * x[i][j] * x[k][j] for i in range(len(s)) for k in range(len(s)) for j in range(len(s)))
    constraints = [mdl.sum(x[i][j] for j in range(len(s))) == 1 for i in range(len(s))]

    # Add objective and constraints to the model
    mdl.minimize(objective)
    mdl.add_constraints(constraints)

    qp = from_docplex_mp(mdl)
    return qp


def relax_problem(problem):
    """Change all variables to continuous."""
    relaxed_problem = copy.deepcopy(problem)
    for variable in relaxed_problem.variables:
        variable.vartype = VarType.CONTINUOUS

    return relaxed_problem

M = 4  # Number of advertisements
N = 4  # Number of ad slots in a break
S = [[0, 1, 0,1], [1, 0, 1,0],[1,0,0,1], [0, 1, 0,1]]
s = np.array(S)

qubo = create_problem(s, M, N)
print(qubo.prettyprint())

from qiskit_optimization.translators import from_docplex_mp
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import CplexOptimizer

qubo = create_problem(s, M, N)
print(qubo.prettyprint())

pip install cplex

!pip install qiskit-optimization[cplex]

print(arr)

from qiskit.algorithms.optimizers import COBYLA

optimizer = COBYLA()

qp = relax_problem(QuadraticProgramToQubo().convert(qubo))
print(qp.prettyprint())

from qiskit_optimization.converters import QuadraticProgramToQubo

qp2qubo = QuadraticProgramToQubo()
qubo = qp2qubo.convert(qubo)
print(qubo.prettyprint())
op, offset = qubo.to_ising()
print("offfset is ", offset)
#qubit_hamiltonian = op

pip install pylatexenc

pip install matplotlib

!pip install pylatexenc

import pylatexenc

from qiskit import QuantumCircuit
from qiskit.circuit.library import QAOAAnsatz

qubit_hamiltonian = op
qaoa_ansatz = QAOAAnsatz(cost_operator=qubit_hamiltonian, reps=1, initial_state=None, mixer_operator=None, name='QAOA')
qaoa_ansatz.decompose().decompose().decompose().draw(output='mpl', scale=1.0, fold=-10, style = "iqp")

import numpy as np
import copy
from docplex.mp.model import Model
from qiskit.algorithms.optimizers import COBYLA
from qiskit.algorithms.minimum_eigensolvers import QAOA, NumPyMinimumEigensolver
from qiskit_optimization.algorithms import MinimumEigenOptimizer, CplexOptimizer
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.problems.variable import VarType
from qiskit_optimization.translators import from_docplex_mp

# Define a function to create the quadratic program using DOcplex
def create_problem(mu: np.array, sigma: np.array, total: int = 3) -> QuadraticProgram:
    mdl = Model()
    x = [mdl.binary_var(f"x{i}") for i in range(len(sigma))]

    objective = mdl.sum([mu[i] * x[i] for i in range(len(mu))])
    objective -= 2 * mdl.sum([sigma[i, j] * x[i] * x[j] for i in range(len(mu)) for j in range(len(mu))])
    mdl.maximize(objective)

    cost = mdl.sum(x)
    mdl.add_constraint(cost == total)

    qp = from_docplex_mp(mdl)
    return qp

# Define a function to relax the problem by changing variables to continuous
def relax_problem(problem) -> QuadraticProgram:
    relaxed_problem = copy.deepcopy(problem)
    for variable in relaxed_problem.variables:
        variable.vartype = VarType.CONTINUOUS

    return relaxed_problem

# Main execution
mu = np.array([3.418, 2.0913, 6.2415, 4.4436, 10.892, 3.4051])
sigma = np.array([[1.07978412, 0.00768914, 0.11227606, -0.06842969, -0.01016793, -0.00839765],
                   [0.00768914, 0.10922887, -0.03043424, -0.0020045, 0.00670929, 0.0147937],
                   [0.11227606, -0.03043424, 0.985353, 0.02307313, -0.05249785, 0.00904119],
                   [-0.06842969, -0.0020045, 0.02307313, 0.6043817, 0.03740115, -0.00945322],
                   [-0.01016793, 0.00670929, -0.05249785, 0.03740115, 0.79839634, 0.07616951],
                   [-0.00839765, 0.0147937, 0.00904119, -0.00945322, 0.07616951, 1.08464544]])

# Create the original binary problem
qubo = create_problem(mu, sigma)
print("Original Binary Problem:")
print(qubo.prettyprint())

# Solve the original binary problem classically
result = CplexOptimizer().solve(qubo)
print("\nClassical Solution to Binary Problem:")
print(result.prettyprint())

# Relax the problem by changing variables to continuous
relaxed_qubo = relax_problem(QuadraticProgramToQubo().convert(qubo))
print("\nRelaxed Continuous Problem:")
print(relaxed_qubo.prettyprint())

# Solve the relaxed continuous problem classically
sol = CplexOptimizer().solve(relaxed_qubo)
print("\nClassical Solution to Relaxed Continuous Problem:")
print(sol.prettyprint())

# Use the solution to the relaxed problem to warm-start QAOA
thetas = [2 * np.arcsin(np.sqrt(c_star)) for c_star in sol.samples[0].x]
init_qc = QuantumCircuit(len(sigma))
for idx, theta in enumerate(thetas):
    init_qc.ry(theta, idx)

# Apply QAOA to the original binary problem with warm-start
qaoa_mes = QAOA(sampler=Sampler(), optimizer=COBYLA(), initial_point=[0.0, 1.0])
qaoa = MinimumEigenOptimizer(qaoa_mes)
qaoa_result = qaoa.solve(qubo)
print("\nQAOA Solution to Binary Problem:")
print(qaoa_result.prettyprint())

# Apply Warm-Start QAOA to the original binary problem
ws_qaoa_mes = QAOA(sampler=Sampler(), optimizer=COBYLA(), initial_state=init_qc, initial_point=[0.0, 1.0])
ws_qaoa = MinimumEigenOptimizer(ws_qaoa_mes)
ws_qaoa_result = ws_qaoa.solve(qubo)
print("\nWarm-Start QAOA Solution to Binary Problem:")
print(ws_qaoa_result.prettyprint())