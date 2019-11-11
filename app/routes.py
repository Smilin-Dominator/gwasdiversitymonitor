from flask import render_template
from flask import request
from flask import Response
from flask import send_file
from app import app
from app import DataLoader

@app.context_processor
def inject_template_scope():
    injections = dict()

    browser = request.user_agent.browser
    injections.update(browser=browser)

    def cookies_check():
        value = request.cookies.get('cookie_consent')
        return value == 'true'
    injections.update(cookies_check=cookies_check)

    if "GA_KEY" in app.config :
        injections.update(key=app.config["GA_KEY"])

    return injections

@app.route('/')
@app.route('/index')
def index():

    dataLoader = DataLoader.DataLoader()

    ancestries = dataLoader.getAncestriesList()
    parentTerms = dataLoader.getTermsList()
    traits = dataLoader.getTraitsList()
    
    summary = dataLoader.getSummaryStatistics()
    bubbleGraph = dataLoader.getBubbleGraph()
    tsPlot = dataLoader.getTSPlot()
    chloroMap = dataLoader.getChloroMap()
    heatMap = dataLoader.getHeatMap()
    doughnutGraph = dataLoader.getDoughnutGraph()

    return render_template('index.html', title='Home', switches='true', ancestries=ancestries, parentTerms=parentTerms, traits=traits, summary=summary, bubbleGraph=bubbleGraph, tsPlot=tsPlot, chloroMap=chloroMap, heatMap=heatMap, doughnutGraph=doughnutGraph)

@app.route('/privacy-policy')
def privacy():
    return render_template('pages/privacy-policy.html', title='Privacy Policy', alwaysShowCookies=1)

@app.route('/faqs')
def faqs():
    return render_template('pages/faqs.html', title='FAQs')

@app.route('/additional-information')
def additional():
    dataLoader = DataLoader.DataLoader()
    summary = dataLoader.getSummaryStatistics()
    return render_template('pages/additional-information.html', summary=summary)

@app.route("/getCSV/<filename>")
def getCSV(filename):

    if filename == "heatmap" or filename == "timeseries" or filename == "gwasdiversitymonitor_download":
        return send_file('data/todownload/'+filename+'.zip')

    with open('app/data/toplot/'+filename+'.csv') as fp:
        csv = fp.read()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename="+filename+".csv"})