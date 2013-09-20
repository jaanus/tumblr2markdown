#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytumblr
from datetime import datetime # for strptime
import re
import os
import codecs
import argparse



def processPostBodyForImages(postBody, downloadImages, imagesPath):

	if not downloadImages:
		return postBody

	print "should process body here"
	return postBody



def downloader(apiKey, host, postsPath, downloadImages, imagesPath):

	# Authenticate via API Key
	client = pytumblr.TumblrRestClient(apiKey)

	# http://www.tumblr.com/docs/en/api/v2#posts

	# Make the request

	processed = 0
	total_posts = 1

	posts_per_type = {}

	while (processed < total_posts) and (processed < 50):
		response = client.posts(host, limit=20, offset=processed, filter='raw')
		total_posts = response['total_posts']
		posts = response['posts']
		processed += len(posts)

		for post in posts:

			try:
				posts_per_type[post['type']] += 1
			except KeyError:
				posts_per_type[post['type']] = 1

			postDate = datetime.strptime(post["date"], "%Y-%m-%d %H:%M:%S %Z")

			if post['type'] == 'text':

				title = post["title"]
				body = post["body"]

			elif post["type"] == "photo":
				title = "Photo post"
				body = "{% img " + post["photos"][0]["original_size"]["url"] + " %}\n\n" + post["caption"]

			elif post["type"] == "video":
				title = "Video post"

				known_width = 0
				for player in post["player"]:
					if player["width"] > known_width:
						player_code = player["embed_code"]

				body = player_code + "\n\n" + post["caption"]

			elif post["type"] == "link":
				title = "Link post"

				body = "<" + post["url"] + ">\n\n" + post["description"]

			elif post["type"] == "quote":

				title = "Quote post"

				body = post["source"] + "\n\n<blockquote>" + post["text"] + "</blockquote>"

			else:
				title = "(unknown post type)"
				body = "missing body"

				print post

			# download images if required
			body = processPostBodyForImages(body, downloadImages, imagesPath)

			# we have processed the post, have "title" and "body" by now, let’s dump it on disk

			# generate a slug out of the title: replace weird characters …
			slug=re.sub('[^0-9a-zA-Z- ]', '', title.lower().strip())

			# … collapse spaces …
			slug=re.sub(' +', ' ', slug)

			# … convert spaces to tabs …
			slug = slug.replace(' ', '-')

			# … and prepend date
			slug = postDate.strftime("%Y-%m-%d-") + slug + ".markdown"

			# if path does not exist, make it
			if not os.path.exists(postsPath):
				os.makedirs(postsPath)

			f = codecs.open(os.path.join(postsPath, slug), encoding='utf-8', mode="w")

			tags = ""
			if len(post["tags"]):
				tags = "\ntags:\n- " + "\n- ".join(post["tags"])

			f.write("---\nlayout: post\ndate: " + post["date"] + tags + "\ntitle: \"" + title.replace('"', '\\"') + "\"\n---\n" + body)

			f.close()

		print "Processed", processed, "out of", total_posts, "posts"

	print "Posts per type:", posts_per_type



def main():
	
	parser = argparse.ArgumentParser(description="Tumblr to Markdown downloader",
		epilog = """
		This app downloads all your Tumblr content into Markdown files that are suitable for processing with Octopress. It optionally also downloads the images hosted on Tumblr and replaces their URLs with locally hosted versions.
		""")
	parser.add_argument('--apikey', dest="apiKey", required=True, help="Tumblr API key")
	parser.add_argument('--host', dest="host", required=True, help="Tumblr site host, e.g example.tumblr.com")
	parser.add_argument('--posts-path', dest="postsPath", default="_posts", help="Output path for posts, by default “_posts”")
	parser.add_argument('--download-images', dest="downloadImages", action="store_true", help="Whether to download images hosted on Tumblr into a local folder, and replace their URLs in posts")
	parser.add_argument('--images-path', dest="imagesPath", default="images", help="If downloading images, store them to this local path, by default “images”")

	args = parser.parse_args()

	if not args.apiKey:
		print "Tumblr API key is required."
		exit(0)

	if not args.host:
		print "Tumblr host name is required."
		exit(0)

	downloader(args.apiKey, args.host, args.postsPath, args.downloadImages, args.imagesPath)



if __name__ == "__main__":
    main()
