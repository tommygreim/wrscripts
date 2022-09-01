import sys
import os
from subprocess import Popen, PIPE
import re
import wikipediaapi
from termcolor import colored
import textwrap

def less(data):
    process = Popen(["less"], stdin=PIPE)

    try:
        process.stdin.write(str.encode(data))
        process.communicate()
    except IOError as e:
        pass

def textwr(outStr, offset = ""):
	maxWidth = 80
	outLines = []
	if len(outStr) > maxWidth:
		# print("===")
		outStr = re.sub(r"\.(?![\s\d])", ".\n",outStr, re.M)
		# print(outStr)
		# print("===")
		paras = outStr.splitlines()
		for p in paras:
			for l in textwrap.wrap(p, width=80, replace_whitespace=True, drop_whitespace=True):outLines.append(offset + l)
	else:
		outLines.append(outStr)
	return outLines

def full_article(page):
	outLines = []
	outLines.append("\n")
	outLines.append(page.title)
	outLines.append('================================================================================')
	outLines = outLines + textwr(page.summary)

	for s in page.sections:
		outLines = outLines + section_lines(s, 1)
		# outLines.append("\n")
		# outLines.append(s.title)
		# outLines.append('--------------------------------------------------------------------------------')
		# outLines = outLines + textwr(s.text)
		# for s2 in s.sections:
		# 	outLines.append("\n")
		# 	outLines.append("[" + s2.title + "]")
		# 	outLines = outLines + textwr(s2.text)
	less("\n".join(outLines))

seps = ['================================================================================',
			'--------------------------------------------------------------------------------',
			'', '']

def section_lines(section, sepNum):
	outLines = []
	# offset = ''
	# sepCount = sepNum
	# while sepCount > 2:
	# 	offset += '\t'
	# 	sepCount -= 1
	if sepNum > 1:
		outLines.append("=" + section.title + "=")
	else:
		outLines.append(section.title)
		outLines.append(seps[sepNum])
	outLines = outLines + textwr(section.text)
	outLines.append('\n')
	for s in section.sections:
		outLines = outLines + section_lines(s, sepNum+1)
	return outLines

wiki_html = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.HTML
)

def article_section(page, sectionIdx):
	section = page.sections[sectionIdx]
	outLines = []
	outLines.append("Full Article: " + page.title)
	# outLines.append("\n\n")
	# outLines.append(section.title)
	# outLines.append(seps[0])
	# outLines = outLines + textwr(section.text)
	# htmlPage = wiki_html.page(page.title)
	# htmlSection = htmlPage.sections[sectionIdx]
	# outLines.append('\n===\n' + htmlSection.text)
	outLines = outLines + section_lines(section, 0)
	less("\n".join(outLines))


def display_options(article):
	page = wiki_wiki.page(article)
	print('\n')
	print("Current Article: " + page.title)
	print("  1) Full Article")
	print("  2) Table of Contents")
	print("  3) Linked Pages")
	print("  4) New Page")
	option = input("Select an option: ")
	if option == "1":
		full_article(page)
	elif option == "2":
		print("Table of Contents: ")
		if len(page.sections) > 0:
			for i in range(len(page.sections)):
				print("  " + str(i+1) + ") " + page.sections[i].title)
			option = input("Select an section: ")
			article_section(page, int(option)-1)
		else:
			input("  No sections found. Return?")
			# option = input("Return?")
	elif option == "3":
		links = sorted(page.links.keys())
		print("Linked Pages")
		if len(links) > 0:
			for i in range(len(links)):
				print("  " + str(i+1) + ") " + links[i])
			option = input("Select an article: ")
			return links[int(option)-1]
		else:
			input("  No links found. Return?")
	elif option == "4":
		# print('\n')
		option = input("Search: ")
		return option
	else:
		return None
	return article

wiki_wiki = wikipediaapi.Wikipedia('en')

selection = sys.argv[1];
while(selection != None):
	selection = display_options(selection)



