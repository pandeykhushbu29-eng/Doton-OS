========================================================
DOUBLERS COMMAND ARCHITECTURE (DCA)
Version 1.0
===========

Status:
Draft

Project Name:
Doublers Command Architecture

Abbreviation:
DCA

Part Of:
Doublers Architecture

Created By:
Real name (not full):Avyaan
creator name:Doub.creator_00001

Purpose:
Define the command representation, decoding model,
processor execution model, and implementation
requirements for processors compatible with the
Doublers ISA.

Relationship:

Doublers ISA defines WHAT the processor shall do.

DCA defines HOW compatible processors shall
understand, decode, and execute Doublers commands.

========================================================

# Chapter 1 — Introduction

## 1.1 Overview

The Doublers Command Architecture (DCA) defines the processor execution architecture used by all processors implementing the Doublers ISA.

While the Doublers ISA specifies architectural behavior visible to software, the DCA specifies how compatible processors interpret, decode, and execute Doublers commands.

Every processor claiming compatibility with the Doublers Base ISA shall also implement the mandatory requirements defined by the corresponding DCA specification.

---

## 1.2 Objectives

The DCA is intended to provide:

* A standardized command architecture.
* Consistent processor behavior.
* Reliable command decoding.
* Efficient processor implementation.
* Long-term architectural stability.

---

## 1.3 Scope

The DCA defines:

* Command representation.
* Command decoding.
* Processor fetch behavior.
* Command execution pipeline.
* Register reference encoding.
* Immediate value representation.
* Command stream validation.
* Architectural alignment rules.

The DCA does not define processor microarchitecture.

Processor designers remain free to choose internal implementation techniques provided all externally visible behavior remains compliant.

---

## 1.4 Design Philosophy

The Doublers Command Architecture is based upon the following principles:

* Simplicity.
* Predictability.
* Compatibility.
* Hardware efficiency.
* Long-term extensibility.

All mandatory architectural behavior shall remain deterministic.

---

## 1.5 Relationship to the ISA

The ISA and DCA are complementary specifications.

The ISA defines:

* Instructions.
* Registers.
* Exceptions.
* Memory behavior.

The DCA defines:

* Command representation.
* Command decoding.
* Execution sequencing.

Neither specification replaces the other.

Both are required for a complete processor implementation.

---

## 1.6 Compliance

A processor is DCA-compatible only if it satisfies every mandatory requirement defined by this specification.

# Chapter 2 — Architectural Model

## 2.1 Purpose

The Doublers Command Architecture (DCA) defines the hardware execution model of a Doublers-compatible processor. While the Doublers ISA specifies the programmer-visible behavior of instructions, registers, memory, and exceptions, the DCA specifies how compatible hardware shall represent, fetch, decode, and execute those instructions.

This chapter defines the architectural model common to all compliant Doublers processors.

---

## 2.2 Architectural Independence

The Doublers ISA is independent of any particular processor implementation.

A processor may differ internally in:

- Pipeline depth
- Cache organization
- Clock frequency
- Internal scheduling
- Execution width
- Power management
- Physical layout

provided that all externally visible architectural behavior remains fully compatible with the Doublers ISA and this DCA.

---

## 2.3 Processor Components

A compliant Doublers processor shall consist of the following logical components.

### Command Fetch Unit

Responsible for obtaining the next command from memory.

---

### Command Decode Unit

Responsible for interpreting the fetched command into its architectural operation.

---

### Execution Unit

Responsible for executing the decoded operation.

---

### Register System

Stores all architecturally visible processor registers.

---

### Memory Interface

Performs architectural memory accesses.

---

### Exception Controller

Detects and reports architectural exceptions.

---

### Program Counter Logic

Maintains the location of the currently executing command.

---

## 2.4 Architectural State

The architectural state of a Doublers processor consists of:

- General-purpose registers
- Special registers
- Program Counter (PC)
- Status/Flag registers
- Architecturally visible memory
- Pending architectural exceptions

Temporary implementation-specific state shall not be architecturally visible.

---

# 2.5 Electrical State Model

The Doublers processor operates using three active hardware states during normal execution.

These states describe the electrical representation used internally by compatible hardware implementations.

Software shall never directly manipulate these electrical states.

---

## Active States

### State 2 — High

Represents the High electrical state.

This state is an active computational state.

---

### State 4 — Mid

Represents the Mid electrical state.

This state is an active computational state.

---

### State 8 — Low

Represents the Low electrical state.

This state is an active computational state.

---

## Power State

### State 10 — OFF

Represents the processor power-off condition.

When a processor is in the OFF state:

- No commands are fetched.
- No commands are decoded.
- No instructions execute.
- No architectural state changes occur.

The OFF state is not an architectural execution state.

It shall never appear within a valid command stream.

It shall never be interpreted as an instruction.

It shall never be referenced by software.

The OFF state exists solely as the physical condition in which the processor is unpowered.

---

## 2.6 Hardware Interpretation

Hardware designers shall implement reliable mechanisms for distinguishing the active electrical states.

