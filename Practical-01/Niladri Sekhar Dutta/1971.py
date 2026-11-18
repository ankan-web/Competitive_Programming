from typing import List

class Solution:
    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        # Build adjacency list
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = [False] * n
        stack = [source]
        while stack:
            node = stack.pop()
            if node == destination:
                return True
            if visited[node]:
                continue
            visited[node] = True
            for nei in adj[node]:
                if not visited[nei]:
                    stack.append(nei)
        return False