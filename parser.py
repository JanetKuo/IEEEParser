__author__ = 'Janet'

import re
import os
import urllib
import csv

url_article_temp = 'http://ieeexplore.ieee.org/xpl/articleDetails.jsp?arnumber=%s'
url_authors_temp = 'http://ieeexplore.ieee.org/xpl/abstractAuthors.jsp?arnumber=%s'
url_reference_temp = 'http://ieeexplore.ieee.org/xpl/abstractReferences.jsp?arnumber=%s'
url_citedby_temp = 'http://ieeexplore.ieee.org/xpl/abstractCitations.jsp?arnumber=%s'
url_keywords_temp = 'http://ieeexplore.ieee.org/xpl/abstractKeywords.jsp?arnumber=%s'
url_metrics_temp = 'http://ieeexplore.ieee.org/xpl/abstractMetrics.jsp?arnumber=%s'
url_similar_temp = 'http://ieeexplore.ieee.org/xpl/abstractSimilar.jsp?arnumber=%s'

def extract_ids(filename):
    ids = []
    f = open(filename, 'rU')
    content = f.read()
    id_match = re.findall(r'@ARTICLE{(\d+),', content)
    for id in id_match:
        ids.append(id)
    return ids

def get_article(id):
    url_article = url_article_temp % id
    article = urllib.urlopen(url_article)
    content = article.read()
    return content

def get_pdf_url(id):
    url_article = url_article_temp % id
    content = get_article(id)
    pdf_match = re.search(r'http://(\S+).pdf', content)
    if pdf_match:
        url_paper = pdf_match.group(0)
        #download_papers(id, url_paper)
        return url_paper
    else:
        print 'Warning! PDF not found in', url_article
        return 'PDF not found'

def download_papers(id, paper_url, dest_dir='PDF'):
    if not os.path.exists(dest_dir):
      os.makedirs(dest_dir)
    paper_path = os.path.join(dest_dir, id+'.pdf')
    print 'Retrieving', paper_url
    urllib.urlretrieve(paper_url, paper_path)

def csv_writer_field(field_list=['ID', 'PDF'], csv_path='result.csv'):
    with open(csv_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(field_list)

def csv_writer(data_list, csv_path='result.csv'):
    with open(csv_path, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data_list)

def main():
    filename = 'tvcg2011bib.txt'
    ids = extract_ids(filename)
    csv_writer_field()
    for id in ids:
        csv_writer([id, get_pdf_url(id)])

if __name__ == '__main__':
    main()