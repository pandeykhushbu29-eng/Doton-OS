# Chapter 1 — Introduction

## 1.1 Purpose

Doublers is an open 64-bit Instruction Set Architecture (ISA) designed to be simple, predictable, and practical. It is intended for operating systems, systems software, compilers, educational use, and future hardware implementations.

The ISA defines the behavior of processors that execute Doublers instructions. It does not define the physical design of a processor. Hardware designers are free to implement the ISA using any suitable architecture, provided the implementation behaves according to this specification.

---

## 1.2 Goals

The primary goals of Doublers are:

* Simplicity over unnecessary complexity.
* Fixed, well-defined instruction behavior.
* Easy implementation in hardware.
* Efficient native execution.
* Stable long-term compatibility.
* Open specification for software and hardware developers.

---

## 1.3 Scope

This specification defines:

* The register architecture.
* The memory model.
* Instruction encoding.
* Instruction behavior.
* Exception handling.
* Privilege levels.
* System calls.
* Compliance requirements.

This specification does not define:

* Operating system design.
* Compiler implementation.
* Processor microarchitecture.
* Semiconductor manufacturing.

---

## 1.4 Design Philosophy

Doublers follows five design principles:

1. Simplicity
2. Predictability
3. Readability
4. Hardware friendliness
5. Long-term compatibility

The ISA should remain understandable to both beginners and experienced system programmers while remaining practical for modern computing.

---

## 1.5 Versioning

The first public release of the architecture is named:

Doublers ISA Version 1.0

Future revisions may introduce optional extensions while preserving compatibility with the Base ISA whenever practical.

---

## 1.6 Open Architecture

Doublers is intended to be an open architecture.

Any individual or organization may develop compatible software, tools, simulators, operating systems, compilers, debuggers, or hardware implementations that conform to this specification, subject to the project's chosen license.

---

## 1.7 Terminology

Throughout this specification:

ISA — Instruction Set Architecture

CPU — Central Processing Unit

Register — A processor storage location.

Opcode — The binary identifier of an instruction.

Operand — Data supplied to an instruction.

Extension — An optional group of additional instructions beyond the Base ISA.

# Chapter 2 — Architecture Overview

## 2.1 Overview

Doublers is a modern 64-bit Instruction Set Architecture (ISA) designed for operating systems, embedded systems, educational purposes, and general systems programming.

The architecture prioritizes simplicity, consistency, and efficient hardware implementation while remaining extensible through optional ISA extensions.

---

## 2.2 Architecture Summary

| Property                  | Value         |
| ------------------------- | ------------- |
| Architecture Name         | Doublers-64   |
| Word Size                 | 64 Bits       |
| Byte Size                 | 8 Bits        |
| Endianness                | Little Endian |
| General Purpose Registers | 16            |
| Special Registers         | 4             |
| Address Space             | 64-Bit        |
| Memory Model              | Flat          |
| Extension Support         | Yes           |

---

## 2.3 Execution Model

A Doublers-compatible processor executes instructions in the following order:

1. Fetch the instruction from memory.
2. Decode the instruction.
3. Read any required registers or memory operands.
4. Execute the operation.
5. Write the result.
6. Advance the Instruction Pointer (IP) unless modified by the instruction.

This execution model applies to all implementations of the Base ISA.

---

## 2.4 General Purpose Registers

The architecture provides sixteen (16) general-purpose 64-bit registers.

These registers are identified as:

* D0
* D1
* D2
* D3
* D4
* D5
* D6
* D7
* D8
* D9
* D10
* D11
* D12
* D13
* D14
* D15

Unless otherwise specified, any instruction may use any general-purpose register.

---

## 2.5 Special Registers

Every Doublers-compatible processor shall implement the following special registers:

**IP** — Instruction Pointer

Tracks the address of the next instruction to be executed.

**SP** — Stack Pointer

Tracks the top of the active stack.

**BP** — Base Pointer

Provides a stable reference for stack frames.

**FLAGS** — Status Register

Stores status information such as arithmetic results and processor state.

---

## 2.6 Memory Model

Doublers uses a flat memory model.

All memory locations exist within a single linear address space.

Memory is byte-addressable.

The operating system is responsible for memory protection, allocation, and virtual memory management where applicable.

---

## 2.7 Instruction Length

The Base Doublers ISA uses a fixed-length instruction format.

Every Base ISA instruction occupies exactly one instruction word.

A fixed-length encoding simplifies hardware decoding, compiler implementation, and instruction fetching.

The exact binary layout is defined in Chapter 6.

---

## 2.8 Privilege Levels

The Base ISA defines two privilege levels:

**Kernel Mode**

Provides unrestricted access to privileged instructions and hardware resources.

**User Mode**

Restricts execution of privileged instructions and protects operating system resources.

Operating systems are responsible for managing transitions between privilege levels.

---

## 2.9 Extensions

The architecture supports optional instruction set extensions.

Processors implementing additional instructions shall clearly identify all supported extensions.

Programs shall not assume extension availability unless explicitly required.

---

## 2.10 Compatibility

A processor is considered Doublers-compatible if it correctly implements all mandatory requirements defined by the Base ISA.

Optional extensions shall not alter the behavior of Base ISA instructions.

---

## 2.11 Future Expansion

Doublers is designed as an open Instruction Set Architecture (ISA).

The original creator may not be able to maintain or publish future official versions of this specification.

To encourage continued development, the community is permitted to create compatible extensions, derivative specifications, tools, and hardware implementations, provided that:

* They clearly identify their work as community-created.
* They do not claim to be official Doublers specifications.
* They preserve compatibility with the Doublers Base ISA whenever practical.

The original Doublers ISA v1.0 shall remain the reference foundation for the architecture.

# Chapter 3 — Register Architecture

## 3.1 Overview

The Doublers Base ISA defines sixteen (16) general-purpose registers and four (4) special-purpose registers.

All general-purpose registers are sixty-four (64) bits wide and are equally capable of storing integer values, addresses, or implementation-defined data.

No general-purpose register has a permanently reserved architectural purpose.

---

## 3.2 Register Set

The Base ISA defines the following general-purpose registers:

| Register |   Width | Description              |
| -------- | ------: | ------------------------ |
| D0       | 64 Bits | General Purpose Register |
| D1       | 64 Bits | General Purpose Register |
| D2       | 64 Bits | General Purpose Register |
| D3       | 64 Bits | General Purpose Register |
| D4       | 64 Bits | General Purpose Register |
| D5       | 64 Bits | General Purpose Register |
| D6       | 64 Bits | General Purpose Register |
| D7       | 64 Bits | General Purpose Register |
| D8       | 64 Bits | General Purpose Register |
| D9       | 64 Bits | General Purpose Register |
| D10      | 64 Bits | General Purpose Register |
| D11      | 64 Bits | General Purpose Register |
| D12      | 64 Bits | General Purpose Register |
| D13      | 64 Bits | General Purpose Register |
| D14      | 64 Bits | General Purpose Register |
| D15      | 64 Bits | General Purpose Register |

---

## 3.3 Register Width

Each register stores exactly sixty-four (64) bits.

Processors implementing the Base ISA shall not reduce the size of any general-purpose register.

---

## 3.4 Register Usage

General-purpose registers may be used by any instruction unless otherwise specified.

Software is free to assign any purpose to a register.

Operating systems, compilers, and Application Binary Interfaces (ABIs) may define register usage conventions, but such conventions are not part of the Base ISA.

---

## 3.5 Special Registers

Every Doublers-compatible processor shall implement the following special registers.

### Instruction Pointer (IP)

The IP register stores the address of the next instruction to execute.

Control-flow instructions modify the IP directly.

---

### Stack Pointer (SP)

The SP register identifies the top of the current stack.

Stack instructions automatically update the SP register.

---

### Base Pointer (BP)

The BP register provides a stable reference point for stack frames.

Its usage is optional and determined by software.

---

### FLAGS Register

The FLAGS register records the outcome of selected processor operations.

The Base ISA defines the following status flags.

| Flag | Meaning       |
| ---- | ------------- |
| Z    | Zero Flag     |
| C    | Carry Flag    |
| O    | Overflow Flag |
| N    | Negative Flag |

Future ISA revisions or extensions may define additional status flags.

---

## 3.6 Register Access

General-purpose registers are readable and writable by all standard instructions.

Special registers may only be modified by instructions defined for that purpose.

Attempting to modify protected registers using undefined instructions results in an Illegal Instruction Exception.

---

## 3.7 Register Reset State

Following processor reset:

* The Instruction Pointer shall point to the platform-defined reset vector.
* The Stack Pointer shall be initialized by the platform firmware or bootloader.
* The FLAGS register shall be initialized to the processor default state.
* The initial values of D0–D15 are implementation-defined.

Software shall not rely on the initial values of general-purpose registers.

---

## 3.8 Reserved Registers

The Base ISA reserves no general-purpose registers.

Future extensions shall not permanently repurpose D0–D15 in a manner that breaks compatibility with existing software.

---

## 3.9 Compliance

A processor shall be considered compliant with this chapter only if it:

* Implements all sixteen general-purpose registers.
* Implements all required special registers.
* Supports sixty-four-bit register operations.
* Preserves the architectural behavior defined in this chapter.

# Chapter 4 — Memory Architecture

## 4.1 Overview

The Doublers Base ISA defines a flat, byte-addressable memory architecture.

Every compatible processor shall access memory using the rules defined in this chapter.

The architecture is designed to remain simple while supporting modern operating systems.

---

## 4.2 Address Space

Doublers-64 defines a sixty-four (64) bit virtual address space.

Each memory location is identified by a unique 64-bit address.

The theoretical address range is:

0x0000000000000000

to

0xFFFFFFFFFFFFFFFF

The actual amount of available memory is implementation-defined.

---

## 4.3 Memory Unit

The smallest addressable memory unit is one (1) byte.

Larger values are formed by combining consecutive bytes.

Supported data sizes include:

| Data Type | Size    |
| --------- | ------- |
| Byte      | 8 Bits  |
| Half      | 16 Bits |
| Word      | 32 Bits |
| Double    | 64 Bits |

Future ISA extensions may introduce larger data types.

---

## 4.4 Endianness

The Base ISA uses Little-Endian byte ordering.

The least significant byte of a multi-byte value is stored at the lowest memory address.

Processors shall not alter this behavior.

---

## 4.5 Memory Alignment

Natural alignment is recommended.

Examples:

* 16-bit values should be aligned to 2-byte boundaries.
* 32-bit values should be aligned to 4-byte boundaries.
* 64-bit values should be aligned to 8-byte boundaries.

Processors may support unaligned memory access.

If unsupported, an Alignment Exception shall be generated.

---

## 4.6 Memory Access

Memory may be accessed only through instructions defined by the ISA.

Examples include:

* LOAD
* STORE
* PUSH
* POP

Undefined methods of memory access are prohibited.

---

## 4.7 Read and Write Operations

A read operation retrieves data from memory without modifying the stored value.

A write operation replaces the existing value stored at the specified address.

All memory accesses shall obey the privilege rules defined by the operating system.

---

## 4.8 Memory Protection

The Base ISA provides support for protected memory.

The implementation of virtual memory, paging, and permission management is platform-defined.

Operating systems are responsible for enforcing memory protection.

---

## 4.9 Reserved Memory

Processors may reserve implementation-specific memory regions.

Software shall not depend upon reserved memory unless documented by the platform.

---

## 4.10 Stack Memory

The stack grows toward lower memory addresses.

The Stack Pointer (SP) always identifies the current top of the stack.

PUSH decreases the Stack Pointer before storing data.

POP retrieves data before increasing the Stack Pointer.

---

## 4.11 Null Address

The interpretation of address 0x0000000000000000 is platform-defined.

Operating systems may reserve this address to detect invalid memory accesses.

---

## 4.12 Future Expansion

Future ISA extensions may introduce:

* Memory encryption
* Capability-based memory
* Tagged memory
* Persistent memory support

Such extensions shall preserve compatibility with the Base ISA whenever practical.

---

## 4.13 Compliance

A processor is compliant with this chapter if it:

