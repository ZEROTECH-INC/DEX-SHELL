; DEX Boot Loader (simulation only)
; Assembler: NASM
BITS 64
ORG 0x7C00

start:
    mov si, msg_boot
    call print_string
    hlt

print_string:
    mov ah, 0x0E
.next:
    lodsb
    or al, al
    jz .done
    int 0x10
    jmp .next
.done:
    ret

msg_boot db "DEX Bootloader Activated - Sim Mode", 0
TIMES 510-($-$$) db 0
DW 0xAA55