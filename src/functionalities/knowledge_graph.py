import requests
from rdflib.namespace import RDF, RDFS, XSD, Namespace
from rdflib import Graph, Literal, URIRef
import os
import re
import urllib

class Publication:
    def __init__(self, title, doi, cites, num_pages, publication_date, language, pages, published_in, main_subject, instance_of, author, topic, similar_papers):
        self._title = title
        self._doi = doi
        self._cites = cites
        self._num_pages = num_pages
        self._publication_date = publication_date
        self._language = language
        self._pages = pages
        self._published_in = published_in
        self._main_subject = main_subject
        self._instance_of = instance_of
        self._author = author
        self._topic = topic
        self._similar_papers = similar_papers

    # Getters
    def get_title(self):
        return self._title

    def get_doi(self):
        return self._doi

    def get_cites(self):
        return self._cites

    def get_num_pages(self):
        return self._num_pages

    def get_publication_date(self):
        return self._publication_date

    def get_language(self):
        return self._language

    def get_pages(self):
        return self._pages

    def get_published_in(self):
        return self._published_in

    def get_main_subject(self):
        return self._main_subject

    def get_instance_of(self):
        return self._instance_of

    def get_author(self):
        return self._author
    
    def get_topic(self):
        return self._topic

    def get_similar_papers(self):
        return self._similar_papers

    #Other fucntions
    def display_info(self):
        print("Title:", self._title)
        print("DOI:", self._doi)
        print("Cites:", self._cites)
        print("Number of Pages:", self._num_pages)
        print("Publication Date:", self._publication_date)
        print("Language:", self._language)
        print("Pages:", self._pages)
        print("Published In:", self._published_in)
        print("Main Subject:", self._main_subject)
        print("Instance Of:", self._instance_of)
        print("Author:", self._author)
        print("Topic:", self._topic)
        print("Similar Papers:", self._similar_papers)
        print("\n")

list_papers = []
author_by_doi = {}
topic_by_doi = {}
topic_and_prob_by_title = {}
topic_and_prob_by_doi = {}
possible_topics = []
similarities_by_doi = {}
similarities_by_title = []

wikidata_res = 'papers/wikidata/results.csv'
openalex_res = 'papers/openalex/results.csv'
prob_res = 'papers/probabilities/'
doi_res = 'papers/doi/'
topic_res = 'papers/topics/'
similarities_res = 'papers/similarities/'
aux_list = []

# read authors
with open(openalex_res, 'r') as f:
    f.readline()
    for line in f:
        line_split = line.split(',')
        doi = line_split[0]
        author = line_split[1]
        author_institution = line_split[2]

        if doi in author_by_doi and author not in author_by_doi[doi]:
            author_by_doi[doi].append(author)
        else:
            author_by_doi[doi] = [author]

