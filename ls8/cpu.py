"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.less = 0
        self.equal = 0
        self.greater = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        self.MUL = 0b10100010
        self.HLT = 0b00000001

    def load(self):
        """Load a program into memory."""
        address = 0

        with open(sys.argv[1]) as program:
            for line in program:
                data = line.split('#')[0].strip()
                if data == '':
                    continue
                value = int(data, 2)

                self.ram_write(address, value)
                address += 1
                # print(value)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""

        # print(self.ram)
        while self.running:
            instruction_register = self.ram[self.pc]
            op_1 = self.ram_read(self.pc + 1)
            op_2 = self.ram_read(self.pc + 2)

            if instruction_register == self.LDI:
                self.reg[op_1] = op_2
                self.pc += 3

            elif instruction_register == self.PRN:
                print(self.reg[op_1])
                self.pc += 2
            
            elif instruction_register == self.MUL:
                self.alu('MUL', op_1, op_2)
                self.pc += 3

            elif instruction_register == self.CMP:
                self.alu('CMP', op_1, op_2)
                self.pc += 3

            elif instruction_register == self.JMP:
                self.pc = self.reg[op_1]

            elif instruction_register == self.JEQ:
                if self.equal == 1:
                    self.pc = self.reg[op_1]
                else:
                    self.pc += 2

            elif instruction_register == self.JNE:
                if self.equal == 0:
                    self.pc = self.reg[op_1]
                else:
                    self.pc += 2

            elif instruction_register == self.HLT:
                self.running = False

            else:
                print(f"Unknown instruction at index: \t {self.pc}")
                sys.exit(1)