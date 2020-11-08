# utils
Some small utility programs that might be useful.

ActivityLogger
--------------
This program is supposed to show a simple UI for managing different activities.
This is a sort of 'gamification' for tasks that you want to do regularly, but
often fail to do due to lazyness or whatever. You can add activities and how
often you want to perform them, like 'work on my thesis at least once a day', 
or 'go to the dentist at least twice a year', and 'log in' whenever you actually
performed that activity. When it's done, this program will not only keep track
of when you performed and when you slacked, but also provide some statistict, 
and maybe also points and badges and other gamification stull to help you keep 
going.

*very early version*


BibAnalyzer
-----------
When this is done, its supposed to be a small utility program or library for
analyzing bibliography databases, primarily BibTex.

Some ideas so far:

* group papers by authors, show topics by author and/or year
* show "hot" topics (title words, bigrams, trigrams), possibly as a tag-cloud
* create graphs showing co-author relationsships and author-"cliques"

*very early version*


ESColorChooser
--------------
The idea behind this program is to use a very simple form of Evolution Strategy
for modifying a color sample until it fits one's needs without having to care
about what exact hue, saturation, or whatever the desired color needs to have.

After picking a color to start, eight similar colors are generated, and after 
picking one of those, another eight similar colors, and so on, until the color
converges to what is wanted.


PictureUtil
-----------
This package contains a few useful utilities for managing picture collections.

The first program can be used for ranking pictures from a folder, for example
when you have hundreds of pictures taken in your last vacation and you want to
find a selection of the best few pictures for your album.

The program works by repeatedly placing two random pictures next to each other
and having the user spontaneously decide which one is better, tournament-style.
After a few minutes of somewhat consistent voting, the best pictures are found.

Another program can be used to arrange pictures freely and to rename them
according to their new order. While this is possible in some file manager or
photo management software, in a surprisingly high number it is not. This can
be useful e.g. when digitizing old scanned photos, or when merging collections
having different file name patterns and possibly diverging camera time settings.


QuickReader
-----------
A screen reader for quickly 'scanning' long texts by briefly flashing the single
words on the screen.

Not really sure how well this works. Newer really tried it on a longer text...


SoundDelay
----------
What this program is supposed to do is to capture audio (speech) from the 
microphone and to play it back to the user's headphones with a very small delay
of about 1/20 to 1/10 of a second.

There are some (very expensive) devices, that claim to do the same and are
supposed to have a beneficial effect on stammering. This program is supposed to
replicate this effect. 

Not at all sure whether this actually works, but if it does, I'm planning to 
turn this into an Android app.

*very early version*


UmlautEscape
------------
A simple command-line tool for replacing Umlauts in HTML and Latex documents.
