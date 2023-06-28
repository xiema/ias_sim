# Lists the first N elements of the fibonacci series

.text
start:
# check if N elements reached
la N
sub counter
sub c1
ba calc_1
exit

.alignl
# next element
calc_1:
la fib_1
add fib_2
calc_2:
sa fib_start
# iterate
la calc_1
add increment
sa calc_1
add increment
saa calc_2
la counter
add c1
sa counter
ja start


.data
=900
N: 20
counter: 2
c1: 1
c2: 2
increment: 0 1 0 1

=1000
fib_1: 0
fib_2: 1
fib_start: 0
