import numpy as np
import pandas as pd
from CrimeData import CrimeData

if __name__ == '__main__':
    cdobj = CrimeData('crimeinfo')

    # create corecrimedata table
    cdobj.create_corecrimedata()

    # loading bulk data into corecrime data table
    for year in range(2001,2024):
        print('Loading ' + str(year) + ' data')

        # find the max number of records we need to pull for a certain year
        num_records = cdobj.get_year_count(year, 'case_number')

        # generate sequence for offset
        sequence = list(range(0, num_records, 100000))

        # page through data and upload
        for ind in sequence:
            df = cdobj.get_bulk_crime_data(year,limit='100000', offset=str(ind)) # fetch data from API
            # upload data to table in chunks
            for chunk in np.array_split(df,10):
                cdobj.insert_corecrimedata(chunk)
        print(str(year) + " completed upload.")

    # Will likely need to increase resources used in MySQL to run the alter table commandas
    # On windows, run `SET GLOBAL innodb_buffer_pool_size=402653184`` to increase innodb_buffer_pool_size before running the below methods.
    # create year-month-day column
    # cdobj.create_y_m_d()
    # cdobj.update_y_m_d()

    # create year-month column
    # cdobj.create_m()
    # cdobj.update_m()

    # close database connection when finished
    cdobj.close()