The exact voltage levels, timing characteristics, transistor implementations, or signaling techniques are implementation-defined.

Only the architectural meanings of States 2, 4, and 8 are standardized by the DCA.

---

## 2.7 Software Visibility

Programs executing under the Doublers ISA shall remain completely unaware of the processor's electrical implementation.

The ISA operates solely on architectural instructions, registers, memory, and exceptions.

The electrical representation defined by the DCA is considered an implementation detail and shall not affect software compatibility.

---

## 2.8 Compliance

A processor is DCA-compliant if it:

- Correctly implements the Doublers ISA.
- Correctly represents the three active electrical states.
- Correctly handles the OFF power condition.
- Preserves all architecturally visible behavior defined by the ISA and DCA.

Implementation-specific optimizations are permitted provided they do not alter observable architectural behavior.

# Chapter 3 — Command Representation

## 3.1 Overview

The Doublers Command Architecture represents executable programs as ordered sequences of architectural commands.

Each command represents one complete operation defined by the Doublers ISA.

Processors shall interpret commands according to the rules defined by this specification.

---

## 3.2 Architectural Command Unit

The Architectural Command Unit (ACU) is the smallest executable unit recognized by a DCA-compatible processor.

Every valid program consists of one or more ACUs arranged in execution order.

Processors shall fetch, decode, and execute commands one ACU at a time.

---

## 3.3 Command Identity

Each ACU shall uniquely identify a single ISA instruction.

The command representation shall provide sufficient information to determine:

* Instruction identity.
* Operand requirements.
* Register references.
* Immediate data requirements.
* Execution behavior.

---

## 3.4 Human Representation

For documentation and software development, commands may be represented using human-readable mnemonic names.

Example:

* LOAD
* STORE
* ADD
* SUB
* JMP
* CALL
* RET
* SYSCALL

The human-readable form is intended solely for software development and documentation.

Processors operate upon the DCA command representation rather than textual mnemonics.

---

## 3.5 Command Stream

Programs shall consist of sequential ACUs.

The Program Counter always references the next ACU to be fetched.

Unless modified by architectural control-flow instructions, command execution proceeds sequentially.

---

## 3.6 Command Completeness

Every ACU shall contain all information required for correct architectural decoding.

Processors shall not depend upon information contained within neighboring commands.

Each command shall remain independently decodable.

---

## 3.7 Command Categories

Architectural commands may belong to one of the following categories:

* Arithmetic
* Logical
* Memory
* Comparison
* Branch
* Stack
* System
* Privileged
* Miscellaneous

Future compatible community additions may introduce additional categories.

---

## 3.8 Operand Description

A command may reference:

* Zero operands
* One operand
* Two operands
* Three operands

The required operand count is determined by the instruction definition within the Doublers ISA.

---

## 3.9 Immediate Data

Commands requiring immediate values shall explicitly include those values within the command representation.

Immediate values shall never be inferred from surrounding commands.

Encoding rules are defined in later chapters.

---

## 3.10 Register References

Commands referencing processor registers shall explicitly identify those registers.

Register identifiers shall correspond to the register definitions contained within the Doublers ISA.

---

## 3.11 Reserved Fields

Command representations may contain reserved fields for future architectural growth.

Software shall not depend upon reserved field values.

Processors shall preserve reserved behavior as defined by this specification.

---

## 3.12 Invalid Representation

An ACU that cannot be decoded according to this specification shall immediately generate an Illegal Command Exception.

No architectural state shall be modified before the exception is generated.

---

## 3.13 Forward Compatibility

Future DCA revisions may introduce additional command fields while preserving compatibility with existing command representations whenever practical.

Previously defined command fields shall retain their architectural meaning unless explicitly revised by a future major version.

---

## 3.14 Compliance

A DCA-compatible processor shall correctly recognize, decode, and validate every Architectural Command Unit defined by this specification before execution.

Commands not conforming to the DCA representation shall not be executed.

# Chapter 4 — Command Fetch Architecture

## 4.1 Overview

The Command Fetch Architecture defines how a DCA-compatible processor retrieves Architectural Command Units (ACUs) from memory prior to execution.

Every processor shall implement a reliable and deterministic command fetch mechanism.

---

## 4.2 Fetch Sequence

The processor shall perform the following operations during command fetch:

1. Read the Program Counter.
2. Locate the next ACU.
3. Verify fetch accessibility.
4. Retrieve the complete ACU.
5. Forward the ACU to the decoder.

No execution shall occur during the fetch stage.

---

## 4.3 Program Counter

The Program Counter (PC) always references the first unit of the next command.

After successful execution, the PC advances according to the length of the fetched command unless modified by architectural control-flow instructions.

---

## 4.4 Sequential Fetch

Commands shall normally be fetched in sequential order.

Sequential fetch continues until interrupted by:

* JMP
* CALL
* RET
* Conditional Branches
* Exceptions
* Interrupts

---

## 4.5 Fetch Permissions

Processors shall verify that the command location is executable before fetching.

Attempting to fetch from a non-executable region shall generate an Execute Protection Exception.

---

## 4.6 Fetch Alignment

