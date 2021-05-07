import os

import boto3
from botocore import UNSIGNED
from botocore.config import Config


BUCKET_NAME = 'data-engineering-interns.macpaw.io'
BUCKET_FILES_LIST = 'files_list.data'
LOCAL_TEMP_FILES_LIST = 'temp_list_of_files.data'

LOCAL_CHECKED_FILES_LIST = 'local_processed_files.data'
LOCAL_TEMP_FILE_FOR_PROCESSING = 'temp_file_processing.data'


def download_s3_file(bucketFileName, localFile, bucket=BUCKET_NAME):
    s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
    create_local_file(localFile)    # if it doesn't exist, it'll be created
    s3.Bucket(bucket).download_file(bucketFileName, localFile)


def download_s3_list_of_files():
    download_s3_file(BUCKET_FILES_LIST, LOCAL_TEMP_FILES_LIST)


def find_new_files():
    resNewFiles = []    # result list of files (names) those haven't been processed

    newListF = open(LOCAL_TEMP_FILES_LIST, 'r')   # file with updated (downloaded from the bucket) list of files
    newListOfFiles = newListF.readlines()
    newListF.close()

    localListF = open(LOCAL_CHECKED_FILES_LIST, 'r+')
    listCheckedFiles = localListF.readlines()

    for bucketFile in newListOfFiles:
        if bucketFile not in listCheckedFiles:
            localListF.write(bucketFile)
            resNewFiles.append(bucketFile.rstrip('\n'))    # the lines contain '\n' in the end after being read

    localListF.close()
    return resNewFiles


def create_local_file(fileName):
    f = open(fileName, "w+")
    f.close()


def delete_local_file(fileName):
    os.remove(fileName)
