# Test alignment-dependent instructions

.text

test_1a: ja jump_left
test_1b: ja jump_right
test_2a: la c1 & ba branch_left
test_2b: la c1 & ba branch_right
test_3a:
la loadvar_1 & sal var1
la var1 & sub var_check_1
sa temp & la |temp
sub c1 & ba test_3b
la status & sub c5
sa status & jl test_3b
test_3b:
la loadvar_2 & sar var2
la var2 & sub var_check_2 
sa temp & la |temp 
sub c1 & ba end
la status & sub c6
sa status & ja end

# act as .data
.alignl
var1: 
skip
var2:
skip

.alignl
jump_left:
jl _jump_left_1 & jr test_1b
_jump_left_1:
la status & sub c1
sa status & jr test_1b

.alignl
jl test_2a
jump_right:
skip
la status & sub c2
sa status & jl test_2a

.alignl
branch_left:
jl _branch_left_1 & jl test_2b
_branch_left_1:
la status & sub c3
sa status & jl test_2b

.alignl
jl test_3a
branch_right:
skip
la status & sub c4
sa status & jl test_3a

end:
exit


.data

=100
c1: 1
c2: 2
c3: 4
c4: 8
c5: 16
c6: 32

loadvar_1: 0 0 0 5
loadvar_2: 0 0 0 7
var_check_1: 0xAA 5 0xAA 0
var_check_2: 0xAA 5 0xAA 7

temp: 0

=4095
status: 63 # bitflag of c1 + c2 + ... + c6
