RESTMocker
===========

RESTMocker is a (very simple at the moment) tool for mocking up RESTful webservices. It can be of helpful for prototyping a client app while the real webservice is not readily available. 

How does it work?
=================

It works by creating "realms" for specific projects and storing "documents" in each of them. This documents can be in JSON, XML or whatever format you choose to since you're simply pasting code in there and setting up an associated mime type. Regular expressions are used to match incoming HTTP requests to documents in the very same fashion of how Django routing works. Parts of the URI can be extracted and replaced in the document itself since it is treated as a Django template and the whole power of the templating language is there to be used. Since 2011-05-08 binary documents are supported via attachments. Please keep in mind that the proper mime type for document stills need to be set manually, even when serving the contents from binary attachments.

An additional text substitution feature is available there to perform simple transformations in all of the documents of a given realm. This way you can, for example, replace all of the images referenced in a JSON document with one single image of your choice. This part is also powered by regular expressions.

The administrator's UI is mostly a vanilla Django admin one but works nicely for the purpose.

At Bit Zeppelin, we're using this tool for easing up our iPhone developing tasks. We hope this little product is helpful for you. 

Verb support
============

All HTTP verbs areare supported. 

Header support
==============

Each document will match the combination of URI + VERB + headers. By returning different responses (including status code and headers) when certain request headers match you can simulated different scenarios. E.g. Using a header named "X-Simulated-Case: missing mandatory parameter".

License
=======

RESTMocker is distributed under the BSD license.

(C) 2011 - 2013 Antonio Ognio <antonio@bitzeppelin.com>
