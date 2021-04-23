import json
import joblib
import discord
from discord.ext import commands
import asyncio

TOKEN = open('TOKEN.txt','r').read()

FLAGGED_WORDS = json.load(open('ABE-Flagged-Words.json','r'))

ABE_BRAIN = joblib.load("ABE-Brain.joblib")

def is_JTexpo():
    def predicate(ctx):
        return 319199396724211722 == ctx.author.id
    return commands.check(predicate)

def in_server(ctx):
    return 433695004645523456 == ctx.guild.id

def ignor_users(ctx):
    users = [159985870458322944, 826454530656043041, 184405311681986560]
    return ctx.author.id in users


BAD_WEIGHT = 4
GOOD_WEIGHT = 1

REPLACE_DICT = {
    '"':' ',
    '\\n': ' ',
    '\\xa0': ' ',
    '\\u2026': ' ',
    '\\': ' ',
    ',': ' ',
    '>': ' ',
    '<': ' ',
    '*': ' ',
    '-': ' ',
    '/': ' ',
    '=': ' ',
    ')': ' ',
    '(': ' ',
    '`': ' ',
    ';': ' ',
    ':': ' ',

    '.': '',
    '?': '',
    '!': '',
    "'": '',
    ":": '',
    '~': '',

    '@':'a',
    '$':'s'
}

def tokenize_text(text):
    """[summary]

    Parameters
    ----------
    text : string
        a sentence to be tokenized

    Returns
    -------
    list of strings
        The tokenized text
    """
    text = text.lower()
    for rep,nrep in  REPLACE_DICT.items():
        text = text.replace(rep,nrep)
    text = text.split()
    return text