* Implements byte-addressable memory.
* Uses Little-Endian byte ordering.
* Supports 64-bit addressing.
* Correctly performs all defined memory operations.
* Preserves architectural compatibility with the Base ISA.

# Chapter 5: Instruction Set Architecture

## 5.1 Overview

The Instruction Set Architecture (ISA) defines the complete communication interface between software and the Doublers-64 processor.

Instructions are fixed-size binary commands executed by the processor. Each instruction specifies an operation, source operands, destination operands, and optional immediate data.

The Doublers-64 ISA is designed with the following goals:

- Simple decoding
- High performance execution
- Easy compiler support
- Future expansion capability
- Strong separation between user and privileged operations

Every valid Doublers-64 processor must implement the base instruction set defined in this chapter.

---

# 5.2 Instruction Size

Doublers-64 uses a fixed-length instruction format.

## Base Instruction Length

| Field | Size |
|---|---:|
| Instruction Size | 32 bits |
| Opcode Field | 8 bits |
| Register Fields | Variable |
| Immediate Field | Variable |

All instructions are aligned on 4-byte boundaries.

The Instruction Pointer (IP) always points to the next 32-bit instruction.

---

# 5.3 Instruction Encoding

A standard Doublers-64 instruction follows this format:


31 24 23 20 19 16 15 0
+--------------------+---------+---------+-------------------------+
| OPCODE | RD | RS1 | IMM / RS2 |
+--------------------+---------+---------+-------------------------+


## Fields

### OPCODE (8 bits)

Defines the operation performed by the processor.

Range:


00000000 - 11111111


Total possible instructions:


256 Opcodes


---

### RD (4 bits)

Destination register.

Range:


D0 - D15


Used when an instruction writes a result.

---

### RS1 (4 bits)

First source register.

Contains the first input operand.

---

### IMM / RS2 (16 bits)

This field has two possible meanings:

1. Immediate value
2. Second source register and additional control bits

The instruction type determines the interpretation.

---

# 5.4 Instruction Categories

The Doublers-64 instruction set is divided into multiple groups.

| Category | Purpose |
|---|---|
| Arithmetic | Mathematical operations |
| Logical | Bit manipulation |
| Memory | Load and store operations |
| Branch | Program flow control |
| System | Processor management |
| Floating Point | Decimal calculations |
| Atomic | Multi-core synchronization |
| Extension | Future expansion |

---

# 5.5 Opcode Organization

Opcode ranges are reserved by category.

| Opcode Range | Category |
|---|---|
| 0x00 - 0x1F | Arithmetic |
| 0x20 - 0x3F | Logical |
| 0x40 - 0x5F | Memory |
| 0x60 - 0x7F | Branch & Control |
| 0x80 - 0x9F | System |
| 0xA0 - 0xBF | Floating Point |
| 0xC0 - 0xDF | Atomic Operations |
| 0xE0 - 0xFF | Reserved Extensions |

Reserved instructions must trigger an illegal instruction exception.

---

# 5.6 Arithmetic Instructions

Arithmetic instructions operate on integer values stored inside general purpose registers.

## ADD

Opcode:


0x00


Operation:


RD = RS1 + RS2


Example:


ADD D1, D2, D3


Meaning:


D1 = D2 + D3


Flags affected:


Z - Zero
C - Carry
O - Overflow
N - Negative


---

## SUB

Opcode:


0x01


Operation:


RD = RS1 - RS2


Example:


SUB D4, D5, D6


Meaning:


D4 = D5 - D6


Flags affected:


Z
C
O
N


---

## MUL

Opcode:


0x02


Operation:


RD = RS1 × RS2


---

## DIV

Opcode:


0x03


Operation:


RD = RS1 ÷ RS2


Division by zero generates a processor exception.

---

# 5.7 Immediate Arithmetic

Immediate instructions allow constants inside instructions.

## ADDI

Opcode:


0x04


Operation:


RD = RS1 + IMM


Example:


ADDI D1, D2, 25


Equivalent:


D1 = D2 + 25


---

# 5.8 Increment and Decrement

## INC

Opcode:


0x05


Operation:


RD = RD + 1


---

## DEC

Opcode:


0x06


Operation:


RD = RD - 1


---

# 5.9 No Operation

## NOP

Opcode:


0x07


Operation:


No action


NOP consumes one instruction cycle.

Used for:

- Timing adjustment
- Pipeline alignment
- Debugging

---

# 5.10 Future Expansion

The following areas are reserved:

- Vector processing
- AI acceleration
- Cryptography extensions
- Graphics instructions
- Secure execution extensions

Future Doublers-64 versions may introduce new instructions without breaking existing software compatibility.

# 5.11 Logical Instructions

Logical instructions perform bit-level operations on registers.

These operations are essential for:

- Device control
- Cryptography
- Operating system functions
- Low-level programming

Logical instructions operate on 64-bit values.

---

# 5.11.1 AND

Opcode:


0x20


Operation:


RD = RS1 AND RS2


Example:


AND D1, D2, D3


Meaning:


D1 = D2 & D3


Each bit is set to 1 only when both input bits are 1.

Flags affected:


Z
N


---

# 5.11.2 OR

Opcode:


0x21


Operation:


RD = RS1 OR RS2


Example:


OR D1, D2, D3


Meaning:


D1 = D2 | D3


Each bit is set to 1 when either input bit is 1.

Flags affected:


Z
N


---

# 5.11.3 XOR

Opcode:


0x22


Operation:


RD = RS1 XOR RS2


Example:


XOR D1, D2, D3


Meaning:


D1 = D2 ^ D3


XOR produces 1 when both input bits are different.

Flags affected:


Z
N


---

# 5.11.4 NOT

Opcode:


0x23


Operation:


RD = NOT RS1


Example:


NOT D1, D2


Meaning:


D1 = ~D2


All bits are inverted.

Flags affected:


Z
N


---

# 5.12 Shift Instructions

Shift instructions move bits inside registers.

All shifts are logical unless specified otherwise.

---

# 5.12.1 Logical Shift Left (LSL)

Opcode:


0x24


Operation:


RD = RS1 << IMM


Bits are shifted toward the most significant side.

Empty positions are filled with zero.

Example:


LSL D1, D2, 4


Equivalent:


D1 = D2 × 16


---

# 5.12.2 Logical Shift Right (LSR)

Opcode:


0x25


Operation:


RD = RS1 >> IMM


Empty positions are filled with zero.

---

# 5.12.3 Arithmetic Shift Right (ASR)

Opcode:


0x26


Operation:


RD = RS1 >> IMM


Unlike LSR, ASR keeps the sign bit.

Used for signed numbers.

---

# 5.12.4 Rotate Left (ROL)

Opcode:


0x27


Operation:


RD = RotateLeft(RS1, IMM)


Bits shifted out from the left side return from the right side.

---

# 5.12.5 Rotate Right (ROR)

Opcode:


0x28


Operation:


RD = RotateRight(RS1, IMM)


Bits shifted out from the right side return from the left side.

---

# 5.13 Bit Manipulation Instructions

Doublers-64 provides direct bit control instructions.

---

# 5.13.1 Bit Set

Opcode:


0x29


Operation:


SetBit(RD, RS1, IMM)


Sets the selected bit to 1.

Example:


BSET D1, D2, 5


---

# 5.13.2 Bit Clear

Opcode:


0x2A


Operation:


ClearBit(RD, RS1, IMM)


Sets the selected bit to 0.

---

# 5.13.3 Bit Toggle

Opcode:


0x2B


Operation:


ToggleBit(RD, RS1, IMM)


Flips the selected bit.

---

# 5.13.4 Bit Test

Opcode:


0x2C


Operation:


FLAGS.Z = SelectedBit == 0


Checks the value of a specific bit.

---

# 5.14 Comparison Instructions

Comparison instructions update FLAGS without changing registers.

---

# 5.14.1 Compare Equal

Opcode:


0x2D


Operation:


FLAGS.Z = (RS1 == RS2)


---

# 5.14.2 Compare Greater

Opcode:


0x2E


Operation:


FLAGS = RS1 > RS2


---

# 5.14.3 Compare Less

Opcode:


0x2F


Operation:


FLAGS = RS1 < RS2


---

# 5.15 Logical Instruction Summary

| Instruction | Opcode | Function |
|---|---|---|
| AND | 0x20 | Bitwise AND |
| OR | 0x21 | Bitwise OR |
| XOR | 0x22 | Bitwise XOR |
| NOT | 0x23 | Invert bits |
| LSL | 0x24 | Shift left |
| LSR | 0x25 | Shift right |
| ASR | 0x26 | Arithmetic shift |
| ROL | 0x27 | Rotate left |
| ROR | 0x28 | Rotate right |
| BSET | 0x29 | Set bit |
| BCLR | 0x2A | Clear bit |
| BTGL | 0x2B | Toggle bit |
| BTEST | 0x2C | Test bit |
| CEQ | 0x2D | Compare equal |
| CGT | 0x2E | Compare greater |
| CLT | 0x2F | Compare less |

---

# 5.16 Memory Instructions

Memory instructions allow the processor to transfer data between registers and main memory.

Doublers-64 uses a byte-addressable memory model.

All memory addresses are 64-bit.

Memory instructions support:

- Loading data from memory
- Storing data to memory
- Stack management
- Atomic memory operations

---

# 5.16.1 LOAD

Opcode:


0x40


Operation:


RD = Memory[RS1 + IMM]


The processor reads data from the calculated memory address and places it into the destination register.

Example:


LOAD D1, D2, 8


Meaning:


D1 = Memory[D2 + 8]


Flags affected:


None


---

# 5.16.2 STORE

Opcode:


0x41


Operation:


Memory[RS1 + IMM] = RD


Stores the value of a register into memory.

Example:


STORE D1, D2, 16


Meaning:


Memory[D2 + 16] = D1


Flags affected:


None


---

# 5.16.3 LOAD BYTE

Opcode:


0x42


Operation:


RD = Memory8[RS1 + IMM]


Loads one byte from memory.

---

# 5.16.4 LOAD HALFWORD

Opcode:


0x43


Operation:


RD = Memory16[RS1 + IMM]


Loads a 16-bit value.

---

# 5.16.5 LOAD WORD

Opcode:


0x44


Operation:


RD = Memory32[RS1 + IMM]


Loads a 32-bit value.

---

# 5.16.6 STORE BYTE

Opcode:


0x45


Operation:


Memory8[RS1 + IMM] = RD


Stores the lowest 8 bits of a register.

---

# 5.16.7 STORE HALFWORD

Opcode:


0x46


Operation:


Memory16[RS1 + IMM] = RD


Stores the lowest 16 bits.

---

# 5.16.8 STORE WORD

Opcode:


0x47


Operation:


Memory32[RS1 + IMM] = RD


Stores the lowest 32 bits.

---

# 5.17 Stack Instructions

The stack is controlled by the Stack Pointer (SP).

The stack grows downward toward lower memory addresses.

---

# 5.17.1 PUSH

Opcode:


0x48


Operation:


SP = SP - 8
Memory[SP] = RD


Stores a 64-bit register value on the stack.

Example:


PUSH D1


Equivalent:


SP -= 8
Memory[SP] = D1


---

# 5.17.2 POP

Opcode:


0x49


Operation:


RD = Memory[SP]
SP = SP + 8


Restores a value from the stack.

Example:


POP D1


---

# 5.17.3 PUSH ALL

Opcode:


0x4A


Operation:

Stores all general-purpose registers:


D0-D15


Used during:

- Interrupt handling
- Context switching
- Task switching

---

# 5.17.4 POP ALL

Opcode:


0x4B


Operation:

Restores:


D0-D15


from the stack.

---

# 5.18 Address Calculation Instructions

These instructions help create memory addresses efficiently.

---

# 5.18.1 LOAD ADDRESS

Opcode:


0x4C


Operation:


RD = RS1 + IMM


Unlike LOAD, this instruction does not access memory.

Example:


LEA D1, D2, 32


Meaning:


D1 = D2 + 32


Used for:

- Arrays
- Structures
- Pointers

---

# 5.18.2 MEMORY COPY

Opcode:


0x4D


Operation:


Copy memory block


Copies a specified amount of memory from one location to another.

Used by:

