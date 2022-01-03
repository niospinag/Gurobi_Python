from gurobipy import *

#resources and jobs sets
R = ['Carlos', 'Joe', 'Monika']
J = ['Tester', 'JavaDeveloper', 'Architect' ]

#matching score data
combinations, ms = multidict({
    ('Carlos', 'Tester'): 53,
    ('Carlos', 'JavaDeveloper'): 27,
    ('Carlos', 'Architect'): 13,
    ('Joe', 'Tester'): 80,
    ('Joe', 'JavaDeveloper'): 47,
    ('Joe', 'Architect'): 67,
    ('Monika', 'Tester'): 53,
    ('Monika', 'JavaDeveloper'): 73,
    ('Monika', 'Architect'): 47
})

print('combinations: ', combinations)
print('ms: ', ms)


# Declare and initialize model
m = Model('RAP')

#  Create decision variables for the RAP model
x = m.addVars(combinations, name = 'assign' )

# create jobs constraints
jobs = m.addConstrs(( x.sum('*',j) ==1 for j in J ), 'job')

# create resources constraints
resources = m.addConstrs(( x.sum(r,'*') <=1 for r in R ), 'resource')

# The objective is to maximize total matching score of the assignments
m.setObjective(x.prod(ms), GRB.MAXIMIZE)

# save model for inspection
m.write('RAP.lp')

# run optimization engine
m.optimize()

# display optimal values of decision variables
for v in m.getVars():
    if(abs(v.x) > 1e-6):
        print(v.varname, v.x)

# # display optimal total matching score
print('total matching scores', m.objVal)

print(m.getVars)
