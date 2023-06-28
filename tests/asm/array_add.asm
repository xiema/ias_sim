# Add the elements of two predefined arrays
# * uses explicit alignment


.text

# initiate counter
la c_count & sa counter

start_1: la x1 & add x2
start_2: sa res & la counter
sub c1 & sa counter
la -counter & bl check
la start_1 & add c_increment
sa start_1 & add c_offset
sal start_2 & jl start_1

check:
# initiate counter
la c_count & sa counter

check_1: la ans & sub res
sa temp & la -|temp
bl check_2 & jl fail
check_2:
la counter & sub c1
sa counter & la -counter
bl success &
# iterate
la check_1 & add c_increment
sa check_1 & jl check_1

fail: 
la c1 & sa status
exit &

success:
exit &


.data

=100
c_increment: 0 1 0 1
c_offset: 0 0 0 2000
c_count: 5 
c1: 1
counter: 0
temp: 0

=1000
x1:
14
5467
21
421
842

=2000
x2:
9
16
931
84
11

=3000
ans:
23
5483
952
505
853

=4000
res: 0

=4095
status: 0
