import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        print(sys.argv)
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    return
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    pd = dict(zip(corpus.keys(),[0]*len(corpus)))
    N = len(corpus)
    
    if len(corpus[page]) :
        n = len(corpus[page])
        for link in corpus[page] :
            pd[link] = damping_factor/n
        
        for page in corpus.keys():
            pd[page] += (1-damping_factor)/N    

    else :
        for page in corpus.keys():
            pd[page] = 1/N

    return pd

    raise NotImplementedError


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pr = dict(zip(corpus.keys(), [0]*len(corpus)))
    page = random.choice(list(corpus.keys()))
    for _ in range(n):
        pr[page] +=1
        pd = transition_model(corpus,page,damping_factor)
        page = random.choices(list(pd.keys()),pd.values())[0]
    pr = {page : num_samples/n for page,num_samples in pr.items()}
    return pr
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N=len(corpus)
    pd = dict(zip(corpus.keys(),[1/N]*N))
    pd_dx = dict(zip(corpus.keys(),[1/N]*N))

    while any(dx>0.001 for dx in pd_dx.values()):
        pass
    raise NotImplementedError


if __name__ == "__main__":
    main()
