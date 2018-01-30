#!/usr/bin/python
# -*- coding: utf-8 -*-
import praw
import time
import credentials


# Copied this character from a text message from someone with the bug.
# How it appears in text editors is variable.
theBadStr = "I️"

bot = praw.Reddit(user_agent='UpgradeBot v1.3', client_id=credentials.myClientID, client_secret=credentials.myClientSecret, username=credentials.myUserName, password=credentials.myPassword)

subreddits = bot.subreddit(credentials.mySubredditList)

comments = subreddits.stream.comments()

done = False

while not done:
	try:
		for comment in comments:
			if theBadStr in comment.body:
				print("\n\n********************")
				print(comment.submission.title)
				print("This guy: {0}".format(comment.author))
				print(comment.body)
				print(comment.submission.shortlink)
		
				alreadySuggested = False
				if (comment.parent().author == credentials.myUserName):
					alreadySuggested = True
					print("Already warned above")
				else:
					for reply in comment.replies:
						if reply.author == credentials.myUserName:
							alreadySuggested = True
							print("Already warned")
			
				if (not alreadySuggested):
					print("Issuing warning")
					try:
						comment.reply("Hi! I'm the iOS upgrade suggestion bot. It looks like you are using an older version of iOS 11. You should upgrade to the latest version to fix a bug that substitutes garbage characters for the letter 'i'.\n\n[See this article at The Verge for more information about the bug.](https://www.theverge.com/2017/11/6/16611756/ios-11-bug-letter-i-a-unicode-symbol)")
	# 				except requests.exceptions.HTTPError as e:
	# 					print(e.response.status_code)
					except praw.errors.HTTPException as e:
						exc = e._raw
						print(exc.status_code)
						time.sleep(1 * 60)
					except Exception as e:
						print("General exception")
						print(e)
	except KeyboardInterrupt:
		print("\nKeyboard interrupt detected")
		done = True
	except Exception as e:
		print("Exception ", e)
		time.sleep(10 * 60)
		print("\nRestarting")

print("Shutting down.")
