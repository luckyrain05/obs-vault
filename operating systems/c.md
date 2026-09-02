# Hello World 

```c
#include <studio.h>

int main() {
	printf("hello world\n");
	return 0;
}
```

- Library <studio.h> imports the printf function, which is just a print statement.

```c
for (int i=0; i<argc; i++) {
	printf("param, %d: %s", i, argv[i]);
}
```

- - Prefix `%` defines the variable after as a placeholder, value defined by variable after `,` .

# Pointers

```c
int x = 10;
int *ptr = &x;
printf("%d\n", *ptr);  // prints 10
```

- Ptr syntax and arithmetic are mostly the same as cpp, except with strings.
- Key thing to remember is [[memory#Pointers|pointer arithmetic]].

# [[arrays]]

```c
// line 1
int x[10];
// line 2
char hello[] = "hi";
```

- C is super low level. Arrays are implemented with [[memory#Pointers|pointers]] and navigated with raw pointer arithmetic.
- The syntax `[]` will ==decay== into `*` by the compiler. 
- It is not strictly the same thing since we still have array sizes to worry about, and the compiler must declare a chunk of memory to "belong" to the array. 
	- `int x[10]` -> `int *x`
	- `char hello[]` -> `char *hello`

- Line 1 declares an empty array of ints with size 10.
- Line 2 declares the array `['h', 'i', '\0'];`. 

# Strings

```c
char *greeting = "hello";

char *words[] = {"apple", "banana", "cherry"};

printf("%s\n", ptr[0]);   // prints "apple"
printf("%s\n", ptr[1]);   // prints "banana"
printf("%c\n", ptr[1][0]); // prints 'b' (first char of "banana")
```

- `greeting` = `['h', 'e', 'l', 'l', 'o', '\0']`. 
- Strings in C are arrays of characters, there does not exist a `string` data type.
- The compiler will always add the null element`\0` to the end of `char*` to signify the end of the string.

- Every character is a byte, including `/0`. 
**sizeof()**
- Counts total bytes allocated of an array, includes `/0`.
**strlen()**
- Counts total bytes until `/0`. Does not include `/0` and isolating the string.

# Compiling and Running

```bash
gcc hello.c -o hello
./hello
Hello, world
```

- Terminal commands above invokes gcc compiler on hello.c
	a. Called the c preprocessor (cpp) on hello.c.
	b. cpp looked for stdio.h in the default path, which includes the needed header files.
	c. The output of step b pasted into hello.c, result compiled by gcc into binary.

```c
int main(int argc, char** argv) {
	printf("The numer of param is %d", argc);
	return 0;
}
```

- When we start a program with `./program arg1 arg2` in the shell, the kernel reads the command line and loads it into our new [[processes|process]].
	- `argc` == 3 because we pass in 2 arguments + the program name itself.
	- `argv` is an array of strings:
		1. `argv[0]` == ./program
		2. `argv[1]` == arg1
		3. `argv[2]` == arg2

- The return 0 is not strictly necessary on the main function.

# Casting

```c
#include <stdio.h>
int main() {
	char x[] = “POLY”;
	int *y;
	y = (int *) &x;
	printf(“%s is %d\n”, x, *y);
	return 0;
}
```

- `y = (int *) &x` casts the string array `x` into an integer of its [[memory#Memory Addresses|memory address]], remember [[memory#Pointers|pointer arithmetic]].
- To copy a `const` variable and modify the copy, we must cast as well.

# Malloc and Free

```c
void* malloc (size_t size):

void free(void* ptr):
```

- c is a low level language, it deals with [[memory]] addresses directly.
**malloc**:
- allocate block of memory `size` bytes.
- does not initialize memory
**free**:
- frees the allocated block
- Always free what we malloc to prevent memory leaks.

# Stack vs Heap Allocation

- Local vars and func args are placed on the ==stack==.
	- Scope only.
- Memory allocated by calls to malloc are placed on the ==heap==.
	- Global.

# C Libraries

- `string.h`
	- Copying: 
		- `void* memcpy (void* dest, void* src, size_t n)`
		- copy n bytes of src into dest
	- Concatenation:
		- `char* strcpy(char* dest, char* src)`
		- append copy of src to end of dest, return dest
	- Comparison:
		- `int strcmp (char* str1, char* str2) : compare str1, str2`
		- compares two strings by ascii values while iterating through, then by len
			- `str1` < `str2`: -1
			- `str1`== `str2`: 0
			- `str1` > `str2`: 1
	- Searching:
		- `char* strstr (char* str1, char* str2)`
		- return ptr to first occurrence of str2 in str1, else null