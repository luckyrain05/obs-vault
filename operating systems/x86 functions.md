- [[x86 assembly]] function calling, conventions, and [[x86 assembly#Memory Stack|stack]] frames.

# Stack Frames

- Each function call creates a ==stack frame== delimited by two pointers:
	- `EBP`
		- ==frame pointer== (base of current frame).
	- `ESP`
		- ==stack pointer== (top of stack / end of current frame).
- Function arguments and local variables are accessed as offsets from `EBP`.

# Functions

- x86 supports function declaration.
- Call a function with `call label`.
- Every function sets up and tears down its stack frame with a standard ==prologue== and ==epilogue==.

**Prologue** 

- runs at the start of every function:

```nasm
push ebp              ; save caller's frame pointer
mov ebp, esp          ; set new frame pointer to current top of stack
sub esp, X            ; reserve X bytes for local variables
```

**Epilogue** -- runs at the end to undo the prologue:

```nasm
mov esp, ebp          ; discard locals (restore esp to frame base)
pop ebp               ; restore caller's frame pointer
ret                   ; pop return address and jump to it
```

- The `leave` instruction is a shorthand for the first two lines of the epilogue (`mov esp, ebp` + `pop ebp`).
- In practice, everything can be omitted expect `ret`, which stops the function and returns to the caller's frame.

**Operations**
- `call label` -- pushes the address of the next instruction onto the stack, then jumps to `label`.
- `ret` -- pops the return address off the stack and jumps to it.

```nasm
; caller
push 5                ; push argument
call myFunc           ; push return addr, jump to myFunc
add esp, 4            ; clean up argument (caller cleans in cdecl)

; callee
myFunc:
    push ebp          ; save old base pointer
    mov ebp, esp      ; set up new stack frame
    mov eax, [ebp + 8] ; first argument is at ebp + 8
    ; ... function body ...
    pop ebp           ; restore old base pointer
    ret               ; return to caller
```

**Call Stack**
- After the caller pushes the argument and `call` pushes the return address, the callee's prologue saves `EBP` and sets the new frame. The resulting stack frame:

```
+------------------+
| argument (5)     |  <- [ebp + 8]  pushed by caller
+------------------+
| return address   |  <- [ebp + 4]  pushed by call instruction
+------------------+
| saved ebp        |  <- ebp        pushed by callee prologue
+------------------+
| local variables  |  <- esp        reserved by sub esp, X
+------------------+
```

- Each slot is 4 bytes. `EBP` is the anchor -- it does not move during the function, so arguments and locals are always at fixed offsets from it.

- `EAX` holds the return value.
- `EBX`, `ESI`, `EDI`, `EBP` are ==callee-saved==.
	- The called function must preserve them.
- `EAX`, `ECX`, `EDX` are ==caller-saved==.
- The caller must save them if it needs them after the call.

# Calling Convention

- The calling convention is system defined, it tells the programmer how to call a function.
- On x86 linux, the convention is named ==cdecl==.

# cdecl

- Caller is responsible for cleaning arguments off the stack.
- This allows functions with variable numbers of arguments.
- `EAX`, `ECX`, `EDX` may be trashed by callee and must be saved by caller.
- `EBP`, `EBX`, `ESI`, `EDI` must be preserved by callee.

[[c]]