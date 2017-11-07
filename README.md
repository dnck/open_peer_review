# Open Peer Review
A python app to find and email peer reviewers

## Introduction
Finding peer reviewers for academic articles is hard work.

First, if you're not an expert in the discipline of the article, then how do you know who to ask to review the article?

Second, there's a lot of boring administrative work like keeping track of who you emailed, when you sent the email, and the person's response, to name just a few examples.

I created this app to try and help manage the peer review process for small one-man operations.

It relies on some standard Python libraries like os, and csv and requests. But, the module zeep, along with the SOAP service run by http://jane.biosemantics.org does most of the heavy lifting for finding reviewers based on semantic search criteria.

The app is currently working for

Python 2.7.12 :: Anaconda custom (x86_64)

with conda v.4.3.23.

on a macOS Sierra v.10.12.6.

## Things that need doing

* Better doc strings in the functions
* Better documentation overall for what the app does
* Convert functions to classes and modularize
* Test in different platforms
* Test the functions for ruling out repeat emails
* Provide a better interface with Tkinter
    * For example, windows do not close after clicking submit, I'd like to change this.
* Include an automation process for accepting, interpreting, and cataloguing responses

## Running the app
If you want to just test out the app and see how it works, I encourage you to run it up until the final step of sending the actual emails. Of course, if you're really planning to respond to people and you're looking for peer reviewers, then go right ahead, and try it out. Let me know how it goes!

Best Wishes
Dan 
