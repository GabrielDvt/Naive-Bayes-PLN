'''
Algoritmo modificado por: Gabriel Augusto De Vito
Gabriel.dvt@hotmail.com

Este algoritmo busca tweets relacionados a uma determinada hashtag
e os insere em um arquivo .CSV

Está sendo utilizado juntamente a outro algoritmo, que é capaz de dizer se um comentário possui caráter positivo, negativo ou neutro

'''
import tweepy
import csv
import pandas as pd
import re
import emoji

#Defina aqui a hashtag que deseja buscar, a quantidade máxima de registros e a data de início
hashtag = "#maisvoce"
quantidade = 400
dataInicial = "2017-06-01"

def remove_emojis(str):
	return ''.join(c for c in str if c not in emoji.UNICODE_EMOJI)

def remove_link(str):
	result = re.sub(r"http\S+", "", str)
	return result

def remove_quebra(str):
	result = re.sub(r"\n", " ", str)
	return result
	
def remove_emoji(string):
    emoji_pattern = re.compile("["
						   u"\U0001f914"
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)
	
# Credenciais do Twitter
consumer_key = '8PdHIYokt8OmUrHiV0sfJe3AB'
consumer_secret = 'gOqFiTLt5qMOQuvP1jmZPg7MbUhCD69xJbDR7IGi5UOiK14Tyt'
access_token = '828402893753634817-JOVZvh7MAK8fxZbZ1nsn2GEwwzxvomA'
access_token_secret = '3HCwhzCpoOw26DgeQg4yuHkQA86KjnK5MdfOFdra2EguO'

#Acesso à API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#Cria o arquivo CSV
csvFile = open('tweets.csv', 'a', newline='')

csvWriter = csv.writer(csvFile)

#Insere os registros dentro do arquivo
for tweet in tweepy.Cursor(api.search,q=hashtag,
                           lang="pt",
                           since_id=dataInicial, tweet_mode="extended").items(quantidade):

	text = remove_link(tweet.full_text)
	text = remove_quebra(text)
	text = remove_emojis(text)
	
	print(text)
	csvWriter.writerow([tweet.created_at, text])

	
