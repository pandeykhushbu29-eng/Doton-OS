# DSH Specification

Version 0.1 Draft

Status:
Draft

Created By:
Avyaan Mishra

---

# Part I
# Foundation

# Chapter 1
## Goals

### 1.1 Purpose

The Doublers Shell (DSH) Specification defines a standard command-line shell
environment for operating systems implementing the Doton-OS Platform.

This specification standardizes command execution, scripting behavior,
environment management, pipes, redirection, and shell interoperability.

The specification SHALL define behavior rather than implementation.

---

### 1.2 Objectives

A conforming implementation SHALL:

• Execute commands.

• Execute scripts.

• Support environment variables.

• Support standard input.

• Support standard output.

• Support standard error.

• Support pipelines.

• Support redirection.

• Report standardized exit codes.

---

### 1.3 Non-goals

This specification does not define:

• GUI terminals.

• Text rendering.

• Fonts.

• Terminal emulators.

• Compiler implementation.

• Kernel implementation.

---

### 1.4 Terminology

Command

An executable operation.

Argument

A parameter supplied to a command.

Built-in

A command implemented by the shell itself.

External Command

A command executed from an executable file.

Script

A file containing DSH commands.

Environment Variable

A key/value runtime property.

---

# Chapter 2
## Architecture

### 2.1 Components

A conforming shell SHALL contain the following logical components.

• Parser

• Executor

• Environment Manager

• Process Manager

• I/O Manager

---

### 2.2 Processing Pipeline

Input

↓

Lexer

↓

Parser

↓

Command Object

↓

Execution

↓

Return Code

---

### 2.3 Runtime

The shell SHALL remain active until:

• exit command

• logout

• fatal runtime error

---

### 2.4 Prompt

The prompt format is implementation-defined.

Example:

DSH>

or

user@system>

Both are valid.

---

### 2.5 Compatibility

Commands SHALL execute identically regardless of implementation language.

---

# Chapter 3
## Command Language

### 3.1 General

The DSH command language SHALL be line-oriented.

Each command SHALL occupy one logical command line unless explicitly continued.

Blank lines SHALL be ignored.

Comments SHALL be ignored.

---

### 3.2 Command Structure

General syntax:

COMMAND [ARGUMENT]...

Examples:

print "Hello"

copy file1.txt file2.txt

mkdir Projects

delete test.txt

---

### 3.3 Command Names

Command names:

• SHALL be case-insensitive by default.

• SHALL begin with an alphabetic character.

• MAY contain:

    A-Z

    a-z

    0-9

    _

    -

Examples

Valid

print

copy

create_file

sys-info

Invalid

123print

!print

---

### 3.4 Arguments

Arguments SHALL be separated by one or more spaces.

Example

copy file1.txt file2.txt

contains

Command

copy

Argument 1

file1.txt

Argument 2

file2.txt

---

### 3.5 String Literals

Strings SHALL be enclosed by quotation marks.

Example

print "Hello World"

Escaped quotation marks SHALL be supported.

Example

print "He said \"Hello\""

---

### 3.6 Numbers

The shell SHALL recognize:

Integer

0

15

-27

Floating Point

3.14

-0.25

Scientific

2e5

---

### 3.7 Boolean Values

Supported boolean literals

true

false

Example

set debug true

---

### 3.8 Escape Characters

Minimum supported escapes

\n

newline

\t

tab

\\

backslash

\"

quotation mark

---

### 3.9 Multiple Commands

Implementations SHALL support multiple commands separated by semicolons.

Example

print "A"; print "B"; print "C"

Execution SHALL occur from left to right.

---

### 3.10 Comments

Single-line comments SHALL begin with

#

Everything following the comment marker SHALL be ignored.

Example

# this is ignored

print "Hello"

---

### 3.11 Reserved Keywords

The following words SHALL be reserved.

if

else

endif

while

endwhile

for

endfor

return

exit

break

continue

function

endfunction

---

### 3.12 Exit Codes

Every command SHALL return a status code.

0

Success

Non-zero

Failure

Implementations MAY define additional status codes.

---

# Chapter 4
## Command Execution

