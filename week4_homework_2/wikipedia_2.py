import sys
import collections
from collections import deque

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

# Homework #2: Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
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
            for src_id,dst_ids in self.links.items():
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
        print("the most important 10 pages are: ")
        # sort by pagerank in descending order and extract the top 10
        top10_pagerank_ids = sorted(new_pagerank.items(), key=lambda item:item[1], reverse= True)[:10]
        for id,value in top10_pagerank_ids:
            print(self.titles[id]) # change a page id to the page title.


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)
    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_most_popular_pages()

# COMMAND
# python3 /Users/hayashiayano/Desktop/STEP/week4_homework_2/wikipedia_2.py /Users/hayashiayano/Desktop/STEP/week4_homework_2/wikipedia_dataset/pages_large.txt /Users/hayashiayano/Desktop/STEP/week4_homework_2/wikipedia_dataset/links_large.txt
# RESULT
# the most important 10 pages are: 
# 英語
# 日本
# VIAF_(識別子)
# バーチャル国際典拠ファイル
# アメリカ合衆国
# ISBN
# ISNI_(識別子)
# 国際標準名称識別子
# 地理座標系
# SUDOC_(識別子)