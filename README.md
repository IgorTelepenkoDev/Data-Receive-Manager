# S3 Data Receive Manager
The application connects to the public AWS S3 bucket, extracts specific files with data and loads appropriate results to a local database.
>The task in details is described [here](https://github.com/MacPaw/msi2021-data-engineering).

## Getting Started

#### Python way
```
python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

python3 __main__.py
```

#### Docker way
```
docker build -t data-recieve-manager .

docker run -it --name drm-container data-recieve-manager && \
docker cp drm-container:/app/local_database.sqlite3 . && \
docker cp drm-container:/app/local_processed_files.data . && \
docker rm drm-container

```

The project can be run by `__main__.py` (function _main()_ is called). All the needed imports and references are provided in this part of code. If the local database and storing file do not exist, they will be created automatically (function _start_objects_init()_ is called).

## Project Structure

The project consists of 4 modules: `dataReceiving.py`, `dataParsing.py`, `dbManagement.py`, `__main__.py`. Also, it contains 2 regular objects: an SQLite database (_local_database.sqlite3_) and a file storing a list of processed bucket items (_local_processed_files.data_). 

During the execution there are created temporary files (and appropriately removed after the work is done): _temp_list_of_files.data_ - for downloading the list of data files currently in S3 bucket; _temp_file_processing.data_ - for storing of a downloaded file during its processing.

- Module `__main__.py` contains imports of all other modules and provides general work of the program. Function _received_file_data_processing()_ is called for each data file downloaded from the bucket. This function creates threads of parsing this data and next insertion of the results to the database.  
- Module `dataReceiving.py` provides downloading the content of files from S3 bucket. Also, _find_new_files()_ returns a list of all needed files in the bucket have not been processed yet. It is used to update the local database with new data.
- Module `dataParsing.py` is responsible for finding and processing of the proper parts within the downloaded content. Function _needed_json_data_blocks(searchedType, file)_ parses the JSON file (the downloaded one) and returns a list of data blocks of the required 'type'. Furthermore, other functions provide finding and transformation of values from JSON-style to the order, appropriate for the next insertion into the database.
- Module `dbManagement.py` makes the local database available to work with. Function _create_all_required_tables(connect)_ sets up the SQLite database with 3 tables according to the task ("songs", "movies", "apps"). Also, the module provides possibilities of proper insertion of values into the database tables.

## Brief History of Changes

This repository does not contain the full history of commits. The brief list of changes during the project implementation:

> - Creation of `dataReceiving.py` module and functions _download_s3_file(bucketFileName, localFile)_, _download_s3_list_of_files()_ - for accessing the AWS S3 bucket and downloading files from it.
> - Creation of _find_new_files()_ function - for finding which data files in the bucket should be processed (which have not been before).
> - Creation of `dbManagement.py` module and functions _db_connect()_, _create_all_required_tables(connect)_ - for the local database to be available.
> - Adding functions _insert_in_songs(connect, values)_, _insert_in_movies(connect, values)_, _insert_in_apps(connect, values)_ - for proper insertion of values into the database tables.
> - Creation of `dataParsing.py` module and _needed_json_data_blocks(searchedType, file)_ - for appropriate finding of needed pieces of data.
> - Adding functions _prepared_values_song(blockData)_, _prepared_values_movie(blockData)_, _prepared_values_app(blockData)_ - for receiving the proper order and content of values those can be inserted into the database.
> - Creation of `__main__.py` module that connects functionality of all others.
> - Adding functions _main()_, _received_file_data_processing()_ - for appropriate processing of all the received files from the bucket and next insertion of the data into the database.