Commands shall begin at valid architectural command boundaries.

Processors shall reject improperly aligned commands according to this specification.

---

## 4.7 Partial Fetch Prevention

Processors shall never decode partially fetched commands.

If the complete ACU cannot be retrieved, execution shall stop and the appropriate architectural exception shall be generated.

---

## 4.8 Branch Fetch

Following a successful branch, jump, call, or return, the next fetch shall begin at the updated Program Counter value.

---

## 4.9 Fetch Exceptions

The fetch stage may generate:

* Execute Protection Exception
* Memory Protection Exception
* Illegal Command Exception

No architectural state shall be modified before the exception is delivered.

---

## 4.10 Compliance

Every DCA-compatible processor shall implement the command fetch behavior defined in this chapter.

# Chapter 5 — Command Decode Architecture

## 5.1 Overview

The Command Decode Architecture defines how fetched Architectural Command Units are interpreted before execution.

Decoding converts the fetched command into an executable architectural operation.

---

## 5.2 Decode Objectives

The decoder shall determine:

* Instruction identity.
* Operand count.
* Register references.
* Immediate value presence.
* Command category.
* Privilege requirements.

---

## 5.3 Decoder Requirements

Every fetched command shall be completely decoded before execution begins.

Incomplete or ambiguous decoding shall not be permitted.

---

## 5.4 Decode Validation

The decoder shall verify that:

* The command format is valid.
* Required operands are present.
* Register references are valid.
* Immediate values are correctly represented.
* Reserved fields comply with this specification.

---

## 5.5 Illegal Commands

Commands failing architectural validation shall generate an Illegal Command Exception.

Illegal commands shall never advance to execution.

---

## 5.6 Reserved Fields

Reserved command fields shall not alter architectural behavior.

Processors shall ignore or validate reserved fields as defined by this specification.

---

## 5.7 Decode Independence

Every command shall be decoded independently.

The decoder shall not require information from previous or subsequent commands to determine the meaning of the current command.

---

## 5.8 Decode Completion

Successful decoding produces an internal architectural representation suitable for execution.

The structure of this internal representation is implementation-defined.

---

## 5.9 Future Compatibility

Future DCA revisions may define additional command fields while preserving compatibility with previously defined command representations whenever practical.

---

## 5.10 Compliance

Every DCA-compatible processor shall correctly decode every valid Architectural Command Unit before execution.

Commands that fail decoding shall not be executed.

# Chapter 6 — Operand Representation

## 6.1 Overview

Operands provide the data required for execution of Architectural Command Units (ACUs).

Every operand shall be explicitly represented within the command representation defined by this specification.

---

## 6.2 Operand Types

The Doublers Command Architecture recognizes the following operand types:

* Register Operand
* Immediate Operand
* Memory Operand
* Address Operand

Future compatible community additions may introduce additional operand types.

---

## 6.3 Operand Count

Commands may contain:

* Zero operands
* One operand
* Two operands
* Three operands

The required operand count is determined by the instruction definition within the Doublers ISA.

---

## 6.4 Explicit Representation

Operands shall always be explicitly identified.

Processors shall not infer operand values from previously executed commands.

---

## 6.5 Operand Ordering

Operand order is architecturally significant.

Processors shall interpret operands in the exact order defined by the corresponding ISA instruction.

---

## 6.6 Operand Validation

Before execution, the processor shall verify:

* Operand count.
* Operand type.
* Register validity.
* Immediate value validity.
* Memory reference validity.

Invalid operands shall generate an Illegal Command Exception.

---

## 6.7 Memory Operands

Memory operands shall reference valid architectural addresses.

Permission checks shall be performed before memory access begins.

---

## 6.8 Immediate Operands

Immediate operands are values stored directly within the command.

Immediate values remain constant throughout execution of that command.

---

## 6.9 Register Operands

Register operands reference architecturally defined processor registers.

Register identifiers shall correspond to the register definitions contained within the Doublers ISA.

---

## 6.10 Compliance

Every DCA-compatible processor shall correctly recognize, validate, and interpret all operand types defined by this specification.

# Chapter 7 — Register Reference Encoding

## 7.1 Overview

This chapter defines how Architectural Command Units identify processor registers.

Register references provide the connection between commands and the processor's architectural register set.

---

## 7.2 Register Identification

Every register referenced by a command shall be identified using the DCA register reference mechanism.

Each reference shall uniquely identify one architectural register.

---

## 7.3 Register Classes

The Base DCA supports the following register classes:

* General-Purpose Registers
* Special-Purpose Registers
* Status Registers

Future compatible community additions may define additional register classes.

---

## 7.4 General-Purpose Registers

General-Purpose Register references shall correspond to the sixteen registers defined by the Doublers Base ISA.

Each register reference shall uniquely identify one General-Purpose Register.

---

## 7.5 Special Registers

Special register references may identify:

* Program Counter
* Stack Pointer
* FLAGS Register

Additional special registers may be introduced through compatible community additions.

---

## 7.6 Reserved Register References

Unused register identifiers are reserved for future architectural expansion.