### 4.1 General

Commands SHALL execute sequentially unless asynchronous execution is explicitly requested.

---

### 4.2 Execution Flow

Input

↓

Parse

↓

Validate

↓

Resolve Command

↓

Execute

↓

Return Status

---

### 4.3 Built-in Commands

Built-in commands SHALL execute internally.

Examples

print

exit

cd

pwd

set

unset

---

### 4.4 External Commands

External executables SHALL be searched using the implementation-defined search path.

The shell SHALL execute the first valid executable found.

---

### 4.5 Command Lookup

Lookup priority SHALL be

1 Built-in

2 Alias

3 External executable

---

### 4.6 Arguments

Arguments SHALL be passed to the command exactly as parsed.

The shell SHALL NOT modify argument contents except escape processing.

---

### 4.7 Return Status

After execution, the shell SHALL expose the command status through the implementation-defined status variable.

Example

if status == 0

print "Success"

endif

---

### 4.8 Fatal Errors

The shell SHALL terminate only when

• exit is executed

• unrecoverable internal failure occurs

Command failures SHALL NOT terminate the shell.

---

### 4.9 Background Execution

Implementations MAY support asynchronous execution.

Example

download file.iso &

Background execution behavior SHALL be implementation-defined.

---

### 4.10 Compatibility

A conforming implementation SHALL produce equivalent observable behavior regardless of implementation language or internal architecture.

# Chapter 5
## Variables & Environment

### 5.1 General

The shell SHALL provide a runtime environment consisting of variables.

Variables MAY be created, modified, read, and deleted during execution.

---

### 5.2 Variable Names

Variable names SHALL:

• Begin with an alphabetic character or underscore.

• Contain only

    A-Z

    a-z

    0-9

    _

Examples

Valid

username

_count

FilePath

Invalid

123name

user-name

my value

---

### 5.3 Assignment

General syntax

set <name> <value>

Examples

set user "Avyaan"

set count 25

set debug true

---

### 5.4 Reading Variables

Variables SHALL be referenced using

$name

Example

print $user

Output

Avyaan

---

### 5.5 Environment Variables

The shell SHALL expose environment variables.

Minimum required variables

PATH

HOME

PWD

SHELL

USER

OS

Additional variables MAY be implemented.

---

### 5.6 Removing Variables

Syntax

unset <name>

Example

unset count

Attempting to remove a non-existent variable SHALL NOT terminate the shell.

---

### 5.7 Scope

Variables SHALL remain valid until

• removed

• shell exits

• implementation-defined scope ends

---

### 5.8 Reserved Variables

The following variable names are reserved.

status

argc

argv

PATH

HOME

PWD

SHELL

USER

Implementations SHALL NOT permit reassignment of protected variables unless explicitly documented.

---

### 5.9 Variable Expansion

Expansion SHALL occur before command execution.

Example

set name "World"

print "Hello $name"

Output

Hello World

---

### 5.10 Errors

Errors include

UNKNOWN_VARIABLE

INVALID_NAME

READ_ONLY_VARIABLE

OUT_OF_MEMORY

Variable-related failures SHALL NOT terminate the shell.

---

# Chapter 6
## Pipes & Redirection

### 6.1 General

The shell SHALL support command chaining through pipelines and input/output redirection.

---

### 6.2 Pipeline Operator

Syntax

command1 | command2

The output of command1 SHALL become the input of command2.

Example

list | filter txt

---

### 6.3 Multiple Pipelines

Multiple pipeline stages SHALL execute from left to right.

Example

list

|

filter txt

|

sort

|

print

---

### 6.4 Input Redirection

Syntax

command < file.txt

The contents of the file SHALL become standard input.

---

### 6.5 Output Redirection

Syntax

command > file.txt

Output SHALL overwrite the destination.

---

### 6.6 Append Redirection

Syntax

command >> file.txt

Output SHALL be appended.

---

### 6.7 Error Redirection

Implementations SHOULD support redirecting standard error.

Example

compile source.ds 2> errors.txt

---

### 6.8 Combined Redirection

Input and output redirection MAY be combined.

