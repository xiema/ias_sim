# Multiply the elements of two predefined arrays
# * uses implicit alignment


.text

# initiate counter
la c_count
sa counter

start_1:
  lam x1
  mul x2
  lm
start_2:
  sa res
  la counter
  sub c1
  sa counter
  la -counter
  ba check
  la start_1
  add c_increment
  sa start_1
  add c_offset
  sar start_2
  ja start_1

check:
  # initiate counter
  la c_count
  sa counter

check_1:
  .alignl
  la ans
  sub res
  sa temp
  la -|temp
  ba check_2
  ja fail
check_2:
  la counter
  sub c1
  sa counter
  la -counter
  ba success
  # iterate
  la check_1
  add c_increment
  sa check_1
  ja check_1

fail: 
  la c1
  sa status
  exit

success:
  exit


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
2
3
4
5
6

=2000
x2:
5
1
9
11
2

=3000
ans:
10
3
36
55
12

=4000
res: 0

=4095
status: 0
