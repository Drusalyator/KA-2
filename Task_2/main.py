"""Модуль решающий задачу о наибольшем паросочетании через алгоритм Форда-Фалкерсона"""


class Edge:
    """Класс ребра"""
    def __init__(self, source: str, target: str, capacity: int):
        """Конструктор"""
        self.source = source
        self.target = target
        self.capacity = capacity
        self.reverse_edge = None

    def __str__(self):
        """Строковое представление"""
        return f'{self.source}->{self.target}  {self.capacity}'

    def __repr__(self):
        """Строковое представление"""
        return f'{self.source}->{self.target}  {self.capacity}'


class Resolver:
    """Класс сети"""
    def __init__(self):
        """Конструктор"""
        self.agjacent_vertices = {}
        self.edge_flow = {}
        self._read_data()
        self.max_flow('s', 't')
        self.matching = self.get_matching()
        self.write_result(self.get_matching())

    def add_vertex(self, vertex: str):
        """Добавление вершины в сеть"""
        self.agjacent_vertices.update({vertex: []})

    def get_incident_edges(self, vertex: str) -> [str]:
        """Получение массива нцидентных вершине ребер"""
        return self.agjacent_vertices[vertex]

    def add_edge(self, source: str, target: str, capacity=1):
        """Добавление ребра"""
        edge = Edge(source, target, capacity)
        reverse_edge = Edge(target, source, 0)
        edge.reverse_edge = reverse_edge
        reverse_edge.reverse_edge = edge
        if self.agjacent_vertices.get(source) is None:
            self.agjacent_vertices.update({source: [edge]})
        else:
            self.agjacent_vertices[source].append(edge)
        if self.agjacent_vertices.get(target) is None:
            self.agjacent_vertices.update({source: [reverse_edge]})
        else:
            self.agjacent_vertices[target].append(reverse_edge)
        self.edge_flow.update({edge: 0})
        self.edge_flow.update({reverse_edge: 0})

    def find_path(self, source: str, target: str, path: []):
        """Нахождение f дополняющей цепи"""
        if source == target:
            return path
        for edge in self.get_incident_edges(source):
            delta = edge.capacity - self.edge_flow[edge]
            if delta > 0 and not (edge, delta) in path:
                result = self.find_path(edge.target, target, path + [(edge, delta)])
                if result is not None:
                    return result

    def max_flow(self, source: str, target: str):
        """Нахождение максимального потока"""
        current_path = self.find_path(source, target, [])
        while current_path is not None:
            flow = min(delta for edge, delta in current_path)
            for edge, delta in current_path:
                self.edge_flow[edge] += flow
                self.edge_flow[edge.reverse_edge] -= flow
            current_path = self.find_path(source, target, [])

    def get_matching(self):
        """Получить паросочетание после нахождения максимального потока"""
        result = []
        for key in self.edge_flow.keys():
            if key.source == 's' or key.target == 's' or key.source == 't' or key.target == 't':
                continue
            if self.edge_flow[key] == 1:
                result.append((key.source, key.target))
        return result

    def _read_data(self):
        """Прочитать данные из файла"""
        with open('in.txt') as file:
            raw_size_of_shares = file.readline().strip().split(' ')
            size_of_shares = []
            for element in raw_size_of_shares:
                if element != '' and element != ' ':
                    size_of_shares.append(element)
            self.size_shares_x = int(size_of_shares[0])
            self.size_shares_y = int(size_of_shares[1])
            for i in range(self.size_shares_x):
                self.add_vertex(str(i + 1))
            for j in range(self.size_shares_y):
                self.add_vertex(str(self.size_shares_x + j + 1))
            self.array_size = int(file.readline().strip())
            raw_adjacency_array = ''
            string_line = file.readline().strip()
            while string_line:
                raw_adjacency_array += f' {string_line}'
                string_line = file.readline().strip()
            adjacency_array = []
            for element in raw_adjacency_array.strip().split(' '):
                if element != '' and element != ' ':
                    adjacency_array.append(int(element))
            for k in range(self.size_shares_x):
                start_index = adjacency_array[k] - 1
                if start_index == 0:
                    continue
                if k == (self.size_shares_x - 1):
                    end_index = self.array_size
                else:
                    end_index = adjacency_array[k + 1] - 1
                for m in range(start_index, end_index):
                    if adjacency_array[m] == 32767:
                        continue
                    self.add_edge(str(k + 1), str(self.size_shares_x + adjacency_array[m]))
            self._add_drain_and_source()

    def _add_drain_and_source(self):
        """Добавить сток и исток в сеть"""
        self.add_vertex('s')
        self.add_vertex('t')
        for i in range(self.size_shares_x):
            self.add_edge('s', str(i + 1))
        for j in range(self.size_shares_y):
            self.add_edge(str(self.size_shares_x + j + 1), 't')

    def write_result(self, matching: []):
        """Запись результата в файл"""
        result_string = ''
        for index in range(self.size_shares_x):
            flag = True
            for match in matching:
                if int(match[0]) == (index + 1):
                    result_string += f'{(int(match[1]) - self.size_shares_x)} '
                    flag = False
            if flag:
                result_string += '0 '
        with open('out.txt', 'w') as file:
            file.write(result_string.strip())


def main():
    """Точка входа"""
    Resolver()


if __name__ == "__main__":
    main()