Processors shall reject undefined register references unless assigned by a compatible community addition.

---

## 7.7 Register Validation

During command decoding, every register reference shall be validated before execution begins.

Invalid register references shall generate an Illegal Command Exception.

---

## 7.8 Architectural Independence

The internal physical implementation of processor registers is implementation-defined.

Software-visible behavior shall remain identical regardless of internal hardware organization.

---

## 7.9 Future Compatibility

Future DCA revisions may define additional register reference formats while preserving compatibility with existing architectural definitions whenever practical.

---

## 7.10 Compliance

Every DCA-compatible processor shall correctly identify and validate all architectural register references before command execution.

# Chapter 8 — Immediate Value Representation

## 8.1 Overview

Immediate values are constant values embedded directly within an Architectural Command Unit (ACU).

Unlike register or memory operands, immediate values are supplied directly by the command itself.

---

## 8.2 Purpose

Immediate values provide constant data required during execution without requiring additional memory accesses.

Typical uses include:

* Constant arithmetic values.
* Memory offsets.
* Branch offsets.
* Initialization values.
* Address calculations.

---

## 8.3 Architectural Representation

Immediate values shall be represented as part of the command representation.

Processors shall retrieve immediate values during command decoding.

---

## 8.4 Immediate Size

The size of an immediate value is determined by the command definition.

Supported immediate sizes are implementation-defined within the constraints of the Doublers ISA.

---

## 8.5 Signed and Unsigned Values

Immediate values may represent:

* Signed integers.
* Unsigned integers.

The interpretation is determined by the executing ISA instruction.

---

## 8.6 Immediate Validation

Processors shall verify that immediate values conform to the architectural representation required by the decoded command.

Malformed immediate representations shall generate an Illegal Command Exception.

---

## 8.7 Immediate Usage

Immediate values become available only after successful command decoding.

Commands shall not modify embedded immediate values during execution.

---

## 8.8 Reserved Immediate Formats

Unused immediate representations are reserved for future compatible community additions.

Reserved formats shall not alter Base DCA behavior.

---

## 8.9 Forward Compatibility

Future DCA revisions may introduce additional immediate representations while preserving compatibility with existing command formats whenever practical.

---

## 8.10 Compliance

Every DCA-compatible processor shall correctly decode, validate, and interpret immediate values according to this specification.

# Chapter 9 — Command Alignment and Boundaries

## 9.1 Overview

Reliable command execution requires processors to correctly identify the beginning and end of every Architectural Command Unit (ACU).

This chapter defines the architectural rules governing command alignment and command boundaries.

---

## 9.2 Command Boundary

Every ACU shall occupy one complete architectural command boundary.

Processors shall always begin decoding at the start of a valid boundary.

---

## 9.3 Alignment Requirements

Commands shall satisfy the alignment requirements defined by the DCA.

Misaligned command fetches shall not be executed.

---

## 9.4 Boundary Detection

Processors shall determine command boundaries before decoding begins.

Partial boundary detection is prohibited.

---

## 9.5 Sequential Advancement

After successful execution, the Program Counter shall advance to the beginning of the next valid ACU unless modified by architectural control-flow instructions.

---

## 9.6 Misaligned Commands

Attempting to decode a command beginning at an invalid boundary shall generate an Illegal Command Exception.

No architectural state shall be modified before the exception is generated.

---

## 9.7 Command Integrity

Processors shall ensure that every fetched command remains complete throughout decoding and execution.

Incomplete command representations shall never execute.

---

## 9.8 Reserved Alignment Rules

Additional alignment requirements may be introduced by future compatible community additions provided they do not alter the mandatory Base DCA behavior.

---

## 9.9 Architectural Consistency

All compliant processors shall interpret command boundaries identically regardless of internal hardware implementation.

---

## 9.10 Compliance

Every DCA-compatible processor shall correctly identify, validate, and enforce command alignment and command boundary rules defined by this specification.

# Chapter 10 — Command Stream Organization

## 10.1 Overview

The Doublers Command Architecture organizes executable programs as ordered streams of Architectural Command Units (ACUs).

Processors shall execute commands in the order specified by the command stream unless modified by architectural control-flow operations.

---

## 10.2 Command Stream Definition

A command stream is a contiguous sequence of valid ACUs beginning at a designated entry point.

The command stream represents the executable portion of a Doublers program.

---

## 10.3 Stream Entry

Execution begins at the architectural entry point defined by the executing program.

The Program Counter shall be initialized to this entry point before the first command is fetched.

---

## 10.4 Sequential Progression

Following successful execution, the processor shall advance to the next ACU in the stream.

Sequential progression continues until altered by:

* Branch instructions
* Procedure calls
* Returns
* Exceptions
* Interrupts

---

## 10.5 Stream Integrity

The processor shall preserve the integrity of the command stream throughout execution.

Corrupted or incomplete command streams shall not be executed.

---

## 10.6 End of Stream

Execution of a command stream normally terminates by:

* HALT instruction
* Program termination
* Fatal architectural exception

