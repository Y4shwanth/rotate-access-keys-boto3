# rotate-access-keys-boto3
this repo consists of script written in Python using Boto3 library.

This script is executed periodically(once in a month) using cronjob set in github actions.
Once it is executed it genrates new keys and stores in AWS S3 folder that is specific to particular user(i.e only owner of keys is able to get contents of folder).
Access control for folder specific permissions is out of scope of this project.
