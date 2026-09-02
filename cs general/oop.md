- Python is fully capable of OOP, and in many cases, much easier.
- Some principles may be ambiguous due to Python's dynamic typing.
- This note will teach OOP for interviews, which includes a review of the 5 core principles and teaching the syntax of OOP programming in Python vs Cpp.

# Constructors

```cpp
class Dog {
public:
	Dog(string _name, int _age) : name(name), age(age) {}

private:
	string name;
	int age;
};
```

- Cpp constructor.
- Fields are declared in their respective sections, and assigned a value with the constructor function.

```python
class Dog:
	def __init__(self, name, age):
		self.name = name
		self.age = age
```

- Python constructor.
- There isn't a field declaration section, we simply add fields to `self` in `__init__`.
- Python uses `__init__` to declare a constructor. There isn't a member declaration section, fields are simply declared in `__init__`.

# Methods

```python
class Dog:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def bark(self):
		return f"{self.name} says woof"
		
	def eat(treat):
		return f"nom"
```

- `self` is equivalent to `this` in Cpp, but I must pass it in to the first parameter to every method.
- Without `self`, a method is automatically static. No need for `static` keyword in Cpp.

# Operator Overloading

| Cpp          | Python                   |
| ------------ | ------------------------ |
| `operator==` | `__eq__(self, other)`    |
| `operator<`  | `__lt__(self, other)`    |
| `operator+`  | `__add__(self, other)`   |
| `operator<<` | `__str__(self)`          |
| `operator[]` | `__getitem__(self, key)` |
| `size()`     | `__len__(self)`          |

# Inheritance

```python
class Animal:
	def __init__(self, name):
		self.name = name
	
	def speak(self):
		pass
		
class Dog(Animal):
	def __init__(self, name):
		super().__init__(name)
	
	def speak(self):
		return "woof"
```

- `super().__init__(self)` is using the parent class' constructor.
- Methods are automatically inherited, there is no risk for slicing since everything in Python is automatically by reference and dynamically typed.

```python
class Dad:
	pass
	
class Mom:
	pass
	
class Child(Mom, Dad):
	pass
```

- Python supports multiple inheritance directly. 
- Uses ==MRO== (Method Resolution Order), leftmost parent will win for all conflicts.

# Encapsulation

```python
class Example:
	def __init__(self):
		self.publicField     = "public"
		self._protectedField = "protected"
		self.__private       = "private"
```

- Python does not have `public`, `procted`, or `private` keywords.
	- `self.name` - public
	- `self._name` - protected
	- `self.__name` - private

# Polymorphism

```python
class Animal:
	def speak(self):
		pass

class Dog(Animal):
	def speak(self):
		return "woof"

class Cat(Animal):
	def speak(self):
		return "meow"

animals = [Dog(), Cat()]
for a in animals:
	print(a.speak())
```

- Program above should output `woofmeow`.
- In Cpp, this requires the `virtual` keyword on the base method.
- In Python, **all methods are virtual by default**. No keyword needed.

```python
class Dog:
	def speak(self):
		return "woof"

class Cat:
	def speak(self):
		return "meow"

# No shared base class, still works
for a in [Dog(), Cat()]:
	print(a.speak())
```

- Because Python is dynamically typed, Polymorphism works without inheritance at all in Python. This is called ==duck typing==.
	- Program above would not work in Cpp, since `a` must be typed . 
	- Even `auto` must stick to one type, cannot switch between `Dog` and `Cat`.
	- The closest thing in Cpp is `template <typename T>`.

# Abstraction

- Hiding implementation details and exposing only the interface.
- In Cpp, this is done with pure virtual functions (`= 0`), very easy.
- In Python, this is done with the `abc` library.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
	@abstractmethod
	def area(self):
		pass

class Circle(Shape):
	def __init__(self, r):
		self.r = r

	def area(self):
		return 3.14 * self.r ** 2
```

- `Shape()` cannot be instantiated directly, just like a Cpp class with a pure virtual.
- Subclasses **must** implement all `@abstractmethod` methods or they remain abstract too.