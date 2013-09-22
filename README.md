## The goal

The goal of this script is to let you completely export your content hosted on Tumblr to plain Markdown files.

It downloads and converts “text”, “photo”, “video”, “link”, and “quote” post bodies. It optionally also downloads images from Tumblr into your local storage. I have built and tested it to migrate from Tumblr to Octopress, but it may have other uses as well.

I found a bunch of Tumblr exporters online, but they were mainly dealing with published site content that was already preprocessed. I did not find any exporters based on Tumblr API, so I decided to write one. Kudos to Tumblr for having a well-defined API and Python wrapper that were a joy to work with in this project. The API seems to enable unlimited data import and export. I can only wish that all products had such a great API.

## Prerequisites

Requires [py2tumblr.](https://github.com/tumblr/pytumblr)

## How to use

Just run it with -h switch.

	jaanus-mbp:tumblr2markdown jaanus$ ./tumblr2markdown.py -h
	usage: tumblr2markdown.py [-h] --apikey APIKEY --host HOST
	                          [--posts-path POSTSPATH] [--download-images]
	                          [--images-path IMAGESPATH]
	                          [--images-url-path IMAGESURLPATH]

	Tumblr to Markdown downloader

	optional arguments:
	  -h, --help            show this help message and exit
	  --apikey APIKEY       Tumblr API key
	  --host HOST           Tumblr site host, e.g example.tumblr.com
	  --posts-path POSTSPATH
	                        Output path for posts, by default “_posts”
	  --download-images     Whether to download images hosted on Tumblr into a
	                        local folder, and replace their URLs in posts
	  --images-path IMAGESPATH
	                        If downloading images, store them to this local path,
	                        by default “images”
	  --images-url-path IMAGESURLPATH
	                        If downloading images, this is the URL path where they
	                        are stored at, by default “/images”

	This app downloads all your Tumblr content into Markdown files that are
	suitable for processing with Octopress. Optionally also downloads the images
	hosted on Tumblr and replaces their URLs with locally hosted versions.

You will need a Tumblr API key, which you can get by [registering a Tumblr application.](http://www.tumblr.com/oauth/apps) Get the value called called “OAuth Consumer Key”.
