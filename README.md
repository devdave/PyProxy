ProxyProject
============
- Author: David W
- Status: Pre-Alpha

Primary goal
------------

ProxyProject is initially meant to resolve one very common and VERY tedious part of Web development,
validating web forms.  A developer would place Proxy Project between their browser and their development environment
then run through the process of populating and submitting a form.  After the developer would return to the Proxy
Project control panel and click a button, in return a python mechanize script would be presented.


Secondary goals
--------------

Since the Proxy is already recording everything, additional features would be the ability to replay the response side
of requestes on demand ( basically caching the respons ).

The ability to mechanize scripts into "story" scripts, to make it easier to re-use and organize them for building up
front loaded system under-test scripts.


Could be nice goals
-------------------

A tool to marry SQL statements stored in a MySQL general log file to individual responses, perhaps make it easier to add
additional DB level post mechanize

