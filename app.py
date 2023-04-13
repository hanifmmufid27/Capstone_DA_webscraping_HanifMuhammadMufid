from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

# #insert the scrapping here
halaman  = 15
title = []
lokasi = []
post_dl = []
perusahaan = []

for i in range(1, halaman + 1):
    print(f'Proses Halaman {i}')
    url_get = requests.get(f"https://www.kalibrr.id/id-ID/job-board/te/data/{i}")
    soup = BeautifulSoup(url_get.content,"html.parser")
    title_0 = soup.find_all('h2', attrs = {'class' : 'k-text-xl k-font-medium'})
    title_1 = BeautifulSoup(str(title_0), 'html.parser')
    for item in title_1.find_all('a', attrs={'class':'k-text-primary-color'}):
        title.append(item.text)
    perusahaan_0 = soup.find_all('span', attrs = {'class' : 'k-inline-flex k-items-center k-mb-1'})
    perusahaan_1 = BeautifulSoup(str(perusahaan_0), 'html.parser')
    for item in perusahaan_1.find_all('a', attrs={'class':'k-text-subdued'}):
        perusahaan.append(item.text)
    for item in soup.find_all('a', attrs={'class':'k-text-subdued k-block'}):
        lokasi.append(item.text)
    for item in soup.find_all('span', attrs={'class':'k-block k-mb-1'}):
        post_dl.append(item.text)
print('DONE')

#change into dataframe
df = pd.DataFrame({"Title Pekerjaan":title,"Lokasi": lokasi, "Post dan Deadline":post_dl, "Perusahaan": perusahaan})

#insert data wrangling here
df = df.replace({'Lokasi': ', Indonesia'}, {'Lokasi' : ''}, regex = True)
df['Lokasi'] = df['Lokasi'].replace(['West Jakarta', 'Kota Jakarta Barat'], 'Jakarta Barat', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['Central Jakarta', 'Central Jakarta City', 'Kota Jakarta Pusat', 'Jakarta Pusat City'],
                                    'Jakarta Pusat', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['North Jakarta'], 'Jakarta Utara', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['East Jakarta'], 'Jakarta Timur', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['South Jakarta', 'South Jakarta City', 'Kota Jakarta Selatan', 'Jakarta Selatan City'],
                                    'Jakarta Selatan', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['South Tangerang'], 'Tangerang Selatan', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['Tangerang Kota'], 'Tangerang', regex = True)

# sekali lagi

df['Lokasi'] = df['Lokasi'].replace(['West Jakarta', 'Kota Jakarta Barat'], 'Jakarta Barat', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['Central Jakarta', 'Central Jakarta City', 'Kota Jakarta Pusat', 'Jakarta Pusat City'],
                                    'Jakarta Pusat', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['North Jakarta'], 'Jakarta Utara', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['East Jakarta'], 'Jakarta Timur', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['South Jakarta', 'South Jakarta City', 'Kota Jakarta Selatan', 'Jakarta Selatan City'],
                                    'Jakarta Selatan', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['South Tangerang'], 'Tangerang Selatan', regex = True)
df['Lokasi'] = df['Lokasi'].replace(['Tangerang Kota'], 'Tangerang', regex = True)

#end of data wranggling 

@app.route("/")
def index():
    card_data = pd.crosstab(
        index=df['Lokasi'],
        columns='Jumlah Pekerjaan'
    ).sort_values(by='Jumlah Pekerjaan', ascending=False).head(5)

    card_data2 = pd.crosstab(
        index = df['Title Pekerjaan'],
        columns = 'Jumlah Pekerjaan'
    ).sort_values(by = 'Jumlah Pekerjaan', ascending = False).head(5)

    card_data3 = df['Perusahaan'].value_counts().head(5)

	# generate plot
    ax = card_data.plot(figsize = (10,6), kind = 'bar', rot = 7)
	# Rendering plot
	# Do not change this
    figfile = BytesIO()
    plt.savefig(figfile, format='png', transparent=True)
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    plot_result = str(figdata_png)[2:-1]

    ax2 = card_data2.plot(figsize = (10,6), kind = 'barh', rot = 7)

    figfile2 = BytesIO()
    plt.savefig(figfile2, format='png', transparent=True)
    figfile2.seek(0)
    figdata_png2 = base64.b64encode(figfile2.getvalue())
    plot_result2 = str(figdata_png2)[2:-1]

	# render to html
    return render_template('index.html',
                           card_data = card_data,
                           plot_result=plot_result,
                           plot_result2=plot_result2,
	    )
if __name__ == "__main__": 
    app.run(debug=True)