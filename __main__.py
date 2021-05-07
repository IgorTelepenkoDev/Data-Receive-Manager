import os

from multiprocessing.pool import ThreadPool
from threading import Thread

import dataReceiving
import dataParsing
import dbManagement


def start_objects_init(db=dbManagement.DEFAULT_DB_PATH, processedFilesFile=dataReceiving.LOCAL_CHECKED_FILES_LIST):
    if not os.path.exists(db):
        dbConn = dbManagement.db_connect(db,)
        dbManagement.create_all_required_tables(dbConn)
        dbConn.close()
    if not os.path.exists(processedFilesFile):
        dataReceiving.create_local_file(processedFilesFile)


def received_file_data_processing():
    print(" processing of a new file... ")

    neededTypes = ['song', 'movie', 'app']
    valuesDict = {'song': None, 'movie': None, 'app': None}   # created for clearer separation of values

    # making a pool of threads to get values for 'song', 'movie' and 'app' types, prepared to be inserted into the DB:
    poolData = ThreadPool(processes=len(neededTypes))
    allValuesNeededTypes = poolData.map(dataParsing.get_all_values_certain_type_from_processed_file, neededTypes)
    poolData.close()
    poolData.join()
    # forming the dictionary with appropriately received values:
    valuesDict['song'] = allValuesNeededTypes[0]
    valuesDict['movie'] = allValuesNeededTypes[1]
    valuesDict['app'] = allValuesNeededTypes[2]

    # making threads of insertion the previously received values into the DB tables:
    dbInsThreads = []
    for typeVal in valuesDict:
        dbInsThreads.append(Thread(target=dbManagement.insert_many_one_type_values,
                                   args=(valuesDict[typeVal], typeVal)))

    for thread in dbInsThreads:
        thread.start()
    for thread in dbInsThreads:
        thread.join()

    print(" processing of the file is finished. ")


def main():
    start_objects_init()   # creation of local database and storing file if they do not exist yet
    dataReceiving.download_s3_list_of_files()

    for newF in dataReceiving.find_new_files():   # processing of all files those have not been processed before
        print(" new file to be processed: ", newF)
        # downloading the data file from the bucket for the next processing
        dataReceiving.download_s3_file(newF, dataReceiving.LOCAL_TEMP_FILE_FOR_PROCESSING)
        received_file_data_processing()
        dataReceiving.delete_local_file(dataReceiving.LOCAL_TEMP_FILE_FOR_PROCESSING)

    dataReceiving.delete_local_file(dataReceiving.LOCAL_TEMP_FILES_LIST)
    print(" The task is done! ")


if __name__ == "__main__":
    main()
