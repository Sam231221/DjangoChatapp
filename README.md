# Chat-app
## Real-Time Chatting app in Django with Channels. (Whatsapp Web Clone)

# Database Model understanding
Thread is an model which relies on two person(sender and reciever). So it uses Tww ForeignKeys to User model.

Take a example of Messenger chatting.
--------------------------------------------------------
When you(Sam) become friend with Ram in Facebook Messenger.
Then only, An Instance of Thread will be created.
For Sam, The thread will have attributes:
first_person = Sam and second_person = Ram

However, For Ram, The thread will have attributes:
first_person = Ram and second_person = Sam

A chat message will be associated with each thread with Foriegn key.
