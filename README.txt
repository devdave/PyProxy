Coming out of nothing and into supah doopa Alpha is finally a working proof of concept of my python web proxy. I don.t really want to talk about the asinine alternatives I.ve tried until I finally said .fuck it, time to go completely twisted!. Low and behold the actual proxy part is 4 lines of code, which is then expanded to maybe 20-30 to allow for overloading some lower level classes.

Originally a public announcement for this project would have been in August at the earliest, give me time to clean things up and go from proof of concept to working concept but apparently a lot of other people have similar thoughts and I figured it.s better to collaborate then compete.

So some quick notes:
The ultimate goal for PyProxy ( or whatever it ends up being named ) is to sit between a developer and a development server. The first and immediate idea for this was to automagically parse out Python mechanize scripts to replicate the traffic. These mechanize scripts could then be collected into a suite, marking other scripts as requirements ( example login process ). That alone would make it pretty easy to create full system under test unit-tests. The next idea was to add in regex or pattern based hooks that could allow a developer to dial in to a specific domain, or even a specific set of webpages.

After that, the idea was to just continually tack on support plugins and scripts, maybe tell PyProxy the name of the target application.s database, and if it.s MySQL, switch on the general log. This could allow for combining both mechanize scripts AND a SQLObject or SQLAlchemy powered unit-test suite to assert that the correct data was changed.

The final future idea was to make a Firefox/Chrome extension that would allow a developer to control some parts of the proxy from their browser and also see additional information. For Python and PHP web apps, imagine have a finalization plugin that appended a response header listing all File.s used to perform a request.. then imagine having a .click to edit. button that, if the dev. instance is workstation local, would have your favorite IDE open the specified file for editing.

All in all, I think these are really subtle idea.s that if combined together, would cut down some mudane parts of developing a web app.
