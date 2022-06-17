import jobserve_scraper as js
import pandas as pd
import os

outname = 'jobs_dataset.csv'

outdir = './dir'
if not os.path.exists(outdir):
    os.mkdir(outdir)

fullname = os.path.join(outdir, outname)    

path="C:/Users/aksc7/Documents/Data Science/data_jobs_analysis"

df = js.get_jobs('data')
df.to_csv('jobs_dataset.csv')