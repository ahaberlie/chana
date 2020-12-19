from chana.preproc.convert import get_index, convert_file
import pandas as pd
from multiprocessing import Pool
import os


if __name__ == "__main__":

    syr = 1990
    eyr = syr + 1
    vars = ['AFWA_CAPE', 'AFWA_CAPE_MU',  'AFWA_CIN', 'AFWA_CIN_MU']
    outfolder = 'capecin'

    out_folder = "/glade/scratch/ahaberli/{}/{}-{}".format(outfolder, syr, eyr)    
    folder = "/glade/scratch/ahaberli/{}-{}".format(syr, eyr)
    index = get_index(syr, folder)

    index['time'] = pd.to_datetime(index.time)
    counts = index.groupby(index.time.dt.month).count()
    counts['percent available'] = 100 * counts.filename / counts.time

    print("Report on 15 Minute Availability by Month")
    print(counts)

    index = index[~pd.isnull(index.filename)].copy()
    
    for mid, month in index.groupby(index.time.dt.month):

        outdir = "{}/{:02d}".format(out_folder, mid)
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        for rid, row in month.iterrows():
            fname = row.filename.split("/")[-1]

            outfile = "{}/{}.nc".format(outdir, fname)

            if not os.path.exists(outfile):

                conv = convert_file(row.filename, vars)

                conv.to_netcdf(outfile)
                print(outfile, "written!")
            else:
                print(outfile, "exists!")
