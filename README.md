[![License](https://img.shields.io/github/license/italia/bootstrap-italia.svg)](https://github.com/italia/bootstrap-italia/blob/master/LICENSE)

# What is Telegraphbot
Telegraphbot is a handy Python tool that allows newcomers to the world of Telegram bots to easily build one and in particular it allows to structure the conversation following a graph paradigm.<br>

The main class of this library is *BOT* and it inherits its deeper functionalities from another library called *[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)*. <br> Understanding the mentioned library is not required for you to follow this tutorial; however it would be quite useful have a look to it as it will increase for sure your knowledge about the whole world of Telegram bots and *telegraphbot* itself.

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
- an ordered list of functions to be called for the corresponding accepted answers. It should contain as many elements as the number of accepted answers from the user
- a function to be called in case the user input is not among the accepted ones
- an (optional) ordered list of successive nodes. If specified it should contain as many elements as the number of accepted answers from the user

Therefore each input given by the user is associated with a function call which can do whatever you want!

The conversation always starts at depth 0 by simply launching the bot using the command "/start" in the chat. Only one node should have 0 depth.

There can be arcs exiting from an edge which does not enter in any other edge, this is because we may only be interested in the transition (i.e. just the a function call).

# Example 1

Let's see how it works.

## Step 1: Obtaining an API token

First of all look for [@BotFather](https://core.telegram.org/bots#botfather) on Telegram, this is the father of all bots: it explains you how to get your bot registered on Telegram's servers and gives you the API token required to control your bot.

## Step 2: Design your bot
> *Drawing of a graph of what your program will do*

![](Draft.png)

It can be useful to make a draft of your bot as it gets more complex.

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
In so doing we are creating a very first node for our conversation. <br> After sending the command "/start" our bot will be asking "What are your orders?" and the only accepted answers are those passed as next argument.<br> The accepted first input causes the call of *action1* and since the corresponding next step is *None* then the bot will not proceed to any next node; similarly the second proper answer calls the function *my_bot.lazy*, which does literally nothing, but this time *step1* is going to be the next state. Of course, *step1* needs to be defined as well. <br> *my_bot.unrecognized* is the default function called when the user inputs an unaccepted answer. <br> Notice that for every function called while passing from a state to another the argument *message* is necessary and it should be the only one. <br> This may seem somehow limiting, but it is not actually. This point will be addressed later.

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

What this step does is to simply accept everything and to call the *make_a_compliment* function that sends a different message to the user depending on the type of the input. <br>

If the bot receives a file, the content is automatically stored by default in the same directory of the source code and named with a trivial name. To modify this behaviour you should specify a directory when instantiating the bot using the argument *directory*. Moreover, a file can be saved with a different name if it gets sent with a caption, in which case the file takes the same name as the caption of the file.

As you may have noticed, each time a function is also meant to restart the bot we call the *reset()* method; this will bring your bot back to the state before its activation (at depth -1). An alternative to *reset()* is *soft_reset()* that brings the bot at the state of depth 0 and you do not need to send "/start" again.

Note that *step1* has depth 1 as it is the son of a step of depth 0.

## Step 5: Add the steps

```python

my_bot.steps=[step0,step1]

# Or
# my_bot.steps.append(step0)
# my_bot.steps.append(step1)
```

Important: the root node should be added as first.

## Step 6: Activate the bot

```python
my_bot.polling()
```

This function should not be called more than once.

# Example 2

As another example it is possible to use *telegraphbot* to build the control menu of an Arduino ultrasonic burglar alarm I created.<br>
Give it a look [here](https://github.com/PythonUser-ux/Arduino-alarm).

# Hints and warnings

## Here are some suggestions for you to shape your bot in greater detail.

## Make large use of global variables to modify your bot behaviour. <br>
The following is an example of action definition.

```python
MIN_LOG=999
def duration_change(message):
    global MIN_LOG
    MIN_LOG=int(message.text)
    if MIN_LOG>59:
        s._bot.send_message(message.chat.id, "Control duration successfully changed to "+str(MIN_LOG//60)+" hours "+str(MIN_LOG%60)+" minutes")
    else:
        s._bot.send_message(message.chat.id, "Control duration successfully changed to "+str(MIN_LOG)+" minutes")
    s.soft_reset()
```

## Define your own "unrecognized" function for each step
Check below how an "unrecognized" function should look like by taking as example the default one:

```python
def unrecognized(message):
        s._bot.send_message(message.chat.id,"Unrecognized")
        s._conversation.pop()
        s._deep_degree-=1
```

Similarly to *actions* it should only take *message* as argument and you may want to arbitrarily modify the *_conversation* and the *_deep_degree* hidden variables. <br>
The first variable is the stack made by all the accepted answers the user gave so far plus the last (to be checked) answer, so you would at least remove the latter using *s._conversation.pop()*.<br>
The second variable is the degree of depth, which should be decreased of exactly the number of words removed from the stack. <br> Those are the only limitations on the unrecognized function you choose, this is done via *s._deep_degree-=1*.

## Restrict your bot users
When creating an instance of the BOT class use the *allowed* argument to pass a list of strings of Telegram member IDs to specify who is allowed to use the bot.<br>
To know your member ID you could just print out *message.chat.id* from one of your chat steps.

## Define new commands

Using the argument *other_commands* you can add your own commands:

```python
from telegraphbot import Command

def function_scream(message):
    for i in range(8):
        s._bot.send_message(message.chat.id, "AAAAAAAAAAAAAAAAAAAAAAAAA")

scream_command = Command("scream",function_scream)

s=BOT("Wall-e",API_TOKEN,other_commands=[scream_command])
```

A *Command* object just takes two arguments: the name of the command and a function taking only *message* as argument. <br>
Once defined, your command can be called by typing "/"+command.name. For instance in the case above, you should send "/scream" in the chat with your bot.

## Do not share your personal token
Anyone with it can code your bot.

# Work in progress

This tutorial contains the absolute minimum to get started, new uptades may come in the next months.<br>
Always take the GitHub page as reference for the full tutorial.

# Licence
MIT Licence
# Author
Made by [Andrea Virgillito](https://github.com/PythonUser-ux).