Processor implementations may define additional platform-specific termination mechanisms.

---

## 10.7 Stream Modification

Self-modifying command streams are implementation-defined.

Processors shall maintain architectural correctness regardless of internal implementation.

---

## 10.8 Stream Isolation

Execution of one command stream shall not modify another command stream unless explicitly permitted by software.

---

## 10.9 Architectural Visibility

The command stream represents the complete architectural instruction sequence visible to software.

Internal processor optimizations shall not alter visible execution behavior.

---

## 10.10 Compliance

Every DCA-compatible processor shall correctly organize, fetch, and execute command streams according to this specification.

# Chapter 11 — Execution Pipeline Model

## 11.1 Overview

The Doublers Command Architecture defines a logical execution pipeline for all compatible processors.

This pipeline specifies architectural behavior rather than physical processor implementation.

---

## 11.2 Logical Pipeline

The architectural execution pipeline consists of the following stages:

1. Fetch
2. Decode
3. Validate
4. Execute
5. Commit
6. Advance

Processors shall preserve the architectural behavior of these stages regardless of internal implementation.

---

## 11.3 Fetch Stage

The Fetch stage retrieves the next Architectural Command Unit using the current Program Counter.

Only complete commands may proceed to decoding.

---

## 11.4 Decode Stage

The Decode stage identifies:

* Instruction identity
* Operand structure
* Register references
* Immediate values
* Privilege requirements

Commands failing architectural decoding shall generate an Illegal Command Exception.

---

## 11.5 Validation Stage

Before execution begins, the processor shall verify:

* Command validity
* Operand validity
* Register references
* Memory permissions
* Privilege requirements

Commands failing validation shall not execute.

---

## 11.6 Execute Stage

The Execute stage performs the architectural operation defined by the decoded command.

Execution shall not become architecturally visible until successful completion.

---

## 11.7 Commit Stage

The Commit stage updates architectural state.

Examples include:

* Register updates
* Memory writes
* FLAGS modifications
* Program Counter changes

State modifications shall occur atomically from the perspective of software.

---

## 11.8 Advance Stage

Following successful commit, the Program Counter advances to the next Architectural Command Unit unless modified by architectural control-flow operations.

---

## 11.9 Pipeline Flexibility

Processor implementations may employ:

* Single-cycle execution
* Multi-cycle execution
* Pipelining
* Superscalar execution
* Speculative execution
* Out-of-order execution

provided architectural behavior remains identical to the model defined by this chapter.

---

## 11.10 Compliance

Every DCA-compatible processor shall preserve the architectural execution model defined by this specification regardless of internal hardware organization.

# Chapter 12 — Command Validation

## 12.1 Overview

Before execution, every Architectural Command Unit (ACU) shall undergo architectural validation.

Validation ensures that only correctly represented and authorized commands are executed.

---

## 12.2 Validation Objectives

The validation stage shall verify:

* Command integrity.
* Instruction identity.
* Operand correctness.
* Register references.
* Immediate value representation.
* Privilege requirements.
* Command alignment.

---

## 12.3 Mandatory Validation

Every fetched command shall be validated before execution begins.

Processors shall not bypass mandatory validation.

---

## 12.4 Validation Order

The architectural validation sequence shall occur after successful decoding and before execution.

The exact internal implementation is processor-defined.

---

## 12.5 Operand Verification

Processors shall verify that:

* The required number of operands is present.
* Operand types match the instruction definition.
* Register references are valid.
* Memory operands reference legal architectural addresses.

---

## 12.6 Privilege Verification

Commands requiring elevated privilege shall verify the current processor privilege level before execution.

Failure shall generate a Privilege Exception.

---

## 12.7 Memory Verification

Commands accessing memory shall verify:

* Read permission.
* Write permission.
* Execute permission (when applicable).

Permission violations shall generate the corresponding architectural exception.

---

## 12.8 Validation Failure

Commands failing validation shall not execute.

No architectural state shall be modified before the exception is generated.

---

## 12.9 Future Compatibility

Additional validation rules may be introduced by future DCA revisions provided they preserve Base DCA compatibility whenever practical.

---

## 12.10 Compliance

Every DCA-compatible processor shall validate every Architectural Command Unit according to this specification before execution.

# Chapter 13 — Exception Generation

## 13.1 Overview

Exceptions provide a standardized mechanism for reporting exceptional conditions encountered during command execution.

All DCA-compatible processors shall generate exceptions consistently.

---

## 13.2 Exception Sources

Exceptions may originate during:

* Fetch
* Decode
* Validation
* Execution
* Commit

The originating stage shall determine the reported exception.

---

## 13.3 Precise Exceptions

Exceptions shall be architecturally precise.

Software shall observe processor state as though execution stopped immediately before the faulting command modified architectural state.

---

## 13.4 Illegal Commands

Commands that cannot be decoded or validated shall generate an Illegal Command Exception.

Processors shall not attempt partial execution.

---

## 13.5 Privilege Exceptions

Execution of privileged commands from an insufficient privilege level shall generate a Privilege Exception.

---

## 13.6 Memory Exceptions

