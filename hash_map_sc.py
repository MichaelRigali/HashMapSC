# Name: Michael Rigali
# OSU Email: rigalim@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 Portfolio Project
# Due Date: March 17th 2023
# Description: Covers Module 8 (Hash Maps)


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        A method that updates the key/value pair in the hash map. If the given key already exists in the hash map,
        its associated value must be replaced with the new value. If the given key is not in the map, a new key/value
        pair is added.

        Note: For this hash map implementation, the table must be resized to double its current capacity when this
        method is called and the current load factor of the table is greater than or equal to 1.0.

        :param key: Of string type.
        :param value: Of object type.

        :return: None type.
        """
        hash = self._hash_function(key)
        if self.table_load() >= 1:
            new_capacity = self._capacity * 2
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)
            index = hash % new_capacity
            self.resize_table(new_capacity)
        else:
            index = hash % self._capacity
        if self._buckets[index].contains(key):
            self._buckets[index].remove(key)
        else:
            self._size += 1
        self._buckets[index].insert(key, value)

    def empty_buckets(self) -> int:
        """
        A method that returns the number of empty buckets in the hash table.

        :return: An integer type (# of empty buckets in hash table).
        """
        counter = 0
        for bucket in range(0, self._buckets.length()):
            if self._buckets[bucket].length() == 0:
                counter += 1
        return counter

    def table_load(self) -> float:
        """
        A method that returns the current hash table load factor.

        :return: Float type (load factor).
        """
        # The ratio of links divided by the number of buckets
        return self._size / self._capacity

    def clear(self) -> None:
        """
        A method that clears the contents of the hashmap without changing the underlying hash table capacity.

        :return: None type.
        """
        for bucket in range(0, self._buckets.length()):
            if self._buckets[bucket].length() != 0:
                self._buckets[bucket] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        A method that changes the capacity of the internal hash table. All existing key/value pairs
        must remain in the new hash map, and all hash table links must be rehashed.
        If the new_capacity is less than 1, the method does nothing.
        If the new_capacity is 1 or more, it must be a prime number. If not, it is changed to the next highest
        prime number.

        :param new_capacity: Of integer type.

        :return: None type.
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        self._size = 0
        temp_buckets = self._buckets
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())
        for bucket_index in range(temp_buckets.length()):
            bucket = temp_buckets[bucket_index]
            for thing in bucket:
                self.put(thing.key, thing.value)

    def get(self, key: str) -> object:
        """
        A method that returns the value associated with the given key provided as a parameter. If the key is not in the
        hash map, the method returns None.

        :param key: String type.

        :return: The value of object type.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index] is not None:
            if self._buckets[index].contains(key) is not None:
                return self._buckets[index].contains(key).value
        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise it returns False. Noe to self, an
        empty hash map does not contain any keys.

        :param key: String type

        :return: Boolean type.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        bucket = self._buckets[index]
        if bucket is not None:  # if the bucket is not none then do the following
            for item in bucket:
                if item.key == key:
                    return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map. If the key
        is not in the hash map, the method does nothing (no exception needs to be raised).

        :param key: Of string type which also removes its associated value

        :return: None type
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        A method that returns a dynamic array where each index contains a tuple of a key/value pair
        stored in the hash map. Note, the order of keys in the dynamic array does not matter.

        :return: Dynamic Array type.
        """
        DA = DynamicArray()
        for i in range(self._buckets.length()):
            for node in self._buckets.get_at_index(i):
                DA.append((node.key, node.value))
        return DA


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    A standalone function that rec's a dynamic array that is not gaurenteed to be sorted. It returns a tuple containing
    a dynamic array comprising the mode of the array, and an integer that represents the frequency. If there is more
    than one value with the highest frequency, all values at that frequency will be included in the dynamic array
    being returned.

    :param da: Of Dynamic Array type.

    :return: A tuple containing a dynamic array (mode(s)) and an integer of the highest frequency.
    """
    # Initialize the map
    map = HashMap()
    # Iterate through the elements of the dynamic array
    for index in range(0, da.length()):
        ele = da[index]
        # If the key appears one time, assign a value of 1
        if map.contains_key(ele) is False:
            map.put(ele, 1)
        # If this is not the first time the key appears, increment the value by 1
        else:
            map.put(ele, map.get(ele) + 1)
    # Step 1
    #  Determine the number of occurences of each key
    # map.get(some_key)
    # Step 2
    #  get the key that has the max occurences assuming there is only 1 (i.e. find the key with the largest paired value)
    max_occurences = 0
    mode_element = DynamicArray()
    keys_values = map.get_keys_and_values()
    for index in range(0, keys_values.length()):
        (ele, num_occurences) = keys_values[index]
        if num_occurences > max_occurences:
            max_occurences = num_occurences
            mode_element = DynamicArray()
            mode_element.append(ele)
        # Step 3
        #  get all keys that have all max occurences
        elif num_occurences == max_occurences:
            max_occurences = num_occurences
            mode_element.append(ele)
    return mode_element, max_occurences


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")