Example

sort < names.txt > sorted.txt

---

### 6.9 Pipeline Failures

If a command within a pipeline fails,

the implementation SHALL return a non-zero status.

Execution of remaining stages is implementation-defined.

---

### 6.10 Resource Management

The shell SHALL close all pipeline resources after execution.

No unused handles SHALL remain open.

---

### 6.11 Compatibility

Pipeline behavior SHALL remain consistent across all conforming implementations.

Observable command results SHALL be equivalent regardless of implementation language.

# Chapter 7
## Scripting

### 7.1 General

A DSH script is a text file containing one or more DSH commands.

Scripts SHALL execute from the first command to the last unless control flow modifies execution.

---

### 7.2 File Extension

The recommended extension is

.dsh

Implementations MAY support additional extensions.

---

### 7.3 Execution

Syntax

run script.dsh

or

script.dsh

if executable.

---

### 7.4 Comments

Comments SHALL begin with

#

Everything following the marker SHALL be ignored.

Example

# Initialize variables

set counter 0

---

### 7.5 Conditional Execution

Syntax

if <condition>

...

else

...

endif

Example

if $debug

print "Debug Mode"

else

print "Release Mode"

endif

---

### 7.6 Loops

WHILE

while <condition>

...

endwhile

FOR

for item in list

...

endfor

BREAK

Immediately exits the nearest loop.

CONTINUE

Immediately begins the next iteration.

---

### 7.7 Functions

Functions SHALL group reusable commands.

Syntax

function hello

print "Hello"

endfunction

Call

hello

---

### 7.8 Parameters

Functions MAY accept parameters.

Example

function greet name

print "Hello $name"

endfunction

greet "World"

---

### 7.9 Return

Functions MAY return a status code.

Syntax

return 0

---

### 7.10 Script Errors

Errors SHALL include

INVALID_SYNTAX

UNKNOWN_COMMAND

UNKNOWN_VARIABLE

FILE_NOT_FOUND

SCRIPT_ABORTED

Script errors SHALL terminate only the current script unless explicitly configured otherwise.

---

# Chapter 8
## Built-in Commands

### 8.1 General

Built-in commands are implemented by the shell itself.

They SHALL NOT require external executables.

---

### 8.2 Minimum Required Commands

A conforming implementation SHALL provide at least

print

echo

cd

pwd

exit

set

unset

clear

help

mkdir

rmdir

copy

move

delete

list

type

run

---

### 8.3 Command Format

Each built-in SHALL define

Purpose

Syntax

Arguments

Return Value

Errors

Examples

---

### 8.4 Example

Command

print

Purpose

Writes one or more values to standard output.

Syntax

print <expression>

Examples

print "Hello"

print $username

Return

0 on success.

Errors

INVALID_ARGUMENT

OUTPUT_FAILURE

---

### 8.5 Exit

Command

exit

Purpose

Terminates the shell.

Syntax

exit

exit 0

exit 5

---

### 8.6 Help

Command

help

Purpose

Displays available commands.

Syntax

help

help print

---

### 8.7 Working Directory

Commands

cd

pwd

SHALL manipulate or report the current working directory.

---

### 8.8 File Operations

Commands

copy

move

delete

mkdir

rmdir

list

SHALL operate on the filesystem.

Exact implementation is platform-defined.

---

### 8.9 Extensibility

Implementations MAY provide additional built-in commands.

Additional commands SHALL NOT modify the behavior of standardized commands.

---

### 8.10 Compatibility

All standardized built-in commands SHALL exhibit equivalent observable behavior across conforming implementations.

# Chapter 9
## Error Handling

### 9.1 General

A conforming DSH implementation SHALL detect, report, and recover from recoverable errors whenever possible.

Errors SHALL NOT terminate the shell unless explicitly classified as fatal.

---

### 9.2 Error Categories

Errors are classified as

• Syntax Errors

• Runtime Errors

• File Errors

• Permission Errors

• Internal Errors

---

### 9.3 Standard Error Codes

The following error codes are standardized.

0

SUCCESS

1

INVALID_ARGUMENT

2

