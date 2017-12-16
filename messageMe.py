import praw
import time
import os
import re
import threading

regex = (r"(im|i'm|me|i have|am|having|feeling|feel|feels|have|we|us)\s.{0,17}(insecure|insecurity|depressed|depression|self harm| self-harm|empty|dead|suicidal|unhappy|despondent|troubled|angry|remorseful|destructive|sad|bitter|dismal|heartbroken|melancholy|mournful|pessimistic|somber|sorrowful|wistful|bereaved|blue|cheerless|dejected|despairing|despondent|disconsolate|distressed|doleful|down|down in dumps|down in mouth|downcast|for lorn|gloomy|glum|grief-stricken|grieved|heartsick|heavy hearted|hurting|in doldrums|in grief|in the dumps|languishing|low|low-spirited|lugubrious|morbid|morose|out of sorts|pensive|troubled|weeping|woebegone\n"
	r")")
if re.search(regex,"Hey everyone! I like cookies and coke and im feeling sad :(",re.IGNORECASE):
	print("Test 1: Passed")
if re.search(regex,"Hey everyone! I like cookies sad and coke and im feeling super happy sad :(",re.IGNORECASE):
	print("Test 2: Failed")
else:
	print ("Test 2: Passed")
if re.search(regex,"I had two mental breakdowns :D ",re.IGNORECASE):
	print("Test 3: Failed")
else:
	print ("Test 4: Passed")
if re.search(regex,"I'm sorry to hear that :( ",re.IGNORECASE):
	print("Test 4: Failed")
else:
	print ("Test 4: Passed")


def saveId( file,  id):
	with open(file, "a") as f:
			f.write(id + "\n")
			
#----------------------The bot main function-----------------------------------
def replyToThreads():
	comments = subreddit.stream.comments()
	for comment in comments:
		body = comment.body
		author = comment.author
		matches = re.finditer(regex, body, re.IGNORECASE)
		if re.search(regex,body,re.IGNORECASE):
			thread = comment.submission
			if thread.id not in posts_replied_to:
				message = ("Hey u/{0}! I'm a bot and not capable of reading. "
				"But if you want, "
				"you can always message me about anything! "
				"Most people find that typing out a problem or "
				"a feeling makes it easier to handle, try it! ").format(author)
				try:
					comment.reply(message)
					print("Bot replying to u/{0} in submission: ".format(author), thread.title)
					print("Post was: ", body)
					posts_replied_to.append(thread.id)
					saveId("posts_replied_to.txt", thread.id)
				except praw.exceptions.APIException as error:
					print("Error: Couldn't reply to u/{0}, \n post was: {1} \n error message was: {2}".format(author,body, error.message))
				#print(message)
#similair to above, duplicated code!
def replyToPrivateMessages():
	messages = praw.models.util.stream_generator(bot.inbox.messages)
	for message in messages:
		body = message.body
		author = message.author
		if message.id not in messages_replied_to:
			response = ("Your problems suddenly feel smaller! Or perhaps the same. Something feels different though, of that you are sure. Quite sure atleast... \n\n <3 \n\n *~beep boop~*")
			try:
				message.reply(response)
				print("Bot replying to u/{0} in private message: ".format(author))
				print("Post was: ", body)
				messages_replied_to.append(message.id)
				saveId("messages_replied_to.txt", message.id)
			except praw.exceptions.APIException as error:
				print("Error: Couldn't reply to u/{0}, \n private message was: {1} \n error message was: {2}".format(author,body, error.message))
			#print(message)

bot = praw.Reddit('bot1')
subreddit = bot.subreddit('testingground4bots') #+meirl+2meirl4meirl
print(bot.user.me())

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
	   posts_replied_to = f.read()
	   posts_replied_to = posts_replied_to.split("\n")
	   posts_replied_to = list(filter(None, posts_replied_to))
#duplicated code!
if not os.path.isfile("messages_replied_to.txt"):
	messages_replied_to = []
else:
	with open("messages_replied_to.txt", "r") as f:
	   messages_replied_to = f.read()
	   messages_replied_to = messages_replied_to.split("\n")
	   messages_replied_to = list(filter(None, messages_replied_to))

threadComment = threading.Thread(target=replyToThreads)
threadComment.start()

threadMessageReply = threading.Thread(target=replyToPrivateMessages)
threadMessageReply.start()
