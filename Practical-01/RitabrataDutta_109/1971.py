from collections import deque, defaultdict


class Solution:
    def validPath(
        self, n: int, edges: list[list[int]], source: int, destination: int
    ) -> bool:

        if source == destination:
            return True

        graph = defaultdict(list)

        for u, v in edges:
            graph[v].append(u)
            graph[u].append(v)

        visited = {source}
        queue = deque([source])

        while queue:
            curr_node = queue.popleft()

            if curr_node == destination:
                return True

            for neighbour in graph[curr_node]:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return False