- Operating systems
- File systems
- Device drivers

---

# 5.19 Atomic Memory Instructions

Atomic instructions guarantee that an operation completes without interruption.

Required for:

- Multi-core processors
- Locks
- Synchronization

---

# 5.19.1 LOAD RESERVED

Opcode:


0x4E


Operation:


RD = Memory[Address]
Reserve(Address)


Creates a memory reservation.

---

# 5.19.2 STORE CONDITIONAL

Opcode:


0x4F


Operation:


if ReservationValid:
Memory[Address] = RD
FLAGS.Z = 1
else:
FLAGS.Z = 0


Used to implement:

- Mutexes
- Spinlocks
- Thread synchronization

---

# 5.20 Memory Instruction Summary

| Instruction | Opcode | Function |
|---|---|---|
| LOAD | 0x40 | Load 64-bit value |
| STORE | 0x41 | Store 64-bit value |
| LOAD.B | 0x42 | Load byte |
| LOAD.H | 0x43 | Load halfword |
| LOAD.W | 0x44 | Load word |
| STORE.B | 0x45 | Store byte |
| STORE.H | 0x46 | Store halfword |
| STORE.W | 0x47 | Store word |
| PUSH | 0x48 | Push stack value |
| POP | 0x49 | Pop stack value |
| PUSHALL | 0x4A | Save registers |
| POPALL | 0x4B | Restore registers |
| LEA | 0x4C | Calculate address |
| MEMCOPY | 0x4D | Copy memory |
| LRES | 0x4E | Load reserved |
| SC | 0x4F | Store conditional |

---

# 5.21 Control Flow Instructions

Control flow instructions modify the Instruction Pointer (IP).

They allow programs to:

- Jump between code sections
- Create functions
- Perform loops
- Handle decisions
- Manage exceptions

The Instruction Pointer always contains the address of the next instruction to execute.

---

# 5.21.1 JUMP

Opcode:


0x60


Operation:


IP = Address


The processor immediately continues execution from the specified address.

Example:


JMP 0x8000


Meaning:


Execute instruction at memory address 0x8000


---

# 5.21.2 JUMP REGISTER

Opcode:


0x61


Operation:


IP = RD


The jump address is stored inside a register.

Example:


JMPR D1


Meaning:


IP = D1


Used for:

- Function pointers
- Dynamic jumps
- Virtual machines

---

# 5.21.3 CALL

Opcode:


0x62


Operation:


SP = SP - 8
Memory[SP] = IP + 4
IP = Address


CALL performs a function call.

It stores the return location on the stack.

Example:


CALL Function_Address


---

# 5.21.4 RETURN

Opcode:


0x63


Operation:


IP = Memory[SP]
SP = SP + 8


Returns execution to the instruction after CALL.

Example:


RET


---

# 5.22 Conditional Branch Instructions

Conditional branches check FLAGS before changing execution flow.

---

# 5.22.1 Branch Equal

Opcode:


0x64


Condition:


IF FLAGS.Z = 1
IP = Address


Instruction:


BEQ Address


Used after comparison operations.

---

# 5.22.2 Branch Not Equal

Opcode:


0x65


Condition:


IF FLAGS.Z = 0
IP = Address


Instruction:


BNE Address


---

# 5.22.3 Branch Greater

Opcode:


0x66


Condition:


IF greater
IP = Address


Instruction:


BGT Address


---

# 5.22.4 Branch Less

Opcode:


0x67


Condition:


IF less
IP = Address


Instruction:


BLT Address


---

# 5.22.5 Branch Greater or Equal

Opcode:


0x68


Instruction:


BGE Address


---

# 5.22.6 Branch Less or Equal

Opcode:


0x69


Instruction:


BLE Address


---

# 5.22.7 Branch Carry Set

Opcode:


0x6A


Condition:


IF FLAGS.C = 1
IP = Address


Instruction:


BCS Address


Used for:

- Arithmetic overflow handling
- Multi-word calculations

---

# 5.22.8 Branch Overflow

Opcode:


0x6B


Condition:


IF FLAGS.O = 1
IP = Address


Instruction:


BVS Address


---

# 5.23 Loop Instructions

Doublers-64 provides dedicated loop instructions.

---

# 5.23.1 LOOP

Opcode:


0x6C


Operation:


RS1 = RS1 - 1

IF RS1 != 0:
IP = Address


Example:


LOOP D1, Start


Equivalent:


D1--
if D1 != 0:
goto Start


---

# 5.23.2 LOOP ZERO

Opcode:


0x6D


Operation:


IF RS1 == 0:
IP = Address


Used for optimized zero checks.

---

# 5.24 Interrupt Control Instructions

Interrupt instructions allow the processor to communicate with hardware events.

---

# 5.24.1 ENABLE INTERRUPTS

Opcode:


0x70


Operation:


FLAGS.INT = 1


Allows hardware interrupts.

---

# 5.24.2 DISABLE INTERRUPTS

Opcode:


0x71


Operation:


FLAGS.INT = 0


Blocks hardware interrupts.

---

# 5.24.3 INTERRUPT RETURN

Opcode:


0x72


Operation:

Restores processor state after an interrupt.

Example:


IRET


Used by operating system kernels.

---

# 5.25 Exception Instructions

Exceptions handle abnormal processor conditions.

---

# 5.25.1 SOFTWARE INTERRUPT

Opcode:


0x73


Operation:


Generate Exception


Used for:

- System calls
- Debugging
- Kernel communication

Example:


INT 0x80


---

# 5.25.2 HALT

Opcode:


0x74


Operation:


Stop processor execution


The processor enters a low-power waiting state.

Used when:

- Operating system shuts down
- CPU has no tasks

---

# 5.25.3 WAIT

Opcode:


0x75


Operation:


Wait for interrupt


Processor pauses until an external event occurs.

---

# 5.26 Control Flow Instruction Summary

| Instruction | Opcode | Purpose |
|---|---|---|
| JMP | 0x60 | Absolute jump |
| JMPR | 0x61 | Register jump |
| CALL | 0x62 | Function call |
| RET | 0x63 | Return |
| BEQ | 0x64 | Branch equal |
| BNE | 0x65 | Branch not equal |
| BGT | 0x66 | Branch greater |
| BLT | 0x67 | Branch less |
| BGE | 0x68 | Branch greater/equal |
| BLE | 0x69 | Branch less/equal |
| BCS | 0x6A | Carry branch |
| BVS | 0x6B | Overflow branch |
| LOOP | 0x6C | Counter loop |
| LOOPZ | 0x6D | Zero loop |
| EI | 0x70 | Enable interrupts |
| DI | 0x71 | Disable interrupts |
| IRET | 0x72 | Interrupt return |
| INT | 0x73 | Software interrupt |
| HALT | 0x74 | Stop CPU |
| WAIT | 0x75 | Wait event |

---
# 5.27 System & Privileged Instructions

System instructions provide direct control over processor features.

These instructions are restricted to privileged execution modes and are primarily used by:

- Operating system kernels
- Hypervisors
- Hardware management software

User applications cannot execute privileged instructions.

Attempting to execute a privileged instruction without permission generates a protection exception.

---

# 5.27.1 CPU Privilege Modes

Doublers-64 supports multiple execution privilege levels.

| Mode | Name | Purpose |
|---|---|---|
| Mode 0 | Kernel Mode | Full hardware access |
| Mode 1 | Supervisor Mode | Operating system services |
| Mode 2 | User Mode | Applications |

The current privilege level is stored inside the processor status register.

---

# 5.27.2 MODE SWITCH

Opcode:


0x80


Operation:


Change CPU privilege level


Example:


MODE USER


Switches execution into user mode.

Only higher privilege levels can switch into lower privilege levels.

---

# 5.27.3 RETURN FROM PRIVILEGE CHANGE

Opcode:


0x81


Operation:


Restore previous privilege state


Used when returning from:

- System calls
- Interrupt handlers
- Exceptions

Example:


RMP


---

# 5.27.4 READ SYSTEM REGISTER

Opcode:


0x82


Operation:


RD = System_Register


Allows privileged software to read processor control information.

Examples:

- CPU identification
- Memory configuration
- Exception state

---

# 5.27.5 WRITE SYSTEM REGISTER

Opcode:


0x83


Operation:


System_Register = RD


Allows the kernel to configure processor features.

---

# 5.27.6 CACHE CONTROL

Opcode:


0x84


Controls processor cache behavior.

Operations:


CACHE FLUSH
CACHE INVALIDATE
CACHE ENABLE
CACHE DISABLE


Used by:

- Operating systems
- Device drivers
- Memory managers

---

# 5.27.7 TLB CONTROL

Opcode:


0x85


Controls the Translation Lookaside Buffer.

Supported operations:


TLB FLUSH
TLB INVALIDATE
TLB UPDATE


The TLB provides fast virtual memory translation.

---

# 5.27.8 MEMORY PROTECTION CONTROL

Opcode:


0x86


Controls memory access permissions.

Permissions include:


READ
WRITE
EXECUTE


Used to enforce:

- Process isolation
- Kernel protection
- Secure memory regions

---

# 5.27.9 PAGE TABLE UPDATE

Opcode:


0x87


Updates virtual memory mappings.

Operation:


Virtual Address → Physical Address


Used by operating system memory managers.

---

# 5.27.10 INTERRUPT VECTOR CONTROL

Opcode:


0x88


Changes the location of interrupt handling code.

Operation:


IVT = Address


The Interrupt Vector Table contains addresses of exception handlers.

---

# 5.27.11 DEBUG CONTROL

Opcode:


0x89


Controls processor debugging features.

Features:

- Hardware breakpoints
- Single-step execution
- Debug exceptions

---

# 5.27.12 CPU IDENTIFICATION

Opcode:


0x8A


Returns processor information.

Example output:


Architecture: Doublers-64
Version: X.Y
Extensions: Supported Features


---

# 5.27.13 POWER MANAGEMENT

Opcode:


0x8B


Controls CPU power states.

Supported states:


ACTIVE
IDLE
SLEEP
SHUTDOWN


---

# 5.28 Kernel Security Rules

Privileged instructions follow strict security rules.

## Rule 1

User programs cannot access hardware directly.

## Rule 2

Invalid privilege operations generate exceptions.

## Rule 3

Memory protection must always remain enabled when running user applications.

## Rule 4

The kernel controls:

- Memory mapping
- Interrupt handling
- Hardware access
- Process scheduling

---

# 5.29 System Instruction Summary

| Instruction | Opcode | Function |
|---|---|---|
| MODE | 0x80 | Change privilege mode |
| RMP | 0x81 | Return privilege state |
| RSYS | 0x82 | Read system register |
| WSYS | 0x83 | Write system register |
| CACHE | 0x84 | Cache control |
| TLB | 0x85 | TLB management |
| MEMPROT | 0x86 | Memory protection |
| PAGETABLE | 0x87 | Virtual memory update |
| IVT | 0x88 | Interrupt vector control |
| DEBUG | 0x89 | Debug control |
| CPUID | 0x8A | CPU information |
| POWER | 0x8B | Power management |

---

# Chapter 5 Completion Status

Implemented instruction groups:

✓ Arithmetic Instructions  
✓ Logical Instructions  
✓ Memory Instructions  
✓ Atomic Operations  
✓ Control Flow Instructions  
✓ Interrupt Instructions  
✓ Exception Instructions  
✓ Privileged System Instructions  

The Doublers-64 base instruction set is now complete.

Future chapters may define:

- Floating Point Extension
- Vector Extension
- Security Extension
- Virtual Machine Extension
- Debug Specification
- Assembly Language Specification

# Chapter 6: Execution Environment

## 6.1 Overview

The Execution Environment defines the operational behavior of the Doublers-64 processor.

It describes:

- Instruction execution
- CPU operating modes
- Pipeline behavior
- Exception handling
- Interrupt processing
- Boot sequence
- Processor state management

The Execution Environment ensures that software can reliably execute on all Doublers-64 compatible processors.

---

# 6.2 Processor Execution Model

Doublers-64 uses a sequential instruction execution model.

The processor follows this cycle:


FETCH → DECODE → EXECUTE → MEMORY → WRITEBACK