Memory-related exceptions include:

* Read Protection
* Write Protection
* Execute Protection
* Address Violation

Processors shall report the appropriate architectural exception.

---

## 13.7 Arithmetic Exceptions

Arithmetic exceptions include:

* Divide by Zero
* Arithmetic Overflow (implementation-defined where applicable)

---

## 13.8 Exception Delivery

Upon exception generation, normal command execution shall cease.

Control shall transfer to the exception handling mechanism defined by the Doublers ISA.

---

## 13.9 Recovery

Following successful exception handling, execution may resume according to the architectural rules defined by the Doublers ISA.

Recovery behavior is determined by the specific exception type.

---

## 13.10 Compliance

Every DCA-compatible processor shall generate and report architectural exceptions consistently with this specification and the Doublers ISA.

# Chapter 14 — Processor State Management

## 14.1 Overview

Processor State Management defines how a DCA-compatible processor maintains, updates, and preserves its architectural state throughout command execution.

Architectural state shall remain consistent at all times.

---

## 14.2 Architectural State

The architectural processor state consists of:

* General-Purpose Registers
* Special Registers
* FLAGS Register
* Program Counter
* Stack Pointer
* Architecturally visible memory

Processors may maintain additional internal state provided it remains invisible to software.

---

## 14.3 State Initialization

Before execution begins, the processor shall initialize the architectural state according to the platform initialization procedure.

The initial Program Counter shall reference the architectural entry point.

---

## 14.4 State Modification

Architectural state may be modified only by:

* Successful command execution
* Exception handling
* Interrupt handling
* Processor reset

No other mechanism shall alter the visible architectural state.

---

## 14.5 State Consistency

At every architectural boundary, processor state shall remain internally consistent.

Software shall never observe partially updated architectural state.

---

## 14.6 State Preservation

Commands that do not explicitly modify a state component shall leave that component unchanged.

Processors shall preserve unaffected architectural state across command execution.

---

## 14.7 State Visibility

Only committed architectural state shall become visible to software.

Internal temporary values remain implementation-defined.

---

## 14.8 Processor Reset

Processor reset returns the architectural state to its defined initialization condition.

The exact initialization values are platform-defined unless specified by the Doublers ISA.

---

## 14.9 Future Expansion

Future DCA revisions may introduce additional architectural state components while preserving compatibility with previously defined processor state.

---

## 14.10 Compliance

Every DCA-compatible processor shall correctly initialize, maintain, preserve, and expose architectural state according to this specification.

# Chapter 15 — Control Flow Processing

## 15.1 Overview

Control Flow Processing defines how a DCA-compatible processor changes the normal sequential execution of Architectural Command Units.

---

## 15.2 Sequential Execution

Execution normally proceeds sequentially from one command to the next.

The Program Counter determines the next command to be fetched.

---

## 15.3 Control Flow Commands

Control flow may be modified by:

* JMP
* CALL
* RET
* Conditional Branches
* Exceptions
* Interrupts

Future compatible community additions may define additional control-flow operations.

---

## 15.4 Program Counter Update

Whenever control flow changes, the Program Counter shall be updated before the next fetch begins.

The updated value shall reference a valid Architectural Command Unit.

---

## 15.5 Conditional Branches

Conditional branch execution depends upon the current architectural condition flags.

The branch decision shall be completed before the next command is fetched.

---

## 15.6 Procedure Calls

Procedure call commands transfer execution to another location while preserving the return location according to the Doublers ISA.

---

## 15.7 Procedure Returns

Return commands restore execution to the previously saved return location.

---

## 15.8 Invalid Targets

Attempting to transfer execution to an invalid or non-executable location shall generate the appropriate architectural exception.

---

## 15.9 Deterministic Behavior

Given identical processor state and command streams, control-flow decisions shall always produce identical architectural results.

---

## 15.10 Compliance

Every DCA-compatible processor shall implement control-flow processing exactly as defined by the Doublers ISA and this specification.

# Chapter 16 — Memory Access Processing

## 16.1 Overview

Memory Access Processing defines how a DCA-compatible processor performs architectural memory operations.

All memory accesses shall comply with the requirements of the Doublers ISA and this specification.

---

## 16.2 Memory Operations

Architectural memory operations include:

* Memory Read
* Memory Write
* Instruction Fetch
* Stack Access

Additional operations may be defined by future compatible community additions.

---

## 16.3 Read Processing

Before reading memory, the processor shall verify:

* Address validity.
* Read permission.
* Alignment requirements.

Successful verification permits the read operation to proceed.

---

## 16.4 Write Processing

Before writing memory, the processor shall verify:

* Address validity.
* Write permission.
* Alignment requirements.

Writes failing verification shall not modify memory.

---

## 16.5 Execute Processing

Instruction fetches shall verify execute permission before command retrieval.

Attempting to fetch from a non-executable region shall generate an Execute Protection Exception.

---

## 16.6 Memory Consistency

Completed memory operations shall become architecturally visible only after successful command commitment.

Processors shall preserve architectural memory consistency regardless of internal implementation.

---

