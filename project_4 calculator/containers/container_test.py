"""Test Container Package"""
from project_4.ontainers.queue import Queue
from project_4.containers.stack import Stack

# Test queue structure

queue = Queue()
assert queue.is_empty()
queue.push(1)
assert not queue.is_empty()
queue.push(2)
assert queue.peek() == 1
assert queue.pop() == 1
queue.push(3)
assert queue.peek() == 2

# Test stack structure
stack = Stack()
assert stack.is_empty()
stack.push(1)
assert not stack.is_empty()
stack.push(2)
assert stack.peek() == 2
assert stack.pop() == 2
stack.push(3)
assert stack.peek() == 3