Each instruction passes through these stages.

---

# 6.3 Instruction Pipeline

The base Doublers-64 processor uses a five-stage pipeline.

## Stage 1: FETCH

Purpose:

Retrieve the next instruction from memory.

Operations:


Instruction Address = IP

Instruction = Memory[IP]

IP = IP + 4


The instruction is transferred to the instruction decoder.

---

## Stage 2: DECODE

Purpose:

Understand the instruction.

The decoder identifies:

- Opcode
- Destination register
- Source registers
- Immediate values
- Required execution unit

---

## Stage 3: EXECUTE

Purpose:

Perform the requested operation.

Examples:

Arithmetic:


ADD D1,D2,D3

D1 = D2 + D3


Branch:


JMP Address

IP = Address


---

## Stage 4: MEMORY ACCESS

Used only by memory instructions.

Examples:

LOAD:


Read RAM


STORE:


Write RAM


Instructions that do not access memory skip this stage.

---

## Stage 5: WRITEBACK

The final result is written into the destination register.

Example:


ALU Result → D1


---

# 6.4 Pipeline Hazards

Doublers-64 processors must handle pipeline conflicts.

There are three major hazard types.

---

# 6.4.1 Data Hazard

Occurs when one instruction depends on the result of another instruction.

Example:


ADD D1,D2,D3

SUB D4,D1,D5


The second instruction requires the result of the first.

Solutions:

- Pipeline forwarding
- Pipeline stall

---

# 6.4.2 Control Hazard

Occurs during jumps and branches.

Example:


BEQ LOOP


The processor may already have fetched incorrect instructions.

Solutions:

- Pipeline flushing
- Branch prediction

---

# 6.4.3 Memory Hazard

Occurs when multiple operations access memory simultaneously.

Solutions:

- Memory ordering rules
- Cache synchronization

---

# 6.5 Processor Operating Modes

Doublers-64 supports three privilege levels.

| Level | Name | Description |
|---|---|---|
| 0 | Kernel Mode | Complete hardware access |
| 1 | Supervisor Mode | OS services |
| 2 | User Mode | Applications |

---

# 6.5.1 Kernel Mode

Kernel Mode has unrestricted access.

Allowed:

- Hardware control
- Memory management
- Interrupt handling
- Device communication

Used by:

- Microkernel
- Hardware drivers
- Core system services

---

# 6.5.2 Supervisor Mode

Supervisor Mode provides controlled operating system access.

Used for:

- System services
- Resource management
- Protected operations

---

# 6.5.3 User Mode

User Mode is designed for applications.

Restrictions:

- Cannot execute privileged instructions
- Cannot access protected memory
- Cannot directly control devices

---

# 6.6 Processor State

The complete CPU state contains:

## General State


D0-D15


## Control State


IP
SP
BP
FLAGS


## System State


Privilege Level
Interrupt State
Memory Configuration
Exception Information


The operating system saves and restores this state during task switching.

---

# 6.7 Instruction Retirement

An instruction is considered completed when:

1. Execution finishes successfully
2. Memory operations complete
3. Result is written back
4. No exception occurs

Only retired instructions modify visible processor state.

---

# 6.8 Atomic Execution

Certain instructions must execute without interruption.

Atomic instructions include:

- LRES
- SC
- Memory synchronization operations

Atomic execution guarantees consistency in multi-core systems.

---

# 6.9 Execution Exceptions

If an instruction cannot complete normally, the processor generates an exception.

Examples:

- Invalid instruction
- Memory violation
- Division by zero
- Privilege violation
- Hardware failure

Exception handling is described in later sections.

---

# 6.10 Compatibility Requirements

Every Doublers-64 processor must:

- Execute all base ISA instructions
- Maintain register behavior
- Follow privilege rules
- Handle exceptions correctly
- Preserve software compatibility

Extensions may add features but cannot modify the behavior of existing instructions.

---

# Chapter 6 — Instruction Encoding

## 6.1 Overview

Instruction encoding defines how Doublers ISA instructions are represented within the Doublers Command Architecture (DCA).

Every compatible processor shall decode instructions according to this specification.

The exact physical implementation of DCA is hardware-defined, but the architectural meaning of every instruction shall remain identical across all compliant processors.

---

## 6.2 Instruction Format

Each Doublers instruction consists of one instruction followed by zero or more operands.

An instruction may contain:

* An opcode.
* One or more register operands.
* One or more immediate values.
* One or more memory addresses.

The required operands depend on the instruction.

---

## 6.3 Opcode

Every instruction shall possess a unique opcode.

The opcode uniquely identifies the operation to be performed by the processor.

Examples include:

* MOVE
* LOAD
* STORE
* ADD
* SUB
* JMP
* CALL
* RET

The official opcode assignments are defined in the Instruction Reference chapter.

---

## 6.4 Operands

Operands provide the data required by an instruction.

Supported operand types include:

* Registers
* Immediate values
* Memory addresses

Processors shall reject unsupported operand combinations.

---

## 6.5 Register Encoding

General-purpose registers shall be encoded according to the DCA specification.

Every processor shall recognize all sixteen Base ISA registers.

Future extensions may define additional register classes without modifying the Base ISA register encodings.

---

## 6.6 Immediate Values

Immediate values represent constant data embedded directly within an instruction.

The supported immediate sizes are implementation-defined by the DCA specification.

Processors shall correctly sign-extend or zero-extend immediate values where required by the instruction.

---

## 6.7 Memory Address Encoding

Memory operands identify locations within the processor address space.

Address encoding shall support the full 64-bit address space defined by the Base ISA.

---

## 6.8 Reserved Encodings

Certain opcode values and operand combinations are reserved.

Software shall not depend upon reserved encodings.

Future official or community extensions may assign meanings to reserved encodings while preserving compatibility with existing software.

---

## 6.9 Illegal Instructions

If a processor encounters an undefined or invalid instruction encoding, it shall generate an Illegal Instruction Exception.

Processor execution shall not continue with an undefined instruction.

---

## 6.10 Compatibility

Processors implementing the Doublers ISA shall interpret every instruction encoding according to this specification.

Alternative internal hardware implementations are permitted provided the externally visible architectural behavior remains identical.

---

## 6.11 Future Expansion

Future versions or compatible extensions may introduce additional instruction formats, operand types, or encoding mechanisms.

Such additions shall not change the behavior of existing Base ISA instructions.

# Chapter 7 — Base Instruction Set

## 7.1 Overview

The Base Instruction Set defines the mandatory instructions that every Doublers-compatible processor shall implement.

Every processor claiming compatibility with the Doublers Base ISA shall correctly execute all instructions defined in this chapter.

Instructions are organized into functional groups for clarity.

---

## 7.2 Instruction Categories

The Base ISA consists of the following instruction categories:

* Data Movement
* Arithmetic
* Logical Operations
* Comparison
* Control Flow
* Stack Operations
* System Instructions

Future extensions may introduce additional categories without altering the behavior of the Base ISA.

---

# 7.3 Data Movement Instructions

Data Movement instructions transfer data between registers, memory, and immediate values.

The Base ISA defines the following mandatory instructions:

* MOVE
* LOAD
* STORE

---

## 7.3.1 MOVE

### Purpose

Copies data from a source operand to a destination operand.

### Syntax

MOVE destination, source

### Operands

* Register → Register
* Register ← Immediate

### Description

The MOVE instruction copies the source value into the destination without modifying the source.

### Flags Affected

None.

### Exceptions

* Invalid Operand Exception
* Illegal Instruction Exception

### Example

MOVE D0, D1

MOVE D2, 100

---

## 7.3.2 LOAD

### Purpose

Loads data from memory into a register.

### Syntax

LOAD destination, address

### Description

The processor reads the value stored at the specified memory location and copies it into the destination register.

### Flags Affected

None.

### Exceptions

* Invalid Memory Address
* Access Violation
* Alignment Exception

### Example

LOAD D0, [0x1000]

---

## 7.3.3 STORE

### Purpose

Stores a register value into memory.

### Syntax

STORE address, source

### Description

The processor writes the source register value to the specified memory address.

### Flags Affected

None.

### Exceptions

* Invalid Memory Address
* Access Violation
* Alignment Exception

### Example

STORE [0x1000], D0

---

## 7.4 Compliance

Every Doublers-compatible processor shall implement all Data Movement instructions exactly as specified.

Alternative internal implementations are permitted provided the architectural behavior remains identical.
## 7.5 Arithmetic Instructions

Arithmetic instructions perform mathematical operations on register values and immediate values.

The Base ISA defines the following arithmetic instructions:

* ADD
* SUB
* MUL
* DIV
* MOD
* INC
* DEC
* NEG

---

## 7.5.1 ADD

### Purpose

Adds the source operand to the destination operand.

### Syntax

ADD destination, source

### Operands

* Register ← Register
* Register ← Immediate

### Description

The destination operand is replaced with the sum of the destination and source operands.

### Flags Affected

* Z (Zero)
* C (Carry)
* O (Overflow)
* N (Negative)

### Exceptions

* Invalid Operand Exception
* Arithmetic Overflow (implementation-defined)

### Example

ADD D0, D1

ADD D2, 10

---

## 7.5.2 SUB

### Purpose

Subtracts the source operand from the destination operand.

### Syntax

SUB destination, source

### Description

The destination operand is replaced with the result of the subtraction.

### Flags Affected

* Z
* C
* O
* N

### Example

SUB D3, D1

SUB D0, 5

---

## 7.5.3 MUL

### Purpose

Multiplies two operands.

### Syntax

MUL destination, source

### Description

The destination operand is replaced by the product of the multiplication.

### Flags Affected

* Z
* O
* N

### Example

MUL D1, D2

---

## 7.5.4 DIV

### Purpose

Divides the destination operand by the source operand.

### Syntax

DIV destination, source

### Description

The quotient replaces the destination operand.

### Flags Affected

* Z
* N

### Exceptions

* Divide By Zero Exception

### Example

DIV D0, D1

---

## 7.5.5 MOD

### Purpose

Computes the remainder after division.

### Syntax

MOD destination, source

### Description

The destination operand is replaced with the remainder.

### Exceptions

* Divide By Zero Exception

### Example

MOD D2, D3

---

## 7.5.6 INC

### Purpose

Increments the destination operand by one.

### Syntax

INC destination

### Description

Adds one to the destination operand.

### Flags Affected

* Z
* O
* N

### Example

INC D0

---

## 7.5.7 DEC

### Purpose

Decrements the destination operand by one.

### Syntax

DEC destination

### Description

Subtracts one from the destination operand.

### Flags Affected

* Z
* O
* N

### Example

DEC D5

---

## 7.5.8 NEG

### Purpose

Negates the destination operand.

### Syntax

NEG destination

### Description

Replaces the destination operand with its arithmetic negative.

### Flags Affected

* Z
* O
* N

### Example

NEG D7

---

## 7.5.9 Compliance

Every Doublers-compatible processor shall implement all arithmetic instructions exactly as specified.

Implementations may optimize execution internally, provided the architectural behavior remains identical.
## 7.6 Logical Instructions

Logical instructions perform bitwise operations on registers and immediate values.

Every Doublers-compatible processor shall implement the following logical instructions:

* AND
* OR
* XOR
* NOT
* SHL
* SHR
* ROL
* ROR

---

## 7.6.1 AND

### Purpose

Performs a bitwise AND operation.

### Syntax

AND destination, source

### Description

Each bit of the destination operand is logically ANDed with the corresponding bit of the source operand.

### Flags Affected

* Z
* N

### Example

AND D0, D1

AND D2, 0xFF

---

## 7.6.2 OR

### Purpose

Performs a bitwise OR operation.

### Syntax

OR destination, source

### Description

Each bit of the destination operand is logically ORed with the corresponding bit of the source operand.

### Flags Affected

* Z
* N

### Example

OR D0, D1

OR D4, 0x80

---

## 7.6.3 XOR

### Purpose

Performs a bitwise Exclusive OR operation.

### Syntax

XOR destination, source

### Description

Each bit of the destination operand is replaced with the Exclusive OR of the destination and source operands.

### Flags Affected

* Z
* N

### Example

XOR D0, D1