## 16.7 Invalid Memory Access

Invalid memory operations shall generate the corresponding architectural exception before modifying processor state.

---

## 16.8 Atomicity

Architecturally atomic memory operations shall complete entirely or have no visible effect.

Partial completion shall not be visible to software.

---

## 16.9 Future Compatibility

Future DCA revisions may define additional memory processing mechanisms while preserving Base DCA compatibility.

---

## 16.10 Compliance

Every DCA-compatible processor shall correctly perform, validate, and report architectural memory operations according to this specification.

# Chapter 17 — Privilege and Protection Model

## 17.1 Overview

The Privilege and Protection Model defines how a DCA-compatible processor enforces architectural security boundaries.

These mechanisms protect processor resources from unauthorized access.

---

## 17.2 Privilege Levels

The Base DCA recognizes the privilege levels defined by the Doublers ISA.

Processors shall correctly distinguish privileged and non-privileged execution.

---

## 17.3 Privileged Commands

Commands designated as privileged by the Doublers ISA shall execute only at the required privilege level.

Execution from an insufficient privilege level shall generate a Privilege Exception.

---

## 17.4 Memory Protection

Processors shall enforce architectural memory permissions.

Protection mechanisms include:

* Read Permission
* Write Permission
* Execute Permission

---

## 17.5 Register Protection

Access to privileged registers shall be restricted according to the architectural privilege model.

Unauthorized access attempts shall generate the appropriate exception.

---

## 17.6 State Isolation

Architectural state belonging to privileged execution shall remain protected from unauthorized modification.

---

## 17.7 Exception Protection

Protection violations shall be reported using the exception mechanisms defined by the Doublers ISA.

Protection failures shall not expose partially modified architectural state.

---

## 17.8 Processor Integrity

Protection mechanisms shall preserve processor integrity regardless of software behavior.

Internal implementation techniques remain processor-defined.

---

## 17.9 Future Expansion

Future compatible community additions may define additional protection mechanisms provided Base DCA compatibility is preserved.

---

## 17.10 Compliance

Every DCA-compatible processor shall implement the privilege and protection mechanisms defined by this specification and the Doublers ISA.

# Chapter 18 — Processor Reset and Initialization

## 18.1 Overview

This chapter defines the architectural requirements for processor reset and initialization.

Every DCA-compatible processor shall enter a well-defined architectural state before beginning execution.

---

## 18.2 Reset Operation

Processor reset terminates all currently executing architectural activity.

After reset, the processor shall initialize itself according to the platform initialization procedure.

---

## 18.3 Initial Processor State

Following reset, the processor shall establish:

* Program Counter
* Stack Pointer
* FLAGS Register
* General-Purpose Registers
* Special Registers

Initialization values are platform-defined unless specified by the Doublers ISA.

---

## 18.4 Initial Fetch

Following successful initialization, the processor shall begin command fetch from the architectural entry point.

No command execution shall occur before initialization completes.

---

## 18.5 Reset Integrity

Processor reset shall leave the architectural state internally consistent.

Partially initialized processor states shall never become visible to software.

---

## 18.6 Warm Reset

Implementations may support warm reset mechanisms.

Warm reset behavior is implementation-defined provided architectural correctness is preserved.

---

## 18.7 Cold Reset

Cold reset returns the processor to its initial architectural state.

Platform-specific initialization procedures may execute before program execution begins.

---

## 18.8 Future Compatibility

Future DCA revisions may define additional initialization mechanisms while preserving Base DCA compatibility.

---

## 18.9 Compliance

Every DCA-compatible processor shall correctly implement processor reset and initialization according to this specification.

# Chapter 19 — Compliance Requirements

## 19.1 Overview

This chapter defines the minimum requirements necessary for processor compatibility with the Doublers Command Architecture.

---

## 19.2 Mandatory Requirements

A compliant processor shall correctly implement:

* Command Fetch
* Command Decode
* Command Validation
* Command Execution
* Processor State Management
* Exception Generation
* Memory Processing
* Privilege Enforcement

---

## 19.3 Architectural Compatibility

Processors shall preserve all mandatory architectural behavior defined by:

* Doublers ISA
* Doublers Command Architecture

---

## 19.4 Internal Freedom

Processor designers may choose any internal implementation technique provided externally visible architectural behavior remains compliant.

---

## 19.5 Unsupported Features

Processors shall not advertise support for architectural features that are not correctly implemented.

---

## 19.6 Community Additions

Processors implementing compatible community additions shall continue to preserve Base DCA compatibility.

---

## 19.7 Compliance Claim

Processors satisfying all mandatory requirements may identify themselves as:

"DCA-Compatible"

---

## 19.8 Documentation

Processor documentation shall clearly identify:

* Supported ISA Version
* Supported DCA Version
* Implemented community additions

---

## 19.9 Future Revisions

Future DCA revisions should preserve compatibility whenever practical.

---

## 19.10 Compliance

Only processors satisfying every mandatory requirement of this specification may claim compatibility with the Doublers Command Architecture.

# Chapter 20 — Versioning and Document References

