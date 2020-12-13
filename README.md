# Public-NLP

A repository containing various code dealing with language processing, machine learning and Twitter data processing. 

## MapNode.py

Algorithm designed to guess the language of a particular sentence using a model based on word order and word frequency. Sentences are broken down into tokens and inputted into the model where the first word of a sentence will map to the second word, the second word to the third word, etc. 

## data.py

Program designed to process Twitter data and write the processed data into a csv file. Program breaks down each Tweet by the language and the country it was written in. 

## processing.py

Program used in the processing of the Twitter data and the WHO COVID-19 data for the month of October for data science final project. The program reads in data from each of the json files for the month of October and reads in the WHO COVID-19 csv, processes it and writes all of it into a csv file. 

## streaming.py

This program uses the python module Tweepy to access the Twitter API for tweets mentioning COVID-19, Coronavirus or Covid. This program then gets the Tweet ids and writes them to a file. Cutoff is around 1000 as to make sure that no errors occur when running this program multiples scheduled times throughout the day. 

