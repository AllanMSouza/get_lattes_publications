from flask import Flask, request, render_template, redirect, url_for
import os
import bs4

app = Flask(__name__)

# Funções do seu código original
def get_conference_papers(filename, until_year=2019):
    soup = bs4.BeautifulSoup(open(f'data/{filename}.xml'), 'lxml')
    production = soup.find('producao-bibliografica')
    papers = []
    for paper in production.find_all('trabalho-em-eventos'):
        basic_data = paper.find('dados-basicos-do-trabalho')
        title = basic_data.get('titulo-do-trabalho')
        year = int(basic_data.get('ano-do-trabalho'))
        doi = basic_data.get('doi')
        
        if year < until_year:
            continue
        
        detailed_data = paper.find('detalhamento-do-trabalho')
        editor = detailed_data.get('nome-da-editora')
        conference = detailed_data.get('nome-do-evento')
        
        authors = []
        for author in paper.find_all('autores'):
            authors.append(author.get('nome-completo-do-autor')) 
            
        papers.append({
            'autores': authors,
            'titulo': title,
            'ano': year,
            'doi': doi,
            'editora': editor,
            'conferencia': conference
        })
    return papers

def format_papers(papers):
    output = ""
    for paper in papers:
        authors = ", ".join(paper['autores'])
        title = paper['titulo']
        year = paper['ano']
        doi = paper['doi']
        editor = paper.get('editora', '')
        conf_rev = paper.get('conferencia', '')
        
        output += f"{authors}. {title}. {conf_rev}. {editor}. {year}. DOI: {doi} <br>"
    return output

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cpf = request.form.get("cpf")
        if cpf:
            # Executa o comando externo para gerar XML
            os.system(f'cv-lattes-to-xml {cpf} > data/{cpf}.xml')
            
            # Processa o arquivo XML e coleta dados
            papers = get_conference_papers(cpf, until_year=2019)
            output = format_papers(papers)
            
            # Redireciona para a página de resultado
            return render_template("result.html", output=output)
    return render_template("index.html")

@app.route("/result")
def result():
    return render_template("result.html", output="Nenhum dado disponível.")

if __name__ == "__main__":
    app.run(debug=True)