## 20.1 Overview

The Doublers Command Architecture shall use semantic versioning to identify architectural revisions.

---

## 20.2 Version Format

Every published DCA specification shall contain:

* Major Version
* Minor Version
* Publication Date

---

## 20.3 Major Versions

Major versions may introduce architectural changes requiring updated processor implementations.

---

## 20.4 Minor Versions

Minor versions primarily provide:

* Documentation improvements
* Clarifications
* Optional compatible additions
* Editorial corrections

---

## 20.5 Related Documents

The complete Doublers architecture consists of:

* Doublers ISA Specification
* Doublers Command Architecture
* DCA License

Each document serves a separate architectural purpose.

---

## 20.6 Authority

When implementation details are concerned:

* The Doublers ISA defines **what** processors shall do.
* The DCA defines **how** processors shall interpret and execute Doublers commands.

Both documents are normative.

---

## 20.7 Future Documentation

Additional project documentation may include:

* CPU Design Guides
* DoubRun Documentation
* Developer Guides
* Community Extension Specifications

These documents do not modify mandatory Base DCA behavior.

---

## 20.8 Normative Language

Within this specification:

* **Shall** indicates a mandatory requirement.
* **Should** indicates a recommendation.
* **May** indicates optional behavior.

---

## 20.9 Completion

This document defines Version 1.0 of the Doublers Command Architecture.

Future revisions shall preserve architectural stability whenever practical.

---

## 20.10 Compliance

Processors implementing this specification shall comply with both the Doublers ISA and the Doublers Command Architecture.

# Appendix A — Command Category Reference

## A.1 Overview

This appendix summarizes the architectural command categories recognized by the Doublers Command Architecture.

---

## A.2 Arithmetic Commands

Arithmetic commands perform mathematical operations upon architectural operands.

Examples include:

* ADD
* SUB
* MUL
* DIV
* MOD
* INC
* DEC
* NEG

---

## A.3 Logical Commands

Logical commands manipulate binary data.

Examples include:

* AND
* OR
* XOR
* NOT

---

## A.4 Memory Commands

Memory commands transfer data between processor registers and memory.

Examples include:

* LOAD
* STORE
* PUSH
* POP

---

## A.5 Control Flow Commands

Control flow commands modify sequential execution.

Examples include:

* JMP
* CALL
* RET
* Conditional Branches

---

## A.6 System Commands

System commands interact with processor services.

Examples include:

* SYSCALL
* BREAK
* HALT
* NOP

---

## A.7 Privileged Commands

Privileged commands execute only when sufficient architectural privilege exists.

---

## A.8 Future Categories

Compatible community additions may introduce additional command categories while preserving Base DCA compatibility.

# Appendix B — Processor Execution States

## B.1 Overview

This appendix summarizes the logical execution states of a DCA-compatible processor.

---

## B.2 Fetch

Retrieve the next Architectural Command Unit.

---

## B.3 Decode

Determine command identity and operands.

---

## B.4 Validate

Verify command correctness before execution.

---

## B.5 Execute

Perform the architectural operation.

---

## B.6 Commit

Update architectural processor state.

---

## B.7 Advance

Move to the next Architectural Command Unit.

---

## B.8 Exception

Suspend normal execution and transfer control to the architectural exception handler.

---

## B.9 Reset

Initialize processor state before execution begins.

# Appendix C — Architectural Validation Summary

## C.1 Validation Checklist

Before executing an Architectural Command Unit, processors shall verify:

* Command integrity
* Command alignment
* Instruction identity
* Operand count
* Operand types
* Register references
* Immediate value representation
* Memory permissions
* Execute permissions
* Privilege requirements

---

## C.2 Failure Handling

Validation failures shall generate the corresponding architectural exception before execution begins.

---

## C.3 Processor Guarantee

Processors shall never execute commands that fail architectural validation.

# Appendix D — Compliance Checklist

## D.1 Processor Requirements

A DCA-compatible processor shall correctly implement:

* Command Fetch
* Command Decode
* Command Validation
* Command Execution
* Processor State Management
* Memory Access Processing
* Control Flow Processing
* Exception Generation
* Privilege Enforcement
* Reset Processing

---

## D.2 Compatibility

Processors claiming compatibility shall preserve all mandatory behavior defined by:

* Doublers ISA
* Doublers Command Architecture

---

## D.3 Community Additions

Community additions shall not alter mandatory Base DCA behavior.

# Appendix E — Reserved Architectural Space

## E.1 Overview

Reserved architectural space exists to support future evolution of the Doublers architecture.

---

## E.2 Reserved Commands

Unused command representations are reserved.

Processors shall reject undefined commands unless assigned by compatible community additions.

---

## E.3 Reserved Register References

Unused register identifiers remain reserved for future expansion.

---

## E.4 Reserved Operand Types

Unused operand representations remain reserved.

---

## E.5 Reserved Immediate Formats

Unused immediate representations remain reserved.

---

## E.6 Forward Compatibility

Future DCA revisions may assign meanings to reserved architectural space while preserving compatibility whenever practical.
