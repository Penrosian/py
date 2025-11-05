import doctest

class NumberSet:
    """
      >>> nums = NumberSet([2, 4, 6])
      >>> print(nums)
      [2, 4, 6]
      >>> nums.mean()
      4.0
      >>> nums.median()
      4
      >>> nums.mode()
      [2, 4, 6]
      >>> nums2 = NumberSet([1, 2, 6, 6])
      >>> nums2.mean()
      3.75
      >>> nums2.median()
      4.0
      >>> nums2.mode()
      [6]
      >>> numset = [3, 5, 19, 42, 5, 42, 11]
      >>> nums3 = NumberSet(numset)
      >>> nums3.numlist
      [3, 5, 5, 11, 19, 42, 42]
      >>> numset
      [3, 5, 19, 42, 5, 42, 11]
      >>> round(nums3.mean())
      18
      >>> nums3.median()
      11
      >>> nums3.mode()
      [5, 42]
    """

    def __init__(self, numlist: list[float]):
        self.numlist = sorted(numlist)

    def __str__(self):
        return str(self.numlist)

    def mean(self):
        return sum(self.numlist) / len(self.numlist)

    def median(self):
        n = len(self.numlist)
        mid = n // 2
        if n % 2 == 0:
            return (self.numlist[mid - 1] + self.numlist[mid]) / 2
        else:
            return self.numlist[mid]

    def mode(self):
        frequency = {}
        for num in self.numlist:
            frequency[num] = frequency.get(num, 0) + 1
        max_freq = max(frequency.values())
        modes = [num for num, freq in frequency.items() if freq == max_freq]
        return modes
    
class Student:
    """
      >>> student = Student('Gizelle', 'Day', 11)
      >>> student.fname
      'Gizelle'
      >>> student.lname
      'Day'
      >>> student.grade
      11
    """
    def __init__(self, fname: str, lname: str, grade: int):
        self.fname = fname
        self.lname = lname
        self.grade = grade

class Polynomial:
    """
      >>> p1 = Polynomial()
      >>> print(p1)
      0
      >>> p2 = Polynomial([3, 1, 5])
      >>> print(p2)
      3x^2 + x + 5
      >>> p3 = Polynomial([2, 3, 1, 5])
      >>> print(p3)
      2x^3 + 3x^2 + x + 5
      >>> p4 = Polynomial([2, 0, 3, 7, 2])
      >>> print(p4)
      2x^4 + 3x^2 + 7x + 2
    """
    def __init__(self, coefficients: list[float] = [0]):
        self.coefficients = coefficients

    def __str__(self):
        terms = []
        degree = len(self.coefficients) - 1
        for i, coeff in enumerate(self.coefficients):
            power = degree - i
            if coeff != 0:
                if power == 0:
                    terms.append(f"{coeff}")
                elif power == 1:
                    terms.append(f"{coeff}x" if coeff != 1 else "x")
                else:
                    terms.append(f"{coeff}x^{power}" if coeff != 1 else f"x^{power}")
        return " + ".join(terms) if terms else "0"

class Time:
    """
    >>> time1 = Time(1, 30, 45)
    >>> time1.increment(10)
    >>> time1.print_time()
    1:30:55
    >>> time1.increment(10)
    >>> time1.print_time()
    1:31:05
    """
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
    
    def print_time(self):
        print(f'{self.hours}:{self.minutes:02d}:{self.seconds:02d}')
    
    def increment(self, seconds):
        self.seconds = seconds + self.seconds
        
        self.minutes = self.minutes + self.seconds // 60
        self.seconds = self.seconds % 60

        self.hours = self.hours + self.minutes // 60
        self.minutes = self.minutes % 60
    
    def after(self, other):
        if self.hours > other.hours:
            return True
        if self.hours < other.hours:
            return False

        if self.minutes > other.minutes:
            return True
        if self.minutes < other.minutes:
            return False

        if self.seconds > other.seconds:
            return True
        return False

def increment(time, seconds):
    """
    >>> time1 = Time(1, 30, 45)
    >>> new_time = increment(time1, 20)
    >>> new_time.print_time()
    1:31:05
    """
    time_seconds = time.seconds + seconds

    time_minutes = time.minutes + time_seconds // 60
    time_seconds = time_seconds % 60

    time_hours = time.hours + time_minutes // 60
    time_minutes = time_minutes % 60

    return Time(time_hours, time_minutes, time_seconds)

if __name__ == "__main__":
    doctest.testmod()