[![License](https://img.shields.io/github/license/italia/bootstrap-italia.svg)](https://github.com/italia/bootstrap-italia/blob/master/LICENSE)

# What is Telegraphbot
Telegraphbot is a handy Python tool that allows newcomers to the world of Telegram bots to easily build one and in particular it allows to structure the conversation following a graph paradigm.
  



## Installation

There are two ways to install the library:

* Via pip:

```
$ pip install telegraphbot
```
* Via git:

```
$ git clone https://github.com/PythonUser-ux/Telegraphbot.git
$ cd Telegraphbot
$ python setup.py install
```
or:
```
$ pip install git+https://github.com/PythonUser-ux/Telegraphbot.git
```
# The graph paradigm

Using telegraphbot every conversation can be represented as an oriented graph in which nodes represent states and arcs represent the possible transitions. <br> Every state is given by: <br>
- an integer for the degree of depth (distance from the initial node)
- a (optional) string to introduce the user to the state (typically a question)
- an ordered list of answers accepted by the bot during that state
- an ordered list of functions to be called for the corresponding accepted answers
- a function to be called in case the user input is not among the accepted ones
- an (optional) ordered list of successive nodes

Therefore each input given by the user is associated with a function call which can do whatever you want!

The conversation always starts at depth 0 by simply launching the bot using the command "/start" in the chat.
Only one node should have 0 depth.

There can be arcs exiting from an edge which does not enter in any edge, this is because we may be only interested in the transition (a function call).

# Example

Let's see how it works.

## Step 1: Obtaining an API token

First of all look for [@BotFather](https://core.telegram.org/bots#botfather) on Telegram, this is the father of all bots: it explains you how to get your bot registered on Telegram's servers and gives you the API required to control your bot.

## Step 2: Design your bot
> *Draw a graph of what your program will do*

![](Draft.png)

It can be useful to make a draft of your bot if it becomes too complex.

## Step 3: Instantiate the bot

```python
from telegraphbot import BOT, Command

API_TOKEN = 'SECRET_TOKEN'

my_bot = BOT(name="Wall-e", token=API_TOKEN)
```

## Step 4: Make your "first steps"

A conversation node is created by defining a function taking only *message* as argument and its body is just a call of the *chat_step* method.

```python

lz=my_bot.lazy
unrecognized=my_bot.unrecognized
chat_step=my_bot.chat_step

def step0(message):
    chat_step(0, message, "What are your orders?", ["Hit the console", "Give me an opinion"], [action1, lz], unrecognized, next_steps=[None,step1])
    
def action1(message):
    for i in range(10):
        print("SPAM")
    my_bot.reset()

```
In so doing we are creating a very first node for our conversation. <br> After sending the command "/start" our bot will be asking "What are your orders?" and the only accepted answers are those passed as next argument.<br> The first input will cause the call of *action1* and since the corresponding next step is *None* then the bot will not proceed to a next node; the second proper answer will call the function *my_bot.lazy*, which does literallly nothing, but this time *step1* will be the next state. Of course, *step1* needs to be defined as well. <br> *my_bot.unrecognized* is the default function called when the user inputs an unaccepted answer. <br> Note that for every function called by mean of a transition *message* should be the only argument. <br> Even tough this may seem limiting, other "arguments" can actually be passed using global variables, and it is not a big deal assuming the only reason why a function changes its behaviour is due to user inputs. This point will be adressed in details in the next uptades of this description.

```python
from anything import Anything

def step1(message):
    chat_step(1, message, "Okay, send me a selfie", [Anything], [make_a_compliment], unrecognized, next_steps=[])

def make_a_compliment(message):
    if message.content_type=="photo":
        my_bot._bot.send_message(message.chat.id,"You look cool!")
    else:
        my_bot._bot.send_message(message.chat.id,"Don't be shy!")
    my_bot.reset()
```

What this step does is simply to accept everything and to call the *make_a_compliment* function that sends a different message to the user depending on the type of the input. <br>

If the bot receives a file, the content is automatically stored by default in the same directory of the source code and named with a trivial name. To modify this behaviour you should specify a directory when instantiating the bot. Moreover, a file can be saved with a different name if it is sent with a caption, in this case the caption becomes the file name.

As you may have noted, each time a function is also meant to restart the bot, the *reset()* method is called; this will bring your bot before its activation. An alternative to *reset()* is *soft_reset()* that brings the bot at the state of depth 0 and you do not need to send "/start" again.

Note that *step1* has depth 1 as it is the son of a step of depth 0.

## Step 5: Add the steps

```python
my_bot.steps.append(step0)
my_bot.steps.append(step1)

# Or
# my_bot.steps=[step0,step1]
```

Important: the root node should be added as first.

## Step 6: Activate the bot

```python
my_bot.polling()
```

This function should not be called more than once.

# Hints and warnings

Here are some suggestions to shape your bot in greater detail.

- Make large use of global variables to modify your bot behaviour.

- Define your own "unrecognized" function for each step and take into account that the default function can be defined in the following way:

```python
def unrecognized(message):
        s._bot.send_message(message.chat.id,"Unrecognized")
        s._conversation.pop()
        s._deep_degree-=1
```

Similarly to *actions* it should only take *message* as argument and you may want to arbitrarily modify the *_conversation* and the *_deep_degree* variables. <br>
The first variable is the stack made by all the accepted answers by the user so far plus the last answer, so you would at least remove the latter.
The second variable is the degree of depth, which should be decreased of exactly the number of words removed from the stack. <br> Those are the only limitations on the unrecognized function you choose.

# Work in progress

This tutorial contains the absolute minimum to get started, new uptades are coming from month to month.

# Licence
MIT Licence
# Author
Made by Andrea Virgillito.