# read topics
with open(topic_res + 'topics.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        if line == '\n':
            continue
        line = line.replace('\n', '')
        topic = line.split(":")[1].strip().replace(",", "_").replace(" ", "")
        topic = str(topic)
        possible_topics.append(topic)

# read topics and probabilities
for filename in os.listdir(prob_res):
    with open(prob_res + filename, 'r') as f:
        line = f.read()

        topic_start = line.find("Topic: [") + len("Topic: [")
        topic_end = line.find("]", topic_start)
        prob_start = line.find("Probability: ") + len("Probability: ")
        prob_end = line.find("\n", prob_start)

        topic = line[topic_start:topic_end]
        probabilidad = float(line[prob_start:prob_end])
        topic_and_prob_by_title[filename] = (topic, probabilidad)

with open(similarities_res + 'similarities.txt', 'r') as f:
    lines = f.readlines()

    for line in lines:
        line = line.replace('\n', '')
        line_split = line.split(";")
        title1 = line_split[0]
        title2 = line_split[1]
        similarity = float(line_split[2])

        similarities_by_title.append((title1, title2, similarity))
        
        if title1 not in aux_list:
            aux_list.append(title1)
        if title2 not in aux_list:
            aux_list.append(title2)    
    
for filename in os.listdir(doi_res):
    with open(doi_res + filename, 'r') as f:
        if filename in topic_and_prob_by_title:
            doi = f.read()
            topic = topic_and_prob_by_title[filename][0]
            probabilidad = topic_and_prob_by_title[filename][1]
            topic_and_prob_by_doi[doi] = (topic, probabilidad)
        
        if filename in aux_list:
            for title1, title2, similarity in similarities_by_title:
                doi1 = open(doi_res + title1, 'r').read()
                doi2 = open(doi_res + title2, 'r').read()
                if title1 == filename:
                    if similarities_by_doi.get(doi1) is None:
                        similarities_by_doi[doi1] = [doi2]
                    else:
                        similarities_by_doi[doi1].append(doi2)
                elif title2 == filename:
                    if similarities_by_doi.get(doi2) is None:
                        similarities_by_doi[doi2] = [doi1]
                    else:
                        similarities_by_doi[doi2].append(doi1)
            

# read csv
with open(wikidata_res, 'r') as f:
    # skip header
    f.readline()
    for line in f:
        if line.startswith('"'):
            title = line.split('"')[1]
            doi = line.split('"')[2]
            doi = doi.split(',')[1]
            # change content between double quotes
            line = line.replace(title, "")
        else:    
            line_split = line.split(',')
            # save all atributes in paper object
            title = line_split[0]
            doi = line_split[1]
            
        line_split = line.split(',')

        if doi in author_by_doi:
            authors = author_by_doi[doi]
            authors = str(authors).replace(',', ' -').replace('[', '').replace(']', '')
        else:
            authors = ""

        if doi in topic_and_prob_by_doi:
            topic, probabilidad = topic_and_prob_by_doi[doi]
        else:
            topic = ""

        similar_papers = []
        
        if doi in similarities_by_doi:
            similar_papers = similarities_by_doi[doi]
        
        similar_papers = str(similar_papers).replace(',', ' -').replace('[', '').replace(']', '')
        
        line_split[9] = line_split[9].replace('\n', '')
        title = title.replace(" ", "_")
        title = title.replace(",", "")
        cleaned_topics = topic.replace("'", "").replace(",", "").replace(" ", "_")

        paper = Publication(title, doi, line_split[2], line_split[3], line_split[4], line_split[5], line_split[6], line_split[7], line_split[8], line_split[9], authors, cleaned_topics, similar_papers)
        list_papers.append(paper)



g = Graph()

for paper in list_papers:
    paper_uri = URIRef("http://example.org/" + paper.get_doi())
    g.add((paper_uri, RDF.type, URIRef("http://schema.org/paper")))
    g.add((paper_uri, URIRef("http://schema.org/title"), Literal(paper.get_title())))
    g.add((paper_uri, URIRef("http://schema.org/doi"), Literal(paper.get_doi())))
    g.add((paper_uri, URIRef("http://schema.org/cites"), Literal(paper.get_cites())))
    g.add((paper_uri, URIRef("http://schema.org/numPages"), Literal(paper.get_num_pages())))
    g.add((paper_uri, URIRef("http://schema.org/publicationDate"), Literal(paper.get_publication_date())))
    g.add((paper_uri, URIRef("http://schema.org/inLanguage"), Literal(paper.get_language())))
    g.add((paper_uri, URIRef("http://schema.org/pages"), Literal(paper.get_pages())))
    g.add((paper_uri, URIRef("http://schema.org/publishedIn"), Literal(paper.get_published_in())))
    g.add((paper_uri, URIRef("http://schema.org/mainSubject"), Literal(paper.get_main_subject())))
    g.add((paper_uri, URIRef("http://schema.org/author"), Literal(paper.get_author())))
    g.add((paper_uri, URIRef("http://schema.org/topic"), Literal(paper.get_topic())))
    g.add((paper_uri, URIRef("http://schema.org/similarPapers"), Literal(paper.get_similar_papers())))

for topic in possible_topics:
    topic_uri = URIRef("http://example.org/"+topic)
    g.add((topic_uri, RDF.type, URIRef("http://schema.org/topic")))
    g.add((topic_uri, URIRef("http://schema.org/name"), Literal(topic)))

g.serialize(destination='papers.xml', format='xml')