---

## 7.6.4 NOT

### Purpose

Performs a bitwise inversion.

### Syntax

NOT destination

### Description

Every bit in the destination operand is inverted.

### Flags Affected

* Z
* N

### Example

NOT D5

---

## 7.6.5 SHL

### Purpose

Shifts all bits to the left.

### Syntax

SHL destination, amount

### Description

Bits are shifted left by the specified amount.

Vacated bits are filled with zero.

### Flags Affected

* Z
* C
* N

### Example

SHL D0, 1

---

## 7.6.6 SHR

### Purpose

Shifts all bits to the right.

### Syntax

SHR destination, amount

### Description

Bits are shifted right by the specified amount.

Vacated bits are filled with zero.

### Flags Affected

* Z
* C
* N

### Example

SHR D2, 3

---

## 7.6.7 ROL

### Purpose

Rotates bits to the left.

### Syntax

ROL destination, amount

### Description

Bits shifted out of the most significant position re-enter at the least significant position.

### Flags Affected

* C

### Example

ROL D7, 1

---

## 7.6.8 ROR

### Purpose

Rotates bits to the right.

### Syntax

ROR destination, amount

### Description

Bits shifted out of the least significant position re-enter at the most significant position.

### Flags Affected

* C

### Example

ROR D3, 2

---

## 7.6.9 Compliance

Every Doublers-compatible processor shall implement all logical instructions exactly as defined in this section.

Hardware implementations may optimize execution internally provided the observable architectural behavior remains identical.
## 7.7 Comparison Instructions

Comparison instructions evaluate values without modifying the original operands. They update the FLAGS register, allowing subsequent control-flow instructions to make decisions.

The Base ISA defines the following comparison instructions:

* CMP
* TEST

---

## 7.7.1 CMP

### Purpose

Compares two operands by subtracting the source operand from the destination operand without storing the result.

### Syntax

CMP destination, source

### Operands

* Register ↔ Register
* Register ↔ Immediate

### Description

The processor performs an internal subtraction to determine the relationship between the operands.

The destination operand is **not** modified.

The comparison result is reflected only through the FLAGS register.

### Flags Affected

* Z (Zero)
* C (Carry)
* O (Overflow)
* N (Negative)

### Exceptions

* Invalid Operand Exception
* Illegal Instruction Exception

### Example

CMP D0, D1

CMP D2, 100

---

## 7.7.2 TEST

### Purpose

Performs a bitwise AND operation without modifying either operand.

### Syntax

TEST destination, source

### Operands

* Register ↔ Register
* Register ↔ Immediate

### Description

The processor performs an internal bitwise AND operation.

The result is discarded after updating the FLAGS register.

This instruction is commonly used to determine whether specific bits are set.

### Flags Affected

* Z (Zero)
* N (Negative)

### Exceptions

* Invalid Operand Exception
* Illegal Instruction Exception

### Example

TEST D0, D1

TEST D4, 0x80

---

## 7.7.3 Compliance

Every Doublers-compatible processor shall implement comparison instructions exactly as specified.

Comparison instructions shall never modify the values of their operands.

Only the FLAGS register may be updated as a result of executing comparison instructions.
## 7.8 Control Flow Instructions

Control Flow instructions alter the normal sequential execution of a program.

Unless modified by a Control Flow instruction, the Instruction Pointer (IP) shall advance to the next sequential instruction.

The Base ISA defines the following Control Flow instructions:

* JMP
* JE
* JNE
* JG
* JL
* JGE
* JLE
* CALL
* RET

---

## 7.8.1 JMP

### Purpose

Transfers program execution to a specified address without evaluating any condition.

### Syntax

JMP target

### Description

The Instruction Pointer (IP) is replaced with the specified target address.

Execution continues from the target instruction.

### Flags Affected

None.

### Exceptions

* Invalid Target Address
* Illegal Instruction Exception

### Example

JMP Loop

JMP 0x400000

---

## 7.8.2 JE (Jump if Equal)

### Purpose

Transfers execution if the Zero Flag (Z) is set.

### Syntax

JE target

### Description

If the Zero Flag equals one, execution continues at the target address.

Otherwise, execution proceeds with the next sequential instruction.

### Flags Affected

None.

### Example

CMP D0, D1

JE EqualLabel

---

## 7.8.3 JNE (Jump if Not Equal)

### Purpose

Transfers execution if the Zero Flag is clear.

### Syntax

JNE target

### Description

The jump is taken only when the Zero Flag equals zero.

### Flags Affected

None.

### Example

CMP D0, D1

JNE NotEqual

---

## 7.8.4 JG (Jump if Greater)

### Purpose

Transfers execution if the previous comparison indicates the destination operand is greater than the source operand.

### Syntax

JG target

### Description

The processor evaluates the FLAGS register according to the comparison rules defined by the ISA.

### Flags Affected

None.

### Example

CMP D0, D1

JG Greater

---

## 7.8.5 JL (Jump if Less)

### Purpose

Transfers execution if the previous comparison indicates the destination operand is less than the source operand.

### Syntax

JL target

### Description

The processor evaluates the FLAGS register according to the comparison rules defined by the ISA.

### Flags Affected

None.

### Example

CMP D0, D1

JL Smaller

---

## 7.8.6 JGE (Jump if Greater or Equal)

### Purpose

Transfers execution if the previous comparison indicates the destination operand is greater than or equal to the source operand.

### Syntax

JGE target

### Description

Execution branches only when the comparison satisfies the required condition.

### Flags Affected

None.

### Example

CMP D0, D1

JGE Continue

---

## 7.8.7 JLE (Jump if Less or Equal)

### Purpose

Transfers execution if the previous comparison indicates the destination operand is less than or equal to the source operand.

### Syntax

JLE target

### Description

Execution branches only when the comparison satisfies the required condition.

### Flags Affected

None.

### Example

CMP D0, D1

JLE Exit

---

## 7.8.8 CALL

### Purpose

Invokes a subroutine.

### Syntax

CALL target

### Description

The processor stores the return address on the stack before transferring execution to the specified target.

Execution returns when the RET instruction is executed.

### Flags Affected

None.

### Exceptions

* Stack Overflow
* Invalid Target Address

### Example

CALL PrintMessage

---

## 7.8.9 RET

### Purpose

Returns from a previously invoked subroutine.

### Syntax

RET

### Description

The processor retrieves the saved return address from the stack and resumes execution at that location.

### Flags Affected

None.

### Exceptions

* Stack Underflow
* Invalid Return Address

### Example

RET

---

## 7.8.10 Compliance

Every Doublers-compatible processor shall implement all Control Flow instructions exactly as specified.

Conditional branch instructions shall evaluate only the architectural FLAGS register.

CALL and RET shall preserve correct subroutine execution semantics across all compliant processors.
## 7.9 Stack Instructions

Stack instructions manipulate the current execution stack.

The Stack Pointer (SP) shall always identify the top of the active stack.

The Base ISA defines the following stack instructions:

* PUSH
* POP

---

## 7.9.1 PUSH

### Purpose

Pushes an operand onto the current stack.

### Syntax

PUSH source

### Operands

* Register
* Immediate Value

### Description

The processor decreases the Stack Pointer (SP) by the size of the pushed operand and stores the operand at the new stack location.

### Flags Affected

None.

### Exceptions

* Stack Overflow
* Invalid Memory Access
* Stack Protection Violation

### Example

PUSH D0

PUSH 100

---

## 7.9.2 POP

### Purpose

Removes the top value from the stack.

### Syntax

POP destination

### Operands

* Register

### Description

The processor reads the value at the current top of the stack into the destination register and then increases the Stack Pointer (SP).

### Flags Affected

None.

### Exceptions

* Stack Underflow
* Invalid Memory Access
* Stack Protection Violation

### Example

POP D0

---

## 7.9.3 Stack Behavior

The Doublers Base ISA defines a downward-growing stack.

During a PUSH operation:

1. The Stack Pointer is decremented.
2. The operand is written to the new stack location.

During a POP operation:

1. The value at the current stack location is read.
2. The Stack Pointer is incremented.

Software shall not assume any additional stack behavior beyond that defined by the Base ISA.

---

## 7.9.4 Compliance

Every Doublers-compatible processor shall implement PUSH and POP exactly as specified.

Implementations may optimize stack accesses internally, provided the architectural behavior remains identical.
## 7.10 System Instructions

System Instructions provide processor control, operating system interaction, and execution management.

Certain System Instructions are privileged and may only be executed while the processor is operating in Kernel Mode.

Attempting to execute a privileged instruction in User Mode shall generate a Privilege Exception.

The Base ISA defines the following System Instructions:

* NOP
* HALT
* SYSCALL
* SYSRET
* BREAK
* WAIT

---

## 7.10.1 NOP

### Purpose

Performs no operation.

### Syntax

NOP

### Description

The processor advances to the next instruction without modifying registers, memory, or processor state.

### Flags Affected

None.

### Exceptions

None.

### Example

NOP

---

## 7.10.2 HALT

### Purpose

Stops processor execution until an interrupt, reset, or implementation-defined wake event occurs.

### Syntax

HALT

### Description

The processor enters a halted state.

### Flags Affected

None.

### Exceptions

None.

### Example

HALT

---

## 7.10.3 SYSCALL

### Purpose

Requests a service from the operating system.

### Syntax

SYSCALL

### Description

The processor transfers execution from User Mode to Kernel Mode.

Control passes to the operating system's system call handler.

The mechanism used to identify the requested service is defined by the operating system ABI and is not specified by the Base ISA.

### Flags Affected

None.

### Exceptions

* Invalid System Call
* Privilege Exception (implementation-defined)

### Example

SYSCALL

---

## 7.10.4 SYSRET

### Purpose

Returns execution from Kernel Mode to User Mode following completion of a system call.

### Syntax

SYSRET

### Description

The processor restores the user execution context and resumes execution at the saved return address.

SYSRET is a privileged instruction.

### Flags Affected

None.

### Exceptions

* Invalid Return Context
* Privilege Exception

### Example

SYSRET

---

## 7.10.5 BREAK

### Purpose

Generates a software breakpoint.

### Syntax

BREAK

### Description

Execution is transferred to the debugger or operating system exception handler.

If no debugger is present, platform-defined behavior shall occur.

### Flags Affected

None.

### Exceptions

* Breakpoint Exception

### Example

BREAK

---

## 7.10.6 WAIT

### Purpose

Places the processor in a low-power waiting state until an interrupt or implementation-defined event occurs.

### Syntax

WAIT

### Description

The processor temporarily suspends instruction execution while remaining capable of responding to interrupts.

### Flags Affected

None.

### Exceptions

None.

### Example

WAIT

---

## 7.10.7 Compliance

Every Doublers-compatible processor shall implement all mandatory System Instructions exactly as specified.

Privileged instructions shall generate a Privilege Exception if executed outside Kernel Mode.

Implementations may introduce additional system instructions through compatible extensions, provided they do not alter the architectural behavior defined in this chapter.

# Chapter 8 — Interrupts and Exceptions

## 8.1 Overview

Interrupts and Exceptions provide a controlled mechanism for altering the normal execution flow of a Doublers-compatible processor.

An interrupt is generated by an external or asynchronous event.

An exception is generated internally during instruction execution.

Every compliant processor shall support both mechanisms.

---

## 8.2 Interrupt Types

The Base ISA defines two interrupt categories.

### Hardware Interrupts

Hardware Interrupts originate from external devices.

Examples include:

* Timer events
* Keyboard input
* Storage devices
* Network interfaces
* Platform-defined peripherals

---

### Software Interrupts

Software Interrupts are intentionally generated by software.

Typical uses include:

* Operating system requests
* Debugging
* Runtime services

---

## 8.3 Exceptions

Exceptions are generated automatically by the processor.

The Base ISA defines the following exception classes.

* Illegal Instruction
* Divide By Zero
* Invalid Memory Access
* Alignment Fault
* Stack Overflow
* Stack Underflow
* Privilege Exception
* Breakpoint Exception

Future extensions may define additional exception classes.

---

## 8.4 Exception Processing

When an exception occurs, the processor shall:

1. Complete any architecturally required state updates.
2. Save the current execution context.
3. Transfer execution to the appropriate exception handler.
4. Resume execution or terminate execution according to operating system policy.

---

## 8.5 Interrupt Processing

When an interrupt is accepted, the processor shall:

1. Preserve the required execution context.
2. Transfer execution to the interrupt handler.
3. Execute the handler.
4. Restore the saved context.
5. Resume execution.

---

## 8.6 Priority

If multiple interrupts or exceptions occur simultaneously, processor-specific priority rules shall determine the servicing order.

Exceptions directly related to the currently executing instruction shall take precedence over pending external interrupts unless otherwise specified.

---

## 8.7 Interrupt Vector Table

Each compatible processor shall provide an Interrupt Vector Table.

The operating system shall initialize this table during system startup.

Each entry shall identify the handler associated with a specific interrupt or exception.

The exact memory location of the Interrupt Vector Table is platform-defined.

---

## 8.8 Compliance

Every Doublers-compatible processor shall correctly detect, report, and process all mandatory interrupt and exception conditions defined by the Base ISA.

Alternative internal implementations are permitted provided the externally visible architectural behavior remains identical.

# Chapter 9 — Boot and Processor Initialization

## 9.1 Overview

This chapter defines the processor state immediately following reset and the minimum initialization requirements for a Doublers-compatible processor.

Every compatible implementation shall begin execution in a well-defined architectural state.

---

## 9.2 Reset

A processor reset returns the processor to its initial execution state.

A reset may be caused by:

* Power-on.
* External reset signal.
* Platform-defined reset event.
* Watchdog timeout.

Following reset, the processor shall begin execution at the Reset Vector.

---

## 9.3 Reset Vector

The Reset Vector specifies the address of the first instruction executed after reset.

The exact address is platform-defined.

Processors shall begin fetching instructions from the Reset Vector immediately after completing reset initialization.

---

## 9.4 Initial Processor State

Immediately after reset:

* The processor shall enter Kernel Mode.
* Interrupts shall be disabled.
* The Instruction Pointer (IP) shall contain the Reset Vector.
* The FLAGS register shall contain its implementation-defined reset value.
* General-purpose registers shall contain implementation-defined values unless otherwise specified by the platform.

Software shall not rely upon the contents of general-purpose registers after reset.

---

## 9.5 Boot Firmware

A Doublers-compatible platform may include boot firmware.

The responsibilities of the firmware may include:

* Processor initialization.
* Memory initialization.
* Hardware discovery.
* Loading the operating system.
* Passing platform information to the operating system.

The firmware interface is platform-defined and is not specified by the Base ISA.

---

## 9.6 Transition to Operating System

After completing platform initialization, control shall be transferred to the operating system entry point.

The operating system assumes responsibility for:

* Interrupt configuration.
* Memory management.
* Device initialization.
* Process management.
* System services.

---

## 9.7 Processor Modes

At minimum, every compatible processor shall support:

* Kernel Mode
* User Mode

Additional execution modes may be implemented through compatible extensions.

---

## 9.8 Boot Requirements

A compatible processor shall:

* Correctly initialize architectural registers.
* Begin execution at the Reset Vector.
* Enter Kernel Mode after reset.
* Support execution of Base ISA instructions immediately following initialization.

---

## 9.9 Compliance

A processor is compliant with this chapter if it correctly performs all mandatory initialization and boot behavior defined by this specification.

Platform-specific firmware behavior shall not alter the architectural guarantees established by the Base ISA.

# Chapter 10 — Processor Compliance and Compatibility

## 10.1 Overview

This chapter defines the requirements a processor shall satisfy in order to claim compatibility with the Doublers Base ISA.

Only processors implementing all mandatory architectural requirements may describe themselves as "Doublers Compatible."

---

## 10.2 Mandatory Components

Every Doublers-compatible processor shall implement:

* The Doublers Base ISA.
* The Doublers Command Architecture (DCA).
* Sixteen general-purpose registers.
* All mandatory special-purpose registers.
* The Base memory model.
* Interrupt and exception handling.
* Kernel Mode and User Mode.

---

## 10.3 Instruction Support

Every mandatory instruction defined by the Base ISA shall be implemented.

A processor shall not omit or redefine the architectural behavior of any mandatory instruction.

Optional extensions may introduce additional instructions provided they remain compatible with the Base ISA.

---

## 10.4 Register Compatibility

Processors shall implement all Base ISA registers exactly as defined.

The size, behavior, and accessibility of architectural registers shall remain compatible across all compliant implementations.

---

## 10.5 DCA Compatibility

Every compatible processor shall correctly decode and execute DCA command streams according to the DCA specification.

Alternative internal hardware designs are permitted provided the processor presents the same architectural behavior.

---

## 10.6 Software Compatibility

Software written exclusively for the Doublers Base ISA shall execute correctly on every Doublers-compatible processor.

Applications shall not depend upon implementation-specific behavior unless explicitly documented by the platform.

---

## 10.7 Extensions

Processors may support optional architectural extensions.

Each supported extension shall be uniquely identified.

Applications requiring an extension shall verify its availability before use.

Extensions shall not alter the defined behavior of the Base ISA.

---

## 10.8 Version Identification

Every compatible processor shall report:

* Supported Doublers ISA version.
* Supported DCA version.
* Supported architectural extensions.
* Implementation identifier.

The mechanism used to retrieve this information is defined elsewhere in this specification.

---

## 10.9 Reserved Behavior

Behavior not explicitly defined by this specification is considered implementation-defined.

Software shall not rely upon implementation-defined behavior for portability.

---

## 10.10 Compliance

A processor shall be considered Doublers-compatible only if it satisfies every mandatory requirement defined by this specification.

Failure to implement any required architectural feature shall prevent the processor from claiming full compatibility with the Doublers Base ISA.

# Chapter 11 — Application Binary Interface (ABI)

## 11.1 Overview

The Application Binary Interface (ABI) defines the standard interface used by software components executing on the Doublers ISA.

Although the Doublers Command Architecture (DCA) does not use traditional binary instruction encoding, all compatible software shall follow a common Application Binary Interface to ensure interoperability.

The ABI defines how functions exchange data, preserve registers, access the stack, and return control to callers.

---

## 11.2 Objectives

The Doublers ABI is designed to provide:

* Software compatibility.
* Predictable function behavior.
* Compiler interoperability.
* Operating system compatibility.
* Future architectural expansion.

---

## 11.3 Function Calls

Functions shall be invoked using the CALL instruction.

Execution shall return using the RET instruction.

The caller shall provide arguments according to the calling convention defined by this specification.

---

## 11.4 Parameter Passing

Arguments may be passed using:

* General-purpose registers.
* Stack memory.

The Base ABI recommends passing the first arguments through registers whenever possible.

Additional arguments shall be placed on the stack.

---

## 11.5 Return Values

Functions shall return values through designated return registers.

If multiple values are returned, additional registers or memory locations may be used according to the ABI.

---

## 11.6 Register Preservation

General-purpose registers are divided into two categories:

* Caller-saved registers.
* Callee-saved registers.

Functions shall preserve all callee-saved registers before modifying them.

Caller-saved registers may be freely modified by called functions.

The complete register classification is defined elsewhere in this specification.

---

## 11.7 Stack Alignment

The Stack Pointer shall remain aligned according to the Base ABI requirements before every function call.

Software shall not intentionally violate stack alignment.

---

## 11.8 Program Entry

Every executable program begins execution at its designated entry point.

The operating system or boot environment transfers control to this entry point after completing program loading.

The exact loading mechanism is platform-defined.

---

## 11.9 Compatibility

Software conforming to this ABI shall execute correctly on every Doublers-compatible implementation supporting the same ISA version.

Implementations shall not alter the externally visible ABI behavior.

---

## 11.10 Future Expansion

Future versions of the ABI may introduce additional calling conventions, register classes, or optimization mechanisms.

Such additions should preserve compatibility with existing software whenever practical.

# Chapter 12 — Memory Protection and Privilege Model

## 12.1 Overview

The Doublers ISA defines a memory protection model to ensure reliable and secure execution of software.

Memory protection prevents unauthorized access to memory regions and enables operating systems to isolate applications from one another.

Every Doublers-compatible processor shall implement the architectural behavior defined in this chapter.

---

## 12.2 Privilege Levels

The Base ISA defines two mandatory privilege levels.

* Kernel Mode
* User Mode

Kernel Mode provides unrestricted access to processor resources.

User Mode provides restricted execution suitable for applications.

Future ISA extensions may define additional privilege levels.

---

## 12.3 Memory Access Permissions

Memory regions may define one or more of the following permissions:

* Read
* Write
* Execute

Processors shall generate a Memory Protection Exception if software attempts an operation not permitted by the active memory permissions.

---

## 12.4 Execute Protection

Memory marked as non-executable shall not be used as an instruction source.

Attempting to execute instructions from a non-executable region shall generate an Execute Protection Exception.

---

## 12.5 User Mode Restrictions

Software executing in User Mode shall not:

* Execute privileged instructions.
* Modify privileged processor registers.
* Access Kernel-only memory.
* Disable memory protection.
* Modify interrupt configuration.

Violations shall generate a Privilege Exception.

---

## 12.6 Kernel Mode Capabilities

Kernel Mode software may:

* Access all memory regions.
* Execute privileged instructions.
* Configure processor registers.
* Modify memory protection structures.
* Control interrupt handling.

The operating system is responsible for maintaining system integrity while operating in Kernel Mode.

---

## 12.7 Memory Isolation

Operating systems should isolate independent software components by assigning separate protected memory regions.

Processors shall enforce memory permissions according to the active execution context.

---

## 12.8 Fault Handling

When a protection violation occurs, the processor shall:

1. Detect the violation.
2. Preserve the required execution context.
3. Generate the appropriate exception.
4. Transfer execution to the operating system's exception handler.

---

## 12.9 Compatibility

Every Doublers-compatible processor shall implement the memory protection mechanisms defined in this chapter.

Alternative implementation techniques are permitted provided they preserve the architectural behavior.

---

## 12.10 Future Expansion

Future ISA revisions may introduce additional protection mechanisms, privilege levels, or memory permission types.

Such additions should maintain compatibility with software written for earlier versions of the Doublers Base ISA whenever practical.

# Chapter 13 — Debugging and Performance Monitoring

## 13.1 Overview

The Doublers ISA defines a standard debugging and performance monitoring interface to support software development, operating system debugging, and hardware validation.

Every Doublers-compatible processor shall implement the mandatory architectural behavior defined in this chapter.

---

## 13.2 Design Goals

The debugging architecture is intended to provide:

* Reliable software debugging.
* Hardware diagnostics.
* Operating system development support.
* Performance analysis.
* Processor validation.

---

## 13.3 Breakpoints

Processors shall support software breakpoints through the BREAK instruction.

Hardware breakpoints may be implemented as an optional architectural extension.

When a breakpoint is encountered, the processor shall generate a Breakpoint Exception.

---

## 13.4 Watchpoints

Processors may support watchpoints.

Watchpoints monitor selected memory locations for:

* Read operations.
* Write operations.
* Execute operations.

When a watched event occurs, the processor shall generate a Watchpoint Exception.

Support for watchpoints is implementation-defined.

---

## 13.5 Single-Step Execution

Processors shall support single-step execution for debugging purposes.

When enabled, the processor shall generate a Debug Exception after completing each instruction.

---

## 13.6 Debug Registers

Processors may implement dedicated Debug Registers.

These registers may be used to configure:

* Breakpoints.
* Watchpoints.
* Debug control.
* Debug status.

The number and organization of Debug Registers are implementation-defined.

---

## 13.7 Performance Counters

Processors may provide performance monitoring counters.

Typical counters include:

* Instructions executed.
* Cycles elapsed.
* Branch instructions.
* Memory accesses.
* Cache events (if applicable).

Performance counters shall not alter normal program execution.

---

## 13.8 Trace Support

Implementations may provide instruction tracing capabilities.

Trace support may record:

* Executed instructions.
* Branch decisions.
* Exceptions.
* Interrupts.

The trace mechanism is implementation-defined.

---

## 13.9 Debug Security

Operating systems shall control access to debugging facilities.

