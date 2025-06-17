import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A mapping from a page title to the page ID (integer)
        # For example, self.titles["abc"] returns the ID of the page whose
        # tiitle is "abc".
        self.ids = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        self.ids = {title:id for id,title in self.titles.items()}

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()

    # Homework #1: Find the shortest path.
    # 'start': A title of the start page.
    # 'goal': A title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = self.ids.get(start,-1) # Change from a title to the id <self.ids>
        assert start_id != -1, f"{start} is not found."
        goal_id = self.ids.get(goal,-1)
        assert goal_id != -1, f"{goal} is not found."
        visited = set() # Save the ids of visited pages and scheduled to visit(in queue).
        visited.add(start_id)
        q = collections.deque() # Save is_visiting_id(int), route_taken(list) in queue. 
        q.append((start_id,[start_id]))
        shortest_routes = []
        min_route_length = float('inf')

        if start_id == goal_id:
            return [start_id]
        while q:
            is_visiting_id, route_taken = q.popleft()
            # Don't search so far, if the route will be longer than min_route_length.
            if len(route_taken) >= min_route_length: 
                continue
            for dst_id in self.links[is_visiting_id]:
                if not dst_id in visited:
                    new_route = route_taken + [dst_id]  # add dst_id to route_taken 
                    if dst_id == goal_id: # if reach the goal
                        if len(new_route) == min_route_length: # and if length of route equals min_route_length, append answer.
                            shortest_routes.append([self.titles[id] for id in new_route]) # Change from a id to the title.
                        elif len(new_route) < min_route_length: # and if length of route < min_route_length
                            shortest_routes = [[self.titles[id] for id in new_route]] # reset answer.
                            min_route_length = len(new_route) # update min_route_length.
                    else:
                        q.append((dst_id,new_route))
                        visited.add(dst_id) # if NOT goal_id, add dst_id to visited.
        return shortest_routes

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # Homework #1a
    paths = wikipedia.find_shortest_path("渋谷", "小野妹子")
    if paths:
        for path in paths:
            print(f"the shortest path is: {" -> ".join(path)}")
    else:
        print("the shortest path was not found.")