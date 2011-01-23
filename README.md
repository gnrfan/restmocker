RESTMocker
===========

RESTMocker is a (very simple at the moment) tool for mocking up RESTful webservices. It can be of helpful for prototyping a client app while the real webservice is not readily available. 

How does it work?
=================

It works by creating "realms" for specific projects and storing "documents" in each of them. This documents can be in JSON, XML or whatever format you choose to since you're simply pasting code in there and setting up an associated mime type. Regular expressions are used to match incoming HTTP requests to documents in the very same fashion of how Django routing works. Parts of the URI can be extracted and replaced in the document itself since it is trated as a Django template and the whole power of the templating language is there to be used.

An additional text substitution feature is available there to perform simple transformations in all of the documents of a given realm. This way you can, for example, replace all of the images referenced in a JSON document with one single image of your choice. This part is also powered by regular expressions.

The administrator's UI is mostly a vanilla Django admin one but works nicely for the purpose.

At Bit Zeppelin, we're using this tool for easing up our iPhone developing tasks. We hope this little product is helpful for you. 

(C) 2011 - Antonio Ognio <antonio@bitzeppelin.com>
