from pipe import Pipe
from filter import Constant, Subtraction, Scope, Gain, Integral, Derivative
from environment import SimpleEnvironment
from fuzzy_m import *
from membership_functions import TriangleMF
from fuzzyfication import Fuzzify
from defuzzyfication import Defuzzify
from tunefis import *


g = 100
r = 1
l = 0.5
cu = 0.01
b = 0.1
j = 0.01

step_size = 0.05

pipe1 = Pipe()
pipe2 = Pipe()
pipe3 = Pipe()
pipe4 = Pipe()
pipe5 = Pipe()
pipe6 = Pipe()
pipe7 = Pipe()
pipe8 = Pipe()
pipe9 = Pipe()
pipe10 = Pipe()
pipe11 = Pipe()
pipe12 = Pipe()
pipe13 = Pipe()
pipe14 = Pipe()
pipe15 = Pipe()
pipe16 = Pipe()
pipe17 = Pipe()
pipe18 = Pipe()
pipe19 = Pipe()
pipe20 = Pipe()
pipe21 = Pipe()
fuzzy_pipe1 = Pipe(initial_value=[['VN', 0], ['MN', 0], ['M', 0], ['MP', 0], ['VP', 0]])
fuzzy_pipe2 = Pipe(initial_value=[['VL', 0], ['ML', 0], ['Z', 0], ['MH', 0], ['VH', 0]])
fuzzy_pipe3 = Pipe(initial_value=[['VN', 0], ['MN', 0], ['Z', 0], ['MP', 0], ['VP', 0]])

scope_pipe = Pipe(name='value')

goal = Constant([], [pipe1], g)
sub1 = Subtraction([pipe1, pipe16], [pipe2, pipe18, pipe19])
sub2 = Subtraction([pipe2, pipe17], [pipe3])
sub3 = Subtraction([pipe3, pipe7], [pipe4])
gain1 = Gain([pipe4], [pipe5], 1 / l)
integrator1 = Integral([pipe5], [pipe6, pipe8], step=step_size)
gain2 = Gain([pipe6], [pipe7], r)
gain3 = Gain([pipe8], [pipe9], cu)
sub4 = Subtraction([pipe9, pipe15], [pipe10])
gain4 = Gain([pipe10], [pipe11], 1 / j)
integrator2 = Integral([pipe11], [pipe12, pipe13, pipe14], step=step_size)
gain5 = Gain([pipe12], [pipe15], b)
integrator3 = Integral([pipe13], [pipe16], step=step_size)
gain6 = Gain([pipe14], [pipe17], cu)
derivative = Derivative([pipe18], [pipe20], step=step_size, min_result=-20, max_result=20)

scope = Scope([scope_pipe], [], 'scope', False)

e_vn = TriangleMF(-150, -100, -50)
e_mn = TriangleMF(-100, -50, 0)
e_m = TriangleMF(-50, 0, 50)
e_mp = TriangleMF(0, 50, 100)
e_vp = TriangleMF(50, 100, 150)

c_vl = TriangleMF(-75, -50, -25)
c_ml = TriangleMF(-50, -25, 0)
c_z = TriangleMF(-25, 0, 25)
c_mh = TriangleMF(0, 25, 50)
c_vh = TriangleMF(25, 50, 75)

out_vn = TriangleMF(-1125, -750, -375)
out_mn = TriangleMF(-750, -375, 0)
out_z = TriangleMF(-375, 0, 375)
out_mp = TriangleMF(0, 375, 750)
out_vp = TriangleMF(375, 750, 1125)

error_fuzzify = Fuzzify([pipe19], [fuzzy_pipe1], [e_vn, e_mn, e_m, e_mp, e_vp], ['VN', 'MN', 'M', 'MP', 'VP'])
change_fuzzify = Fuzzify([pipe20], [fuzzy_pipe2], [c_vl, c_ml, c_z, c_mh, c_vh], ['VL', 'ML', 'Z', 'MH', 'VH'])
fuzzy_rules = FuzzyRules([fuzzy_pipe1, fuzzy_pipe2], [fuzzy_pipe3], [], ['VN', 'MN', 'Z', 'MP', 'VP'])
defuzzify = Defuzzify([fuzzy_pipe2], [scope_pipe], [out_vn, out_mn, out_z, out_mp, out_vp])

environment = SimpleEnvironment([goal, sub1, sub2, sub3, gain1, integrator1, gain2, gain3, sub4, gain4, integrator2,
                                 gain5, integrator3, gain6, derivative, error_fuzzify, change_fuzzify, fuzzy_rules,
                                 defuzzify])
environment.add_filter(scope)

random_search(environment, fuzzy_rules, ['ERROR', 'CHANGE'],
              [['VN', 'MN', 'M', 'MP', 'VP'], ['VL', 'ML', 'Z', 'MH', 'VH']], ['VN', 'MN', 'Z', 'MP', 'VP'])
