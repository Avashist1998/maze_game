from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

import pygame
from pygame.event import Event
from typing import List

#make sure redirect URL is: http://localhost:17563

APP_ID = 'APP_ID'
APP_SECRET = 'APP_SECRET'
USER_SCOPE = [AuthScope.CHAT_READ]
TARGET_CHANNEL = 'abhayisontwitch'

class TwitchFeed():
    event_queue: List[Event] = []

    # this will be called when the event READY is triggered, which will be on bot start
    async def on_ready(self, ready_event: EventData):
        print('Bot is ready for work, joining channels')
        # join our target channel, if you want to join multiple, either call join for each individually
        # or even better pass a list of channels as the argument
        await ready_event.chat.join_room(TARGET_CHANNEL)
        # you can do other bot initialization things in here


    # this will be called whenever a message in a channel was send by either the bot OR another user
    async def on_message(self, msg: ChatMessage):
        if msg.text == "down":
            self.event_queue.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
        elif msg.text == "up":
            self.event_queue.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
        elif msg.text == "left":
            self.event_queue.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT))
        elif msg.text == "right":
            self.event_queue.append(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT))

        print(f'in {msg.room.name}, {msg.user.name} said: {msg.text}')


    # this will be called whenever someone subscribes to a channel
    async def on_sub(self, sub: ChatSub):
        print(f'New subscription in {sub.room.name}:\n'
              f'  Type: {sub.sub_plan}\n'
              f'  Message: {sub.sub_message}')


    # this will be called whenever the !reply command is issued
    async def test_command(self, cmd: ChatCommand):
        print("cmd:", cmd)
        # if len(cmd.parameter) == 0:
        #     await cmd.reply('you did not tell me what to reply with')
        # else:
        #     await cmd.reply(f'{cmd.user.name}: {cmd.parameter}')


    # this is where we set up the bot
    async def run(self):
        # set up twitch api instance and add user authentication with some scopes
        twitch = await Twitch(APP_ID, APP_SECRET)
        auth = UserAuthenticator(twitch, USER_SCOPE)
        print("asking for token")
        token, refresh_token = await auth.authenticate()
        print(token, refresh_token)
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

        # create chat instance
        chat = await Chat(twitch)

        # register the handlers for the events you want

        # listen to when the bot is done starting up and ready to join channels
        chat.register_event(ChatEvent.READY, self.on_ready)
        # listen to chat messages
        chat.register_event(ChatEvent.MESSAGE, self.on_message)
        # listen to channel subscriptions
        chat.register_event(ChatEvent.SUB, self.on_sub)
        # there are more events, you can view them all in this documentation

        # you can directly register commands and their handlers, this will register the !reply command
        chat.register_command('reply', self.test_command)


        # we are done with our setup, lets start this bot up!
        chat.start()

        # lets run till we press enter in the console
        try:
            while True:
                print("Doing the twitch thing")
                await asyncio.sleep(2)
        finally:
            # now we can close the chat bot and the twitch api client
            chat.stop()
            await twitch.close()

    # @asyncio.coroutine
    def start_polling(self):
         asyncio.run(self.run())

    # def main():
    #     # lets run our setup
    #     asyncio.run(run())