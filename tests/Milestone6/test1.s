.data

	_nl: .asciiz "\n"


.text
.globl main

_Print_char:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	li $t9, 11
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY arg_[Print_char_-8]
	add $a0, $a0, $0
	li $v0, 11
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	_return_Print_char:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_Print_int:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	li $t8, 1
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY arg_[Print_int_-8]
	add $a0, $a0, $0
	li $v0, 1
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	li $t7, 10
	li $t6, '
'
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY temp_3
	### offset: [0, '$t6'], temp_3
	add $a0, $t6, $0
	jal _Print_char
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	_return_Print_int:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_Print_string:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	li $t5, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY arg_[Print_string_-8]
	add $a0, $a0, $0
	li $v0, 4
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	li $t4, 10
	li $t3, '
'
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY temp_6
	### offset: [0, '$t3'], temp_6
	add $a0, $t3, $0
	jal _Print_char
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	_return_Print_string:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_Scan_int:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	lw $t2, 0($a0)
	li $t1, 5
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	li $v0, 5
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	addi $t0, $v0, 0
	sw $t0 0($a0)
	_return_Scan_int:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_Scan_char:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	lw $s7, 0($a0)
	li $s6, 12
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	li $v0, 12
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	addi $s5, $v0, 0
	sw $s5 0($a0)
	_return_Scan_char:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_Scan_string:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	lw $s4, 0($a0)
	li $s3, 8
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	li $v0, 8
	syscall
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	addi $s2, $v0, 0
	sw $s2 0($a0)
	_return_Scan_string:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
_add:
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -0
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	add $s1, $a0, $a1
	add $s0, $s1, $0
	add $sp, $sp, -4
	sw	$t9,-68($fp)

	sub $t9, $a0, $a1
	add $sp, $sp, -4
	sw	$t8,-72($fp)

	add $t8, $t9, $0
	# $s0, temp_16
	li $a0 8
	li $v0 9
	syscall
	# $s0, temp_16
	sw $s0, 0($v0)
	# $t8, temp_17
	sw $t8, 4($v0)
	addi $v1, $0, 8
	j _return_add
	_return_add:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	jr $ra
