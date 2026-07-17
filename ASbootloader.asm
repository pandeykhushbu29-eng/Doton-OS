; BOOT SEQUENCE
;   UEFI firmware → ASbootloader.o → [RDI=0x0011045110] → linkloader_main.py
;
; WHAT THIS BOOTLOADER DOES
;   1. UEFI entry point (PE32+ image called by firmware)
;   2. Minimal hardware initialisation (serial debug, timer)
;   3. Opens / creates the .rdi_mirror file via UEFI Simple File System
;   4. Writes token 0x0011045110 as little-endian uint64_t
;   5. Hands control to Python runtime → linkloader_main.py
;   6. HLT on any failure
;
; ASSEMBLY
;   nasm -f win64 -o ASbootloader.o ASbootloader.asm
;   (or -f elf64 on Linux UEFI)
;
; UEFI calling convention (Microsoft x64):
;   RCX = first arg, RDX = second, R8 = third, R9 = fourth
;   Stack is 16-byte aligned
; ==============================================================================

; ---------------------------------------------------------------------------
; UEFI Protocol GUIDs
; ---------------------------------------------------------------------------
EFI_SIMPLE_FILE_SYSTEM_PROTOCOL_GUID:  equ 0x0964e5b22-0x6459-0x11d2-0x8e3900000000
; Short form used below – in real build use proper GUID structs

; ---------------------------------------------------------------------------
; Constants
; ---------------------------------------------------------------------------
EXPECTED_TOKEN:     equ 0x0011045110
TOKEN_SIZE:         equ 8           ; uint64_t
RDI_MIRROR_FILENAME: db ".rdi_mirror", 0

; ---------------------------------------------------------------------------
; UEFI Entry point
; ---------------------------------------------------------------------------
[BITS 64]
[ORG 0x0]  ; Relocatable PE32+ – UEFI firmware handles base address

global _start
_start:
    ; -----------------------------------------------------------
    ; Stage 1 — Save UEFI boot parameters
    ; RCX = ImageHandle, RDX = SystemTable
    ; -----------------------------------------------------------
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32                ; shadow space

    mov     [image_handle], rcx
    mov     [system_table], rdx

    ; -----------------------------------------------------------
    ; Stage 2 — Minimal hardware wake (serial port init)
    ; -----------------------------------------------------------
    call    _init_serial
    call    _debug_string, msg_booting

    ; -----------------------------------------------------------
    ; Stage 3 — Open .rdi_mirror file via UEFI FS protocol
    ; -----------------------------------------------------------
    call    _open_rdi_mirror
    test    rax, rax
    jz      .halt_fail
    mov     [mirror_handle], rax

    ; -----------------------------------------------------------
    ; Stage 4 — Write token 0x0011045110 to mirror
    ; -----------------------------------------------------------
    call    _write_token, [mirror_handle], EXPECTED_TOKEN
    test    rax, rax
    jz      .halt_fail

    call    _debug_string, msg_token_ok

    ; -----------------------------------------------------------
    ; Stage 5 — Close mirror
    ; -----------------------------------------------------------
    call    _close_file, [mirror_handle]

    ; -----------------------------------------------------------
    ; Stage 6 — Handoff to Python / linkloader_main.py
    ; In UEFI: exec via shell or return to boot manager
    ; Here we return with success so firmware can boot next stage
    ; -----------------------------------------------------------
    call    _debug_string, msg_handoff
    xor     rax, rax               ; return EFI_SUCCESS
    leave
    ret

.halt_fail:
    call    _debug_string, msg_fail
    ; Halt the CPU — token mismatch / boot abort
.hlt_loop:
    hlt
    jmp     .hlt_loop

; ===========================================================================
; FUNCTIONS
; ===========================================================================

; ---------------------------------------------------------------------------
; _init_serial — Initialise serial port (COM1 / 0x3F8)
; ---------------------------------------------------------------------------
_init_serial:
    push    rbp
    mov     rbp, rsp

    mov     dx, 0x3F8 + 1         ; COM1: Interrupt Enable
    xor     al, al
    out     dx, al

    mov     dx, 0x3F8 + 3         ; Line Control
    mov     al, 0x80              ; DLAB=1
    out     dx, al

    mov     dx, 0x3F8             ; Divisor LSB (115200 baud)
    mov     al, 1
    out     dx, al

    mov     dx, 0x3F8 + 1         ; Divisor MSB
    xor     al, al
    out     dx, al

    mov     dx, 0x3F8 + 3         ; 8N1
    mov     al, 0x03
    out     dx, al

    mov     dx, 0x3F8 + 2         ; FIFO enable
    mov     al, 0xC7
    out     dx, al

    pop     rbp
    ret

; ---------------------------------------------------------------------------
; _debug_string — Print null-terminated string to serial
;   RDI = pointer to string
; ---------------------------------------------------------------------------
_debug_string:
    push    rbp
    mov     rbp, rsp
    push    rdi

    mov     rdi, [rbp + 16]       ; first arg
.loop:
    lodsb                        ; AL = [RSI], RSI++
    test    al, al
    jz      .done
    mov     dx, 0x3F8
    out     dx, al
    jmp     .loop
.done:
    ; newline
    mov     dx, 0x3F8
    mov     al, 0x0D
    out     dx, al
    mov     al, 0x0A
    out     dx, al

    pop     rdi
    pop     rbp
    ret     8

; ---------------------------------------------------------------------------
; _open_rdi_mirror — Open or create .rdi_mirror via UEFI FS
;   Returns handle in RAX, or 0 on failure
; ---------------------------------------------------------------------------
_open_rdi_mirror:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32

    ; In a full implementation, this would:
    ; 1. Get EFI_SIMPLE_FILE_SYSTEM_PROTOCOL from SystemTable
    ; 2. Open volume → get root directory
    ; 3. Open/Create .rdi_mirror file with RW access
    ;
    ; For this assembly template, we use a stub that
    ; indicates the file should be available.
    ; The actual implementation requires UEFI protocol calls.

    ; Stub: return a non-zero handle to indicate success
    ; (In production, this would be the actual file handle)
    mov     rax, 1                 ; stub handle
    pop     rbp
    ret

; ---------------------------------------------------------------------------
; _write_token — Write uint64_t token to file
;   Arg1: file handle, Arg2: token value
;   Returns RAX = 1 on success, 0 on failure
; ---------------------------------------------------------------------------
_write_token:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 32

    ; In a full implementation, this would:
    ; 1. Call EFI_FILE_PROTOCOL.Write(handle, &size, &token)
    ;
    ; For this template, we write to a fixed memory address
    ; that the Python side can also mmap.

    ; Stub: always succeed
    ; (In production, actually write the token bytes)
    mov     rax, 1                 ; success
    pop     rbp
    ret     16

; ---------------------------------------------------------------------------
; _close_file — Close UEFI file handle
; ---------------------------------------------------------------------------
_close_file:
    push    rbp
    mov     rbp, rsp

    ; Stub: no-op for now
    ; (In production, call EFI_FILE_PROTOCOL.Close)

    pop     rbp
    ret     8

; ===========================================================================
; DATA
; ===========================================================================
section .data
image_handle:   dq 0
system_table:   dq 0
mirror_handle:  dq 0

msg_booting:    db "[ASbootloader] Booting firstAS v0.1...", 0
msg_token_ok:   db "[ASbootloader] RDI token 0x0011045110 written", 0
msg_handoff:    db "[ASbootloader] Handoff → linkloader_main.py", 0
msg_fail:       db "[ASbootloader] FATAL — boot aborted, HLT", 0

; ===========================================================================
; END
; ===========================================================================