User Mode software shall not modify privileged debugging resources without operating system authorization.

Unauthorized access attempts shall generate a Privilege Exception.

---

## 13.10 Compliance

Every Doublers-compatible processor shall correctly implement all mandatory debugging behavior defined by this specification.

Optional debugging facilities shall not modify the architectural behavior of the Base ISA.

---

## 13.11 Future Expansion

Future ISA revisions may define additional debugging mechanisms, performance monitoring capabilities, and trace facilities while maintaining compatibility with existing software.

# Chapter 14 — Compatibility and Community Additions

## 14.1 Overview

The Doublers ISA is a source-available architecture intended to encourage experimentation, research, and processor development.

Future additions may be created by the community provided they preserve compatibility with the Doublers Base ISA.

---

## 14.2 Design Goals

Community additions are intended to provide:

* New processor capabilities.
* Research opportunities.
* Hardware innovation.
* Software compatibility.
* Long-term architectural growth.

---

## 14.3 Base ISA Preservation

The Doublers Base ISA shall remain unchanged.

Existing instructions, registers, exceptions, and architectural behavior defined by the Base ISA shall not be modified.

Software written for the Base ISA should continue to operate correctly on compatible processors.

---

## 14.4 Community Additions

Developers may create additional instructions, registers, or processor capabilities.

Community additions should:

* Clearly document all new functionality.
* Preserve Base ISA behavior.
* Avoid redefining existing instructions.
* State any compatibility requirements.

---

## 14.5 Processor Compatibility

A processor implementing additional capabilities may still describe itself as Doublers-compatible if every mandatory Base ISA feature operates exactly as defined by this specification.

Additional functionality shall supplement, not replace, the Base ISA.

---

## 14.6 Software Compatibility

Software designed exclusively for the Base ISA should execute correctly on processors implementing compatible community additions.

Software requiring additional features should verify their availability before use.

---

## 14.7 Documentation

Every published community addition should include:

* Name
* Version
* Purpose
* Added instructions
* Added registers (if applicable)
* Compatibility information
* Implementation notes

---

## 14.8 Version Identification

Processors should provide a mechanism for software to identify:

* Supported Doublers ISA version.
* Supported DCA version.
* Available community additions.

The exact identification mechanism is implementation-defined.

---

## 14.9 Compatibility Requirements

Community additions shall not:

* Modify existing Base ISA instructions.
* Change register behavior.
* Alter exception handling.
* Break software written for the Base ISA.

Processors that violate these requirements shall not claim compatibility with the Doublers Base ISA.

---

## 14.10 Future Growth

The Doublers architecture is intended to evolve through documented, compatible community additions.

The Base ISA serves as the stable architectural foundation upon which future innovations may be developed.

# Chapter 15 — Processor Identification

## 15.1 Overview

Every Doublers-compatible processor shall provide a standardized mechanism for software to identify the processor implementation and supported architectural features.

Processor identification enables operating systems, development tools, and applications to determine the capabilities of the executing processor.

---

## 15.2 Identification Objectives

Processor identification is intended to provide:

* ISA version identification.
* DCA version identification.
* Processor implementation identification.
* Community addition discovery.
* Software compatibility verification.

---

## 15.3 Required Information

A compatible processor shall make the following information available:

* Processor Vendor Name
* Processor Model Name
* Doublers ISA Version
* Supported DCA Version
* Processor Revision
* Supported Community Additions

The retrieval mechanism is implementation-defined.

---

## 15.4 Processor Vendor

Processor vendors may identify themselves using a unique vendor string.

Examples include:

* Independent hardware developers.
* Educational projects.
* Commercial processor manufacturers.
* Research organizations.

The Base ISA does not reserve vendor names.

---

## 15.5 Processor Model

Each processor implementation should provide a human-readable model identifier.

Model identifiers assist software developers when diagnosing compatibility issues.

---

## 15.6 Version Reporting

Processors shall accurately report:

* Implemented Doublers ISA version.
* Implemented DCA version.
* Processor revision.

Software shall not assume compatibility with newer ISA versions unless explicitly reported.

---

## 15.7 Community Addition Reporting

If community additions are implemented, processors should provide a mechanism for software to determine their availability.

Software should verify support before attempting to use additional features.

---

## 15.8 Compatibility Verification

Operating systems and software may compare reported processor capabilities against their requirements before execution.

Processors shall report their capabilities accurately.

---

## 15.9 Future Growth

Future versions of the Doublers architecture may define additional processor identification fields.

New identification fields should remain compatible with software written for earlier ISA versions.

---

## 15.10 Compliance

Every Doublers-compatible processor shall implement the mandatory processor identification requirements defined in this chapter.

Implementation-specific identification fields may be added provided they do not conflict with the Base ISA.

# Chapter 16 — Architectural Limits

## 16.1 Overview

This chapter defines the architectural limits guaranteed by the Doublers Base ISA.

All compatible processors shall satisfy the minimum requirements defined in this chapter.

Processors may exceed these limits through compatible community additions.

---

## 16.2 Register Width

The Doublers Base ISA defines a 64-bit architecture.

General-purpose registers shall be 64 bits wide.

Future compatible processors may internally use wider registers provided Base ISA behavior remains unchanged.

---

## 16.3 Address Space

The Base ISA supports a 64-bit virtual address space.

The physically implemented address space is implementation-defined.

Processors may implement fewer physical address bits provided software-visible behavior remains compatible.

---

## 16.4 Instruction Length

Instruction representation is defined by the Doublers Command Architecture (DCA).

Processors shall correctly decode every valid instruction defined by the Base ISA.

The internal implementation of instruction decoding is processor-defined.

---

## 16.5 Register Count

Every compatible processor shall implement:

* Sixteen General-Purpose Registers.
* Mandatory Special-Purpose Registers.
* Mandatory Status Registers.

Additional registers may be introduced through compatible community additions.

---

## 16.6 Privilege Levels

The Base ISA requires support for:

* Kernel Mode
* User Mode

Additional privilege levels may be introduced through compatible community additions.

---

## 16.7 Interrupt Support

Every compatible processor shall support:

* Hardware Interrupts.
* Software Interrupts.
* Architectural Exceptions.

Additional interrupt mechanisms may be introduced through compatible community additions.

---

## 16.8 Processor Frequency

The Doublers Base ISA places no restrictions upon processor clock frequency.

Processor performance is implementation-defined.

Software shall not depend upon any specific execution speed.

---

## 16.9 Scalability

The architecture is intended to support implementations ranging from educational processors to high-performance processors.

Implementation complexity is left to processor designers provided compatibility with the Base ISA is maintained.

---

## 16.10 Compliance

A processor is considered compliant with this chapter if it satisfies every mandatory architectural limit defined by the Doublers Base ISA.

Processors exceeding these limits shall remain compatible with Base ISA software whenever practical.

# Chapter 17 — Reserved Architecture Space

## 17.1 Overview

The Doublers Base ISA reserves portions of the architecture for future compatibility and controlled expansion.

Reserved architectural space shall not be used by Base ISA software.

Processors shall treat reserved architectural elements according to this specification.

---

## 17.2 Reserved Instructions

Instruction encodings not assigned by the Base ISA are considered reserved.

Execution of a reserved instruction shall generate an Illegal Instruction Exception unless otherwise defined by a compatible community addition.

---

## 17.3 Reserved Registers

Register identifiers not assigned by the Base ISA are reserved.

Software shall not assume the existence or behavior of reserved registers.

Compatible community additions may define additional registers without modifying the Base ISA register definitions.

---

## 17.4 Reserved System Resources

The following architectural resources may contain reserved fields:

* Status Registers
* Control Registers
* Processor Identification Structures
* Future Architectural Structures

Reserved fields shall retain their defined values unless otherwise specified by a compatible community addition.

---

## 17.5 Reserved Exception Codes

Exception identifiers not defined by the Base ISA are reserved.

Future compatible additions may assign meanings to reserved exception identifiers.

---

## 17.6 Reserved Interrupt Vectors

Interrupt vectors not defined by the Base ISA are reserved for future expansion.

Software shall not depend upon reserved interrupt vectors.

---

## 17.7 Forward Compatibility

Processors shall preserve reserved architectural space to maintain compatibility with future revisions and compatible community additions.

Software shall not depend upon the behavior of any reserved architectural element.

---

## 17.8 Compliance

Every Doublers-compatible processor shall correctly preserve and protect reserved architectural space as defined by this specification.

Implementations shall not assign conflicting meanings to reserved architectural elements while claiming compatibility with the Doublers Base ISA.

# Chapter 18 — Architectural Compliance Testing

## 18.1 Overview

Architectural Compliance Testing verifies that a processor correctly implements the Doublers Base ISA and the Doublers Command Architecture (DCA).

A processor claiming compatibility with the Doublers architecture shall successfully pass all mandatory compliance requirements.

---

## 18.2 Objectives

Compliance testing is intended to verify:

* Correct instruction execution.
* Register behavior.
* Memory operations.
* Interrupt handling.
* Exception handling.
* Processor initialization.
* Privilege transitions.
* DCA command decoding.

---

## 18.3 Compliance Requirements

A compliant processor shall correctly execute every mandatory feature defined by the Base ISA.

Partial implementations shall not claim full compatibility.

Processors implementing additional features shall remain compatible with all mandatory Base ISA behavior.

---

## 18.4 Test Categories

Compliance tests should include:

* Instruction Tests
* Register Tests
* Memory Tests
* Stack Tests
* Interrupt Tests
* Exception Tests
* Privilege Tests
* DCA Decoder Tests

Additional implementation-specific tests may be included.

---

## 18.5 Processor Verification

Processor designers should verify:

* Every instruction produces the correct result.
* FLAGS register updates correctly.
* Memory permissions are enforced.
* Exceptions are correctly generated.
* Interrupt handling behaves according to specification.
* Processor reset behavior matches the architecture.

---

## 18.6 DCA Verification

Implementations shall correctly decode every valid DCA command defined by the Base DCA specification.

Invalid command representations shall generate the appropriate architectural exception.

---

## 18.7 Compatibility Verification

Processors successfully completing compliance testing may describe themselves as:

"Compatible with the Doublers Base ISA."

Processors implementing compatible community additions may additionally describe those supported additions.

---

## 18.8 Future Test Suites

Future versions of the Doublers project may publish standardized compliance test suites.

Passing future test suites shall not replace compliance with the Base ISA specification.

---

## 18.9 Compliance

Compliance testing verifies implementation correctness.

Passing a compliance test suite does not guarantee identical processor performance or internal implementation.

Only architectural behavior is evaluated.

# Chapter 19 — Conformance Requirements

## 19.1 Overview

This chapter defines the requirements for software, processors, tools, and documentation claiming compatibility with the Doublers Base ISA.

Conformance ensures that independently developed implementations behave consistently across the Doublers ecosystem.

---

## 19.2 Processor Conformance

A processor claiming compatibility with the Doublers Base ISA shall:

* Implement all mandatory architectural features.
* Correctly implement the Doublers Command Architecture (DCA).
* Preserve the behavior of all mandatory instructions.
* Correctly implement mandatory exceptions.
* Correctly implement mandatory privilege levels.

Processors shall not redefine existing Base ISA behavior.

---

## 19.3 Software Conformance

Software claiming Base ISA compatibility shall:

* Use only instructions defined by the Base ISA unless additional requirements are explicitly documented.
* Avoid relying on implementation-defined behavior.
* Correctly follow the Doublers ABI.

---

## 19.4 Toolchain Conformance

Assemblers, compilers, translators, simulators, and related development tools shall generate or interpret Doublers programs according to this specification.

Tools shall not intentionally generate undefined instruction behavior while claiming Base ISA compatibility.

---

## 19.5 Documentation Conformance

Documentation describing processors or software shall accurately identify:

* Supported Doublers ISA version.
* Supported DCA version.
* Required community additions (if any).

Documentation shall not claim unsupported architectural features.

---

## 19.6 Community Addition Conformance

Community additions claiming compatibility with the Doublers ecosystem shall:

* Preserve all Base ISA behavior.
* Clearly document added functionality.
* State compatibility requirements.
* Avoid redefining existing architectural behavior.

