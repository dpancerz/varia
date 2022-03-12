#! bin/python3

## creates a hypercube graph in graphviz format given length (default 4) of bit chain.
## example usage ./graph_viz.py 5 | dot -Tsvg > ./hyper.svg

import sys

class Vertice:
    value: int = 0

    def __str__(self) -> str:
        return f"{self.value}"


class Edge:
    start: Vertice
    end: Vertice

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self) -> str:
        return f"{self.start} -- {self.end}"


class Graph:
    vertices: set[Vertice]
    edges: set[Edge]

    def __init__(self):
        self.vertices = set()
        self.edges = set()

    def add(self, edge: Edge):
        self.edges.add(edge)
        self.vertices.add(edge.start)
        self.vertices.add(edge.end)

    def add_all(self, edges: list[Edge]):
        for i in edges:
            self.add(i)

    def __str__(self) -> str:
        return "\n".join([str(edge) for edge in self.edges])


class HipercubeVertice(Vertice):
    size: int

    def __init__(self, value, size):
        self.value = value
        self.size = size

    def neighbours(self) -> list['HipercubeVertice']:
        return [HipercubeVertice(self.value ^ off_bit, self.size) for off_bit in range(self.size)]

    def __str__(self) -> str:
        binary = bin(self.value)
        leftpadded = binary.split('b')[1].zfill(size)
        return f'" {self.value} [{leftpadded}]"'


class Hipercube:
    size: int

    def __init__(self, size):
        self.__result = Graph()
        self.size = size

        for i in range(2 ** self.size):
            vertice = HipercubeVertice(value = i, size = size)
            self.__result.add_all([Edge(vertice, neighbor) for neighbor in vertice.neighbours()])

    def __str__(self) -> str:
        return f'strict graph {{\n{self.__result}\n}}'


if __name__ == '__main__':
    size = int(sys.argv[1]) or 4
    print(Hipercube(size))

