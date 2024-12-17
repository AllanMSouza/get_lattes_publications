import bs4
import xml.etree.ElementTree as ET
import sys
import os
from optparse import OptionParser

def get_conference_papers(filename, until_year=2019):
    soup       = bs4.BeautifulSoup(open(f'data/{filename}.xml'), 'lxml')
    production = soup.find('producao-bibliografica')
    papers     = []
    for paper in production.find_all('trabalho-em-eventos'):
        # print(paper)
        basic_data    = paper.find('dados-basicos-do-trabalho')
        title         = basic_data.get('titulo-do-trabalho')
        year          = basic_data.get('ano-do-trabalho')
        year          = 2024  if year == 'onic' else int(year)
        doi           = basic_data.get('doi')
        
        if year < until_year: continue
        
        detailed_data = paper.find('detalhamento-do-trabalho')
        editor        = detailed_data.get('nome-da-editora')
        conference    = detailed_data.get('nome-do-evento')
        
        authors       = []
        for author in paper.find_all('autores'):
            authors.append(author.get('nome-completo-do-autor')) 
            
        _paper                = {}
        _paper['autores']     = authors
        _paper['titulo']      = title
        _paper['ano']         = year
        _paper['doi']         = doi
        _paper['editora']     = editor
        _paper['conferencia'] = conference
        
        papers.append(_paper)
    
    return papers

def get_journal_papers(filename, until_year):
    
    soup    = bs4.BeautifulSoup(open(f'data/{filename}.xml'), 'lxml')
    production = soup.find('producao-bibliografica')
    papers     = []
    paper      = production.find('artigos-publicados') 

    for paper in paper.find_all('artigo-publicado'):

        basic_data    = paper.find('dados-basicos-do-artigo')
        title         = basic_data.get('titulo-do-artigo')
        year          = basic_data.get('ano-do-artigo')
        year          = int(year) if year != 'onic' else 2024
        doi           = basic_data.get('doi')
        
        if year < until_year: continue
        
        detailed_data = paper.find('detalhamento-do-artigo')
        journal       = detailed_data.get('titulo-do-periodico-ou-revista')
        
        authors     = []
        
        for author in paper.findAll('autores'):
            authors.append(author.get('nome-completo-do-autor'))
            
        _paper                = {}
        _paper['autores']     = authors
        _paper['titulo']      = title
        _paper['ano']         = year
        _paper['doi']         = doi
        _paper['journal']     = journal
        
        papers.append(_paper)

    return papers

def print_papers(papers):
    for paper in papers:
        
        authors  = paper['autores']     
        title    = paper['titulo']     
        year     = paper['ano']        
        doi      = paper['doi']        
        editor   = paper['editora'] if 'editora' in paper.keys() else ''   
        conf_rev = paper['conferencia'] if 'journal' not in paper.keys() else paper['journal']
        
        text     = ""
        for author in authors:
            text += f"{author}, " 
        text += f"""{title}. {conf_rev}. {editor}. {year}. DOI: {doi} \n"""
        print(text)
        
def main():

    parser = OptionParser()
    
    parser.add_option("", "--cpf",    dest="cpf", default=0)
    parser.add_option("", "--from",   dest="year", default=0)
    
    (opt, args) = parser.parse_args()

    os.system(f'cv-lattes-to-xml {opt.cpf} > data/{opt.cpf}.xml')
    
    conference_papers = get_conference_papers(opt.cpf, int(opt.year))
    journal_papers    = get_journal_papers(opt.cpf, int(opt.year))
    
    print('\n\n')
    print('*'*37)
    print('*'*10 + ' Conference Papers ' + '*'*10)
    print('*'*37)
    print('\n\n')
    print_papers(conference_papers)
    
    print('\n\n')
    print('*'*37)
    print('*'*10 + ' Journal Papers ' + '*'*10)
    print('*'*37)
    print('\n\n')
    print_papers(journal_papers)
    
main()