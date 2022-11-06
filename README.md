# Chat-app-tutorial
## Real-Time Chatting app in Django with Channels. (Whatsapp Web Clone)
You can chat with multiple persons by staying on the same page.

Explanation for this repository : https://youtu.be/205tbCUl4Uk


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

# Date formatting
new Date(1663468988000).toLocaleDateString('en-us', { day:"numeric", weekday:"long", year:"numeric", month:"short", hour:"numeric", minute:"numeric", second:"numeric"})