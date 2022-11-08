import json
import time
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from MChat.models import Thread, ChatMessage

from django.utils.timezone import localtime

User = get_user_model()

#Each Consumer accepts WebSocketConnection
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        user = self.scope['user']
        self.chat_room = f'user_chatroom_{user.id}'
        print("....", self.chat_room)
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )
        #for establishing connection between consumer and websocket.
        await self.send({
            'type': 'websocket.accept'  # needed
        })
        
        
   #THIS function is called when we recive any message from frontend (i.e socket.send() in message.js line 36)
    async def websocket_receive(self, event):
        print('receive', event)
        received_data = json.loads(event['text'])
        print('Received Event:', received_data)
        msg = received_data.get('message')
        sent_by_id = received_data.get('sent_by')
        send_to_id = received_data.get('send_to')
        thread_id = received_data.get('thread_id')

        if not msg:
            print('Error:: empty message')
            return False

        sender_obj = await self.get_user_object(sent_by_id)
        print('sender_obj:', sender_obj)
        reciever_obj = await self.get_user_object(send_to_id)
        print('reciever_obj:', reciever_obj)
        thread_obj = await self.get_thread(thread_id)
        if not sender_obj:
            print('Error:: Sender Invalid')
        if not reciever_obj:
            print('Error:: Receiver Invalid')
        if not thread_obj:
            print('Error:: Thread id is incorrect')

        await self.create_chat_message(thread_obj, sender_obj, msg)
        message_obj = await self.get_chat_message(thread_obj.id, sender_obj, msg)
        print("\n")
        #get the local nepal time out of utc time
        local_date = localtime(message_obj.timestamp)
        print(int(time.mktime(local_date.timetuple())) * 1000)
        other_user_chat_room = f'user_chatroom_{send_to_id}'
        self_user = self.scope['user']
        
        response = {
            'message': msg,
            'sent_by': self_user.id,
            'user_image': self_user.image.url,
            'msg_timestamp': int(time.mktime(local_date.timetuple())) * 1000,
            'thread_id': thread_id
            
            
        }

        #sent to message sender and reciever
        '''
        #await self.channel_layer.group_send(chatroom that receives event, event to be triggered):
        triggers event to all the websocket connected to the MChat room which are given as the argument
        
        Below we sending event to the two room.
        '''
        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(response)
            }
        )


    #called when the conection between websocket and consumer is gone away.
    async def websocket_disconnect(self, event):
        print('disconnect', event)

    async def chat_message(self, event):
        print('chat_message', event)
        await self.send({
            'type': 'websocket.send',  #needed
            'text': event['text']
        })

    #this decorater enures that every time connect to db, the connection is closed
    @database_sync_to_async
    def get_user_object(self, user_id):
        qs = User.objects.filter(id=user_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def get_thread(self, thread_id):
        qs = Thread.objects.filter(id=thread_id)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj

    @database_sync_to_async
    def create_chat_message(self, thread, user, msg):
        ChatMessage.objects.create(thread=thread, user=user, message=msg)
   
    @database_sync_to_async
    def get_chat_message(self, thread_id, user, msg):
        thread_obj = Thread.objects.filter(id=thread_id).first()
        qs = ChatMessage.objects.filter(thread=thread_obj,user=user ,message=msg)
        if qs.exists():
            obj = qs.first()
        else:
            obj = None
        return obj