COMMAND_NOT_FOUND

3

INVALID_SYNTAX

4

FILE_NOT_FOUND

5

PERMISSION_DENIED

6

INVALID_PATH

7

RUNTIME_ERROR

8

OUT_OF_MEMORY

9

ACCESS_DENIED

10

INTERNAL_ERROR

Implementations MAY define additional implementation-specific error codes above 100.

---

### 9.4 Error Messages

Error messages SHOULD clearly describe

• the failure

• the affected command

• the reason

Example

Error:

FILE_NOT_FOUND

details:

"notes.txt"

---

### 9.5 Command Failures

A failed command SHALL

• stop its own execution

• return a non-zero status

• leave the shell operational

---

### 9.6 Script Failures

Script execution SHALL terminate only when

• a fatal error occurs

• exit is executed

• return exits the current function

Recoverable errors MAY be ignored if explicitly configured.

---

### 9.7 Fatal Errors

Fatal errors include

• unrecoverable internal corruption

• runtime initialization failure

• memory exhaustion preventing continued execution

Fatal errors MAY terminate the shell.

---

### 9.8 Error Reporting

Implementations SHALL expose the last command status.

Example

if $status != 0

print "Failure"

endif

---

### 9.9 Compatibility

All conforming implementations SHALL produce equivalent observable failure behavior.

Internal implementation details are implementation-defined.

---

# Chapter 10
## Conformance

### 10.1 General

An implementation claiming DSH compatibility SHALL satisfy every mandatory requirement defined by this specification.

---

### 10.2 Mandatory Features

A conforming shell SHALL provide

✓ Command execution

✓ Variables

✓ Environment variables

✓ Built-in commands

✓ External commands

✓ Pipelines

✓ Input redirection

✓ Output redirection

✓ Scripts

✓ Standard exit codes

✓ Error reporting

---

### 10.3 Optional Features

The following features are optional.

• Background execution

• Command aliases

• Auto-completion

• Syntax highlighting

• History

• Themes

• Plugin systems

Optional features SHALL NOT change standardized behavior.

---

### 10.4 Version Reporting

Implementations SHOULD expose

Shell Name

Version

Specification Version

Example

DSH

Version 1.2

Compatible with DSH Specification 0.1

---

### 10.5 Compatibility Statement

Implementations MAY advertise compatibility using

"DSH Compatible"

only if all mandatory requirements are implemented.

---

### 10.6 Deprecated Features

Deprecated behavior SHALL remain supported until removed by a future specification revision.

---

### 10.7 Future Compatibility

Implementations SHOULD ignore unknown optional extensions whenever practical.

---

### 10.8 Compliance

Compliance SHOULD be verified using

• command execution tests

• scripting tests

• pipeline tests

• variable tests

• filesystem tests

• error handling tests

---

### 10.9 Specification Updates

Future specification versions SHALL preserve backwards compatibility whenever practical.

Breaking changes SHALL require a major specification version.

---

### 10.10 Summary

This specification defines the observable behavior of the Doublers Shell.

Implementations remain free to choose any internal architecture, programming language, parser, or execution engine, provided all externally visible behavior conforms to this specification.

---

# Appendix A
## DSH Grammar

Basic Command

COMMAND [ARGUMENT]...

Variable

$name

Assignment

set name value

Function

function name

...

endfunction

Conditional

if condition

...

endif

Loop

while condition

...

endwhile

Pipeline

command1 | command2

Redirection

command > file

command >> file

command < file

---

# Appendix B
## Standard Built-in Commands

Required Commands

print

echo

help

exit

cd

pwd

set

unset

mkdir

rmdir

copy

move

delete

list

type

run

Optional Commands

history

alias

clear

which

time

sleep

---

# Appendix C
## Example Scripts

Example 1

print "Hello World"

Example 2

set name "Avyaan"

print "Welcome $name"

Example 3

if $debug

print "Debug"

else

print "Release"

endif

Example 4

list | filter txt > files.txt

Example 5

function greet person

print "Hello $person"

endfunction

greet "World"

---

END OF DSH SPECIFICATION

Version 0.1 Draft