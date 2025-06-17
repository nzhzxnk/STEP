import sys
import collections
from collections import deque
import matplotlib.pyplot as plt

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):
        # A mapping from a page ID (integer) to the page title.
        self.titles = {}
        # A mapping from a page title to the page ID (integer)
        self.ids = {}
        # A set of page links.
        self.dst_links = {} # src_id -> dst_id
        self.src_links = {} # dst_id -> src_id

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.dst_links[id] = []
                self.src_links[id] = []
        print("Finished reading %s" % pages_file)

        self.ids = {title:id for id,title in self.titles.items()}

        # Read the links file into self.dst_links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.dst_links[src].append(dst)
                self.src_links[dst].append(src)
        print("Finished reading %s" % links_file)
        print()

# Homework #2: Calculate the page ranks and print the most popular pages.
    def calculate_pagerank(self):
        old_pagerank = {} # Initialize old_pagerank all 1.0.
        for id in self.titles.keys():
            old_pagerank[id] = 1.0
        converging = False
        num_pages = len(self.titles)

        while not converging:
            new_pagerank = {} # initialize new_pagerank all 0.0.
            for id in self.titles.keys():
                new_pagerank[id] = 0.0
            # print(new_pagerank) #debag
            random_jump_value = 0.0 # ramdomly distributed pagerank is initialized 0.
            torerance = 0 
            for src_id,dst_ids in self.dst_links.items():
                if not dst_ids: # if source has no outgoing links, its 100% pagerank is distributed into random_jump_value.
                    random_jump_value += old_pagerank[src_id]
                else:
                    for dst_id in dst_ids: # if source has any outgoing links
                        # its 85% pagerank is distributed into each desitination equally.
                        new_pagerank[dst_id] += old_pagerank[src_id]*0.85/len(dst_ids) 
                    random_jump_value += old_pagerank[src_id]*0.15 # its 15% pagerank is distributed into random_jump_value.
            random_jump_per_page = random_jump_value/num_pages
            for id in self.titles.keys():
                new_pagerank[id] += random_jump_per_page # complete calculating new pagerank.
                torerance += (new_pagerank[id]-old_pagerank[id])**2 # the torerance between before and after pagerank calculating.
            assert abs(sum(new_pagerank.values()) - num_pages) < 1e-4, f"the pagerank system is wrong.{sum(new_pagerank.values()) - num_pages} "
            if torerance < 0.01: # difine the process as converged when the torerance is within 0.01.
                converging = True
            else:
                old_pagerank = new_pagerank
        return new_pagerank

    def calculate_connection(self):
        connection = {}
        for id in self.titles.keys():
            connection[id] = len(self.src_links[id]) + len(self.dst_links[id])
        return connection

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    pagerank = wikipedia.calculate_pagerank()
    connection = wikipedia.calculate_connection()

    x_values = [] # the num of connection
    y_values = [] # pagerank
    data_count = 0

    for page_id, pr_value in pagerank.items():
        if page_id in connection:
            x = connection[page_id]
            y = pr_value
            if x < 100000 and y < 1500:
                data_count += 1
                x_values.append(x)
                y_values.append(y)

    plt.figure(figsize=(10, 6)) # graph size
    plt.scatter(x_values, y_values, alpha=0.7, color='red') 
    plt.xlabel("Number of Connections")
    plt.ylabel("PageRank")
    plt.title("PageRank vs. Number of Connections")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig("pagerank_vs_connections.png")
    plt.text(0.95, 0.95, f"Data Count: {data_count}",
         horizontalalignment='right',
         verticalalignment='top',
         transform=plt.gca().transAxes,
         fontsize=12,
         bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.5'))

    # x_values = [] # the num of connection
    # y_values = [] # pagerank
    # data_count  = 0

    # for page_id, pr_value in pagerank.items():
    #     if page_id in connection:
    #         data_count += 1
    #         x_values.append(connection[page_id])
    #         y_values.append(pr_value)

    # plt.figure(figsize=(10, 6)) # graph size
    # plt.scatter(x_values, y_values, alpha=0.7, color='red') 
    # plt.xlabel("Number of Connections")
    # plt.ylabel("PageRank")
    # plt.title("PageRank vs. Number of Connections")
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.savefig("pagerank_vs_connections.png")
    # plt.text(0.95, 0.95, f"Data Count: {data_count}",
    #      horizontalalignment='right',
    #      verticalalignment='top',
    #      transform=plt.gca().transAxes,
    #      fontsize=12,
    #      bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round,pad=0.5'))