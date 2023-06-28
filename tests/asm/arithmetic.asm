# Test for correctness of arithmetic functions
# Correct answers are checked for in-code
# Computation results are stored for external checking

.text

addition: LOAD M(x1) & ADD M(x2)
STOR M(add_res) &
SUB M(add_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) &

subtraction:
LOAD M(x2) & SUB M(x1)
STOR M(sub_res) &
SUB M(sub_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &

multiplication:
LOAD MQ,M(x1) & MUL M(x2)
LOAD MQ & STOR M(mul_res)
SUB M(mul_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) &

division:
LOAD M(x2) & DIV M(x1)
STOR M(div_rem_res) &
SUB M(div_rem) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) & LOAD MQ
STOR M(div_res) &
SUB M(div_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &

leftshift:
LOAD M(x1) & LSH
STOR M(lsh_res) &
SUB M(lsh_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) &

rightshift:
LOAD M(x1) & RSH
STOR M(rsh_res) &
SUB M(rsh_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &

negation:
LOAD -M(x1) & SKIP
STOR M(neg_res) &
SUB M(neg_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) &

negabs:
LOAD -|M(x3)| & SKIP
STOR M(negabs_res) &
SUB M(negabs_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &

addabs:
LOAD M(x1) & ADD |M(x3)|
STOR M(addabs_res) &
SUB M(addabs_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) &

subabs:
LOAD M(x1) & SUB |M(x3)|
STOR M(subabs_res) &
SUB M(subabs_ans) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &

mul_l: #double-precision multiplication
LOAD MQ,M(xl1) & MUL M(xl2)
STOR M(mul_l_res_msb) &
SUB M(mul_l_ans_msb) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,0:19) & LOAD MQ
STOR M(mul_l_res_lsb) &
SUB M(mul_l_ans_lsb) & STOR M(temp)
LOAD |M(temp)| & SUB M(c1)
JUMP + M(fail,20:39) &


success:
EXIT & EXIT

fail:
# left and right so that we can check both versions of JUMP
LOAD M(c1) & LOAD M(c1)
# set `status` to nonzero value to signal a computational error
STOR M(status) & EXIT


.data

=1000
temp: 0
c0: 0
c1: 1

x1: 7
x2: 8
x3: -9

xl1: 549755813888
xl2: 31

=2000
add_ans: 15
sub_ans: 1
mul_ans: 56
div_ans: 1
div_rem: 1
lsh_ans: 14
rsh_ans: 3
neg_ans: -7
negabs_ans: -9
addabs_ans: 16
subabs_ans: -2
mul_l_ans_msb: 15
mul_l_ans_lsb: 549755813888

# Store results for external checking
=3000
add_res: 0
sub_res: 0
mul_res: 0
div_res: 0
div_rem_res: 0
lsh_res: 0
rsh_res: 0
neg_res: 0
negabs_res: 0
addabs_res: 0
subabs_res: 0
mul_l_res_msb: 0
mul_l_res_lsb: 0

=4095
# Set to nonzero when calculation is wrong
status: 0
