---

## Một số từ khóa/decorator nâng cao khác

**@abstractmethod, @abstractclassmethod, @abstractstaticmethod**
- Định nghĩa phương thức trừu tượng trong abstract class (dùng module `abc`).
- **Ví dụ:**
```python
from abc import ABC, abstractmethod
class Animal(ABC):
	@abstractmethod
	def speak(self):
		pass
```

**@dataclass**
- Tự động sinh các method như `__init__`, `__repr__`, `__eq__` cho class dữ liệu (Python 3.7+).
- **Ví dụ:**
```python
from dataclasses import dataclass
@dataclass
class Point:
	x: int
	y: int
p = Point(1, 2)
print(p)
```

**@overload**
- Hỗ trợ type hint cho các hàm đa hình (module `typing`).
- **Ví dụ:**
```python
from typing import overload
class Example:
	@overload
	def func(self, x: int) -> int: ...
	@overload
	def func(self, x: str) -> str: ...
```

**@final**
- Đánh dấu method/class không cho phép override/kế thừa (Python 3.8+).
- **Ví dụ:**
```python
from typing import final
@final
class Base: ...
```

**__slots__**
- Giới hạn thuộc tính có thể gán cho object, tối ưu bộ nhớ.
- **Ví dụ:**
```python
class A:
	__slots__ = ['x', 'y']
	def __init__(self):
		self.x = 1
		self.y = 2
```

**@property.setter, @property.deleter**
- Mở rộng thuộc tính property cho phép gán/xóa giá trị.
- **Ví dụ:**
```python
class Person:
	def __init__(self, name):
		self._name = name
	@property
	def name(self):
		return self._name
	@name.setter
	def name(self, value):
		self._name = value
```

**isinstance(), issubclass()**
- Kiểm tra kiểu và quan hệ kế thừa giữa các class/object.
- **Ví dụ:**
```python
class A: pass
class B(A): pass
print(isinstance(B(), A))  # True
print(issubclass(B, A))    # True
```
---



## Nguồn tài liệu chính thức

- [Python OOP documentation](https://docs.python.org/3/tutorial/classes.html)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Python abc module](https://docs.python.org/3/library/abc.html)
- [Python typing module](https://docs.python.org/3/library/typing.html)

# Các từ khóa và decorator thường dùng với OOP trong Python


1. **@classmethod**
	 - Định nghĩa phương thức lớp. Tham số đầu tiên là `cls` (class), cho phép gọi method mà không cần tạo instance. Thường dùng để khởi tạo object từ dữ liệu ngoài (như from_dict).
	 - **Ví dụ:**
		 ```python
		 class MyClass:
				 @classmethod
				 def from_dict(cls, data):
						 return cls(**data)
		 obj = MyClass.from_dict({'a': 1, 'b': 2})
		 ```


2. **@staticmethod**
	 - Định nghĩa phương thức tĩnh. Không nhận `self` hay `cls`. Dùng cho logic không phụ thuộc vào instance hay class.
	 - **Ví dụ:**
		 ```python
		 class Math:
				 @staticmethod
				 def add(a, b):
						 return a + b
		 print(Math.add(2, 3))  # 5
		 ```


3. **@property**
   - Biến một method thành thuộc tính chỉ đọc. Giúp truy cập như thuộc tính thông thường nhưng có thể tính toán động.
   - **Ví dụ:**
	 ```python
	 class Person:
		 def __init__(self, name):
			 self._name = name
		 @property
		 def name(self):
			 return self._name.upper()
	 p = Person('Nam')
	 print(p.name)  # NAM
	 ```


4. **super()**
   - Gọi phương thức của lớp cha, thường dùng trong kế thừa để mở rộng hoặc ghi đè hành vi.
   - **Ví dụ:**
	 ```python
	 class Animal:
		 def speak(self):
			 print('Animal speaks')
	 class Dog(Animal):
		 def speak(self):
			 super().speak()
			 print('Dog barks')
	 d = Dog()
	 d.speak()
	 # Animal speaks
     # Dog barks
	 ```


5. **self**
   - Tham chiếu đến chính instance hiện tại của class. Dùng trong mọi method của object.
   - **Ví dụ:**
	 ```python
	 class Counter:
		 def __init__(self):
			 self.count = 0
		 def inc(self):
			 self.count += 1
	 c = Counter()
	 c.inc()
	 print(c.count)  # 1
	 ```


6. **cls**
	 - Tham chiếu đến class hiện tại. Dùng trong classmethod.
	 - **Ví dụ:**
		 ```python
		 class A:
				 @classmethod
				 def whoami(cls):
						 print(cls.__name__)
		 A.whoami()  # A
		 ```


7. **__init__, __str__, __repr__, __eq__, ...**
   - Các magic method (dunder method) để tùy biến hành vi của object (khởi tạo, in ra, so sánh, ...).
   - **Ví dụ:**
	 ```python
	 class Point:
		 def __init__(self, x, y):
			 self.x = x
			 self.y = y
		 def __repr__(self):
			 return f"Point({self.x}, {self.y})"
		 def __eq__(self, other):
			 return self.x == other.x and self.y == other.y
	 p1 = Point(1, 2)
	 p2 = Point(1, 2)
	 print(p1)        # Point(1, 2)
	 print(p1 == p2)  # True
	 ```

## Một số từ khóa/decorator nâng cao khác

8. **@abstractmethod, @abstractclassmethod, @abstractstaticmethod**
   - Định nghĩa phương thức trừu tượng trong abstract class (dùng module `abc`).
   - **Ví dụ:**
	 ```python
	 from abc import ABC, abstractmethod
	 class Animal(ABC):
		 @abstractmethod
		 def speak(self):
			 pass
	 ```

9. **@dataclass**
   - Tự động sinh các method như `__init__`, `__repr__`, `__eq__` cho class dữ liệu (Python 3.7+).
   - **Ví dụ:**
	 ```python
	 from dataclasses import dataclass
	 @dataclass
	 class Point:
		 x: int
		 y: int
	 p = Point(1, 2)
	 print(p)
	 ```

10. **@overload**
	- Hỗ trợ type hint cho các hàm đa hình (module `typing`).
	- **Ví dụ:**
	  ```python
	  from typing import overload
	  class Example:
		  @overload
		  def func(self, x: int) -> int: ...
		  @overload
		  def func(self, x: str) -> str: ...
	  ```

11. **@final**
	- Đánh dấu method/class không cho phép override/kế thừa (Python 3.8+).
	- **Ví dụ:**
	  ```python
	  from typing import final
	  @final
	  class Base: ...
	  ```

12. **__slots__**
	- Giới hạn thuộc tính có thể gán cho object, tối ưu bộ nhớ.
	- **Ví dụ:**
	  ```python
	  class A:
		  __slots__ = ['x', 'y']
		  def __init__(self):
			  self.x = 1
			  self.y = 2
	  ```

13. **@property.setter, @property.deleter**
	- Mở rộng thuộc tính property cho phép gán/xóa giá trị.
	- **Ví dụ:**
	  ```python
	  class Person:
		  def __init__(self, name):
			  self._name = name
		  @property
		  def name(self):
			  return self._name
		  @name.setter
		  def name(self, value):
			  self._name = value
	  ```

14. **isinstance(), issubclass()**
	- Kiểm tra kiểu và quan hệ kế thừa giữa các class/object.
	- **Ví dụ:**
	  ```python
	  class A: pass
	  class B(A): pass
	  print(isinstance(B(), A))  # True
	  print(issubclass(B, A))    # True
	  ```

---