---

## 19.7 Compatibility Claims

Products may describe themselves as:

* "Doublers Base ISA Compatible"
* "Doublers DCA Compatible"

only if they satisfy every mandatory requirement defined by the applicable specification.

False compatibility claims are discouraged.

---

## 19.8 Future Revisions

Future revisions of the Doublers Base ISA shall strive to preserve compatibility with conforming software whenever practical.

Where compatibility cannot be maintained, changes shall be clearly documented.

---

## 19.9 Compliance

A processor, software package, or development tool conforms to the Doublers Base ISA if it satisfies all mandatory architectural requirements applicable to its implementation category.

Conformance does not imply identical performance or internal implementation.

# Chapter 20 — Glossary of Architectural Terms

## 20.1 Overview

This chapter defines the terminology used throughout the Doublers ISA Specification.

Unless otherwise stated, these definitions apply to all chapters of this specification.

---

## 20.2 Application Binary Interface (ABI)

The standardized software interface defining function calls, register usage, stack behavior, and software interoperability for the Doublers architecture.

---

## 20.3 Architecture

The complete processor design as defined by the Doublers ISA, the Doublers Command Architecture (DCA), and all mandatory architectural behavior.

---

## 20.4 Base ISA

The mandatory instruction set, registers, memory model, exceptions, and processor behavior defined by this specification.

All compatible processors shall implement the Base ISA.

---

## 20.5 Community Addition

An optional architectural feature developed outside the Base ISA that preserves compatibility with the Doublers Base ISA.

---

## 20.6 DCA

The Doublers Command Architecture.

DCA defines the command representation and decoding architecture used by processors implementing the Doublers ISA.

---

## 20.7 Exception

An event generated by the processor while executing an instruction that requires software intervention.

Examples include:

* Illegal Instruction
* Divide By Zero
* Memory Protection Exception

---

## 20.8 FLAGS Register

A processor register containing architectural status information describing the result of previous operations.

---

## 20.9 General-Purpose Register (GPR)

A register available for general computational use by software.

The Base ISA defines sixteen General-Purpose Registers.

---

## 20.10 Interrupt

An asynchronous event causing the processor to temporarily suspend normal execution in order to execute an interrupt handler.

---

## 20.11 ISA

Instruction Set Architecture.

Defines the architectural behavior visible to software, including instructions, registers, exceptions, and memory operations.

---

## 20.12 Kernel Mode

The highest processor privilege level defined by the Base ISA.

Kernel Mode permits unrestricted execution of privileged instructions.

---

## 20.13 Privilege Level

The execution permission level currently assigned to software executing on the processor.

The Base ISA defines:

* Kernel Mode
* User Mode

---

## 20.14 Register

A storage element within the processor capable of holding architectural state.

Registers may be general-purpose or special-purpose.

---

## 20.15 System Call

A controlled transfer of execution from User Mode to Kernel Mode using the SYSCALL instruction.

---

## 20.16 TransDoub

The official software development and testing environment for the Doublers architecture.

TransDoub executes Doublers programs on existing processor architectures for development, testing, and validation purposes.

---

## 20.17 HardDoub

The hardware implementation specification describing how processor designers may implement a Doublers-compatible processor.

HardDoub complements the Doublers ISA and DCA specifications.

---

## 20.18 User Mode

The restricted processor privilege level intended for application software.

User Mode software shall not execute privileged instructions defined by the Base ISA.

---

## 20.19 Compatibility

The ability of processors, software, and development tools to correctly implement and execute the behavior defined by the Doublers Base ISA.

---

## 20.20 Future Definitions

Future versions of the Doublers architecture may introduce additional terminology.

Previously defined architectural terms shall retain their meanings unless explicitly revised by a newer specification.

# Chapter 21 — Versioning Policy

## 21.1 Overview

The Doublers ISA shall use semantic versioning to identify architectural revisions.

Every published specification shall include a major version number and a minor version number.

Example:

* Version 1.0
* Version 1.1
* Version 2.0

---

## 21.2 Major Versions

A major version indicates significant architectural changes.

Major versions may introduce new mandatory architectural behavior.

Processors shall clearly report the major ISA version they implement.

---

## 21.3 Minor Versions

Minor versions introduce clarifications, documentation improvements, optional additions, or compatibility improvements.

Minor versions should preserve compatibility with previous software whenever practical.

---

## 21.4 Compatibility

Software written for an earlier compatible version should continue to execute correctly on newer compatible processors unless explicitly documented otherwise.

Processors shall accurately report the ISA version they implement.

---

## 21.5 Deprecation

Architectural features should not be removed without strong technical justification.

Deprecated features shall remain documented until formally removed in a future major version.

---

## 21.6 Version Reporting

Processors shall provide a mechanism for software to determine:

* Supported ISA Version
* Supported DCA Version

The reporting mechanism is implementation-defined.

---

## 21.7 Documentation

Every published version shall include:

* Version Number
* Publication Date
* Revision Summary

---

## 21.8 Compliance

Processors shall not claim compatibility with ISA versions they do not fully implement.

# Chapter 22 — Document Structure and References

## 22.1 Overview

This specification defines the mandatory architectural behavior of the Doublers Base ISA.

Supporting documents complement this specification and define additional architectural components.

---

## 22.2 Required Documents

The complete Doublers architecture consists of the following primary documents:

* Doublers ISA Specification
* Doublers Command Architecture (DCA) Specification
* DCA License

Each document serves a distinct purpose.

---

## 22.3 Relationship Between Documents

The Doublers ISA defines:

* Processor behavior.
* Instructions.
* Registers.
* Exceptions.
* Memory architecture.

The DCA Specification defines:

* Command representation.
* Command decoding.
* Processor implementation model.

The DCA License defines:

* Ecosystem participation requirements.
* Redistribution permissions.
* Community extension requirements.

---

## 22.4 Community Additions

Community additions shall reference the compatible versions of:

* Doublers ISA
* DCA

Published additions should clearly identify the versions against which they were developed.

---

## 22.5 Future Documents

Additional project documentation may be published, including:

* Programming Guides
* Developer Manuals
* CPU Design Notes
* DoubRun Documentation

These documents do not modify the mandatory architectural behavior defined by the Base ISA.

---

## 22.6 Normative Language

Within this specification, the following terms indicate requirement strength:

* **Shall** — Mandatory requirement.
* **Should** — Recommended practice.
* **May** — Optional behavior.

---

## 22.7 Final Authority

In the event of conflicting documentation, the Doublers ISA Specification shall be considered the authoritative definition of Base ISA behavior.

For DCA implementation details, the DCA Specification shall take precedence.

---

## 22.8 Completion

This document constitutes Version 1.0 of the Doublers Base ISA Specification.

Future revisions shall preserve compatibility whenever practical while continuing the long-term evolution of the Doublers architecture.

# Appendix A — Register Reference

## A.1 Overview

This appendix summarizes all architecturally defined registers in the Doublers Base ISA.

---

## A.2 General-Purpose Registers

The Base ISA defines sixteen 64-bit General-Purpose Registers (GPRs).

| Register | Purpose         |
| -------- | --------------- |
| R0       | General-purpose |
| R1       | General-purpose |
| R2       | General-purpose |
| R3       | General-purpose |
| R4       | General-purpose |
| R5       | General-purpose |
| R6       | General-purpose |
| R7       | General-purpose |
| R8       | General-purpose |
| R9       | General-purpose |
| R10      | General-purpose |
| R11      | General-purpose |
| R12      | General-purpose |
| R13      | General-purpose |
| R14      | General-purpose |
| R15      | General-purpose |

---

## A.3 Special-Purpose Registers

| Register | Purpose                   |
| -------- | ------------------------- |
| PC       | Program Counter           |
| SP       | Stack Pointer             |
| FLAGS    | Processor Status Register |

---

## A.4 Reserved Registers

Additional register identifiers are reserved for future compatible community additions.

Processors shall not assign conflicting meanings to Base ISA registers.

---

## A.5 Register Width

All Base ISA registers are 64 bits wide unless otherwise specified.

# Appendix B — Instruction Reference

## B.1 Overview

This appendix summarizes the mandatory instruction categories defined by the Doublers Base ISA.

Instruction syntax and behavior are defined within the appropriate chapters of this specification.

---

## B.2 Arithmetic Instructions

* ADD
* SUB
* MUL
* DIV
* MOD
* INC
* DEC
* NEG

---

## B.3 Logical Instructions

* AND
* OR
* XOR
* NOT

---

## B.4 Shift Instructions

* SHL
* SHR

---

## B.5 Comparison Instructions

* CMP
* TEST

---

## B.6 Memory Instructions

* LOAD
* STORE
* PUSH
* POP

---

## B.7 Control Flow Instructions

* JMP
* CALL
* RET

Conditional branches:

* JE
* JNE
* JG
* JL
* JGE
* JLE

---

## B.8 System Instructions

* SYSCALL
* BREAK
* NOP
* HALT

---

## B.9 Privileged Instructions

Privileged instructions may execute only in Kernel Mode.

Execution from User Mode shall generate a Privilege Exception.

---

## B.10 Future Instructions

Future compatible community additions may define additional instructions without modifying the Base ISA.

# Appendix C — Exception Codes

## C.1 Overview

This appendix summarizes the architectural exceptions defined by the Doublers Base ISA.

---

## C.2 Mandatory Exceptions

| Exception           | Description                                    |
| ------------------- | ---------------------------------------------- |
| Illegal Instruction | Invalid or undefined instruction               |
| Divide By Zero      | Division by zero                               |
| Memory Protection   | Unauthorized memory access                     |
| Execute Protection  | Execution from non-executable memory           |
| Privilege Exception | Privileged instruction executed from User Mode |
| Breakpoint          | BREAK instruction encountered                  |
| Debug Exception     | Single-step or debugging event                 |
| Watchpoint          | Optional watchpoint event                      |
| System Call         | SYSCALL instruction                            |
| Interrupt           | Hardware or software interrupt                 |

---

## C.3 Reserved Exception Codes

Exception identifiers not defined by the Base ISA are reserved for future compatible additions.

---

## C.4 Exception Handling

Exception processing behavior is defined in the Interrupt and Exception chapters of this specification.

# Appendix D — Memory Map

## D.1 Overview

The Doublers Base ISA defines a logical memory organization.

Actual physical implementation is processor-defined.

---

## D.2 Typical Memory Layout

```
+-------------------------------+
| Kernel Reserved               |
+-------------------------------+
| Kernel Code                   |
+-------------------------------+
| Kernel Data                   |
+-------------------------------+
| User Program Code             |
+-------------------------------+
| User Data                     |
+-------------------------------+
| Heap                          |
+-------------------------------+
| Free Memory                   |
+-------------------------------+
| Stack                         |
+-------------------------------+
```

---

## D.3 Stack Growth

The Base ISA does not require a specific stack growth direction.

The selected convention shall remain consistent throughout execution.

---

## D.4 Memory Permissions

Memory regions may define:

* Read
* Write
* Execute

Processors shall enforce these permissions.

---

## D.5 Address Space

The Base ISA defines a 64-bit virtual address space.

Physical memory implementation is processor-defined.

# Appendix E — Reserved Instruction List

## E.1 Overview

This appendix defines the treatment of instruction encodings reserved by the Doublers Base ISA.

---

## E.2 Reserved Instructions

Instruction representations not assigned by the Base ISA are reserved.

Reserved instructions shall not be executed by Base ISA software.

---

## E.3 Processor Behavior

Execution of a reserved instruction shall generate an Illegal Instruction Exception unless the instruction has been assigned by a compatible community addition.

---

## E.4 Community Additions

Compatible community additions may assign meanings to reserved instruction representations provided they:

* Preserve Base ISA compatibility.
* Do not redefine existing Base ISA instructions.
* Clearly document the added behavior.

---

## E.5 Undefined Behavior

Software shall not depend upon the behavior of reserved instructions.

Processor implementations shall not assign conflicting meanings while claiming compatibility with the Doublers Base ISA.

---

## E.6 Future Expansion

Reserved instruction space exists to support the long-term evolution of the Doublers architecture while preserving compatibility with existing software.