main:
	addi $sp, $sp, 0
	add $fp, $sp, $0
	addi $sp, $sp, -4
	sw $ra, 0($sp)
	addi $sp, $sp, -4
	sw $fp, 0($sp)
	add $fp, $sp, $0
	addi $sp, $sp, -12
	### Saving $s registers
	add $sp, $sp, -4
	sw $s0, 0($sp)
	add $sp, $sp, -4
	sw $s1, 0($sp)
	add $sp, $sp, -4
	sw $s2, 0($sp)
	add $sp, $sp, -4
	sw $s3, 0($sp)
	add $sp, $sp, -4
	sw $s4, 0($sp)
	add $sp, $sp, -4
	sw $s5, 0($sp)
	add $sp, $sp, -4
	sw $s6, 0($sp)
	add $sp, $sp, -4
	sw $s7, 0($sp)
	add $sp, $sp, -4
	sw	$t7,-80($fp)

	li $t7, 2
	add $sp, $sp, -4
	sw	$t6,-84($fp)

	li $t6, 3
	add $sp, $sp, -4
	sw	$t5,-88($fp)

	li $t5, 5
	# $t7, temp_18
	sw $t7, -36($fp)
	# $t6, temp_19
	sw $t6, -40($fp)
	# $t5, temp_20
	sw $t5, -44($fp)
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_a
	add $sp, $sp, -4
	sw	$t4,-148($fp)

	lw $t4, -36($fp)
	add $a0, $t4, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_b
	add $sp, $sp, -4
	sw	$t3,-152($fp)

	lw $t3, -40($fp)
	add $a0, $t3, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_c
	add $sp, $sp, -4
	sw	$t2,-156($fp)

	lw $t2, -44($fp)
	add $a0, $t2, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	add $sp, $sp, -4
	sw	$t1,-104($fp)

	lw $t1, -36($fp)
	add $sp, $sp, -4
	sw	$t0,-108($fp)

	addi $t0, $t1, 0
	lw $t9, -40($fp)
	add $sp, $sp, -4
	sw	$t8,-112($fp)

	addi $t8, $t9, 0
	add $sp, $sp, -4
	sw	$t7,-116($fp)

	lw $t7, -44($fp)
	add $sp, $sp, -4
	sw	$t6,-120($fp)

	addi $t6, $t7, 0
	# $t0, temp_21
	sw $t0, -40($fp)
	# $t8, temp_22
	sw $t8, -44($fp)
	# $t6, temp_23
	sw $t6, -36($fp)
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_a
	add $sp, $sp, -4
	sw	$t5,-180($fp)

	lw $t5, -36($fp)
	add $a0, $t5, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_b
	lw $t4, -40($fp)
	add $a0, $t4, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_c
	lw $t3, -44($fp)
	add $a0, $t3, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	lw $t2, -36($fp)
	addi $t1, $t2, 0
	lw $t9, -40($fp)
	addi $t7, $t9, 0
	add $sp, $sp, -4
	sw	$t0,-128($fp)

	lw $t0, -44($fp)
	add $sp, $sp, -4
	sw	$t8,-132($fp)

	addi $t8, $t0, 0
	# $t1, temp_24
	sw $t1, -40($fp)
	# $t7, temp_25
	sw $t7, -44($fp)
	# $t8, temp_26
	sw $t8, -36($fp)
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_a
	add $sp, $sp, -4
	sw	$t6,-192($fp)

	lw $t6, -36($fp)
	add $a0, $t6, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_b
	lw $t5, -40($fp)
	add $a0, $t5, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	#### Saving temporary registers
	add $sp, $sp, -4
	sw $t0, 0($sp)
	add $sp, $sp, -4
	sw $t1, 0($sp)
	add $sp, $sp, -4
	sw $t2, 0($sp)
	add $sp, $sp, -4
	sw $t3, 0($sp)
	add $sp, $sp, -4
	sw $t4, 0($sp)
	add $sp, $sp, -4
	sw $t5, 0($sp)
	add $sp, $sp, -4
	sw $t6, 0($sp)
	add $sp, $sp, -4
	sw $t7, 0($sp)
	add $sp, $sp, -4
	sw $t8, 0($sp)
	add $sp, $sp, -4
	sw $t9, 0($sp)
	#### Done saving temporary registers
	#### Saving argument registers
	add $sp, $sp, -4
	sw $a0, 0($sp)
	add $sp, $sp, -4
	sw $a1, 0($sp)
	add $sp, $sp, -4
	sw $a2, 0($sp)
	add $sp, $sp, -4
	sw $a3, 0($sp)
	#### Done saving argument registers
	#### YAYYY 4_c
	lw $t4, -44($fp)
	add $a0, $t4, $0
	jal _Print_int
	### Restoring argument registers
	lw $a3, 0($sp)
	add $sp, $sp, 4
	lw $a2, 0($sp)
	add $sp, $sp, 4
	lw $a1, 0($sp)
	add $sp, $sp, 4
	lw $a0, 0($sp)
	add $sp, $sp, 4
	### Done restoring argument registers
	lw $t9, 0($sp)
	add $sp, $sp, 4
	lw $t8, 0($sp)
	add $sp, $sp, 4
	lw $t7, 0($sp)
	add $sp, $sp, 4
	lw $t6, 0($sp)
	add $sp, $sp, 4
	lw $t5, 0($sp)
	add $sp, $sp, 4
	lw $t4, 0($sp)
	add $sp, $sp, 4
	lw $t3, 0($sp)
	add $sp, $sp, 4
	lw $t2, 0($sp)
	add $sp, $sp, 4
	lw $t1, 0($sp)
	add $sp, $sp, 4
	lw $t0, 0($sp)
	add $sp, $sp, 4
	_return_main:
	### Restoring $s registers
	lw $s7, 0($sp)
	add $sp, $sp, 4
	lw $s6, 0($sp)
	add $sp, $sp, 4
	lw $s5, 0($sp)
	add $sp, $sp, 4
	lw $s4, 0($sp)
	add $sp, $sp, 4
	lw $s3, 0($sp)
	add $sp, $sp, 4
	lw $s2, 0($sp)
	add $sp, $sp, 4
	lw $s1, 0($sp)
	add $sp, $sp, 4
	lw $s0, 0($sp)
	add $sp, $sp, 4
	lw $ra, 4($fp)
	addi $sp, $fp, 8
	lw $fp, 0($fp)
	li $v0 10
	syscall
