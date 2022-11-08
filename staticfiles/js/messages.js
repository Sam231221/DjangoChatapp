let input_message = $('#input-message')
let message_body = $('.msg_card_body')
let send_message_form = $('#send-message-form')
const USER_ID = $('#logged-in-user').val()

let loc = window.location
let wsStart = 'ws://'

if(loc.protocol === 'https:') {
    wsStart = 'wss://'
}

let endpoint = wsStart + loc.host + loc.pathname
    var socket = new WebSocket(endpoint)

function get_active_other_user_id(){
    let other_user_id = $('.messages-wrapper.is_active').attr('other-user-id')
    other_user_id = $.trim(other_user_id)
    return other_user_id
}

function get_active_thread_id(){
    let chat_id = $('.messages-wrapper.is_active').attr('chat-id')
    console.log('chat-id:', chat_id)
    //get 1 from chat_1 by replace()
    let thread_id = chat_id.replace('chat_', '')
    console.log(thread_id)
    return thread_id
}

//send data to backend using WebSocket
socket.onopen = function(e){
    console.log('open', e)
    get_active_thread_id()
    send_message_form.on('submit', function (e){
        e.preventDefault()
        console.log('hello')
        let message = input_message.val()
        let send_to = get_active_other_user_id()

        let thread_id = get_active_thread_id()
        console.log(message,USER_ID ,send_to, thread_id)
        /*
        this is the main data object that we have to send, So
        We can identify which channel to broadcat the message to
        */
        let data = {
            'message': message,
            'sent_by': USER_ID,
            'send_to': send_to,
            'thread_id': thread_id
        }
        data = JSON.stringify(data)
        console.log('data:',data)
        socket.send(data)
        $(this)[0].reset()
    })
}


//Render left side messages
function newMessage(message, sent_by_id, thread_id, user_image, msg_timestamp) {
    
	if ($.trim(message) === '') {
		return false;
	}
	let message_element;
	let chat_id = 'chat_' + thread_id
    let send_at;
    console.log(moment(msg_timestamp).format('MMMM Do YYYY, h:mm:ss a'))
    console.log(moment().format('MMMM Do YYYY, h:mm:ss a'))

    if (moment(msg_timestamp).format('MMMM Do YYYY, h:mm a') == moment().format('MMMM Do YYYY, h:mm a')){
       send_at ='Just now'
    }else{
        send_at = moment(msg_timestamp).format('MMMM Do YYYY, h:mm:ss a')
    }
    console.log(send_at)
    //if the user_is has sent the data append it on right side
    //Sender Messages
	if(sent_by_id == USER_ID){
	    message_element = `
            <div class="messages d-flex you-message">
                <p>${message}
                    <br>
                    <span> ${send_at}</span>
                </p>
            </div>
	    `
    }
    //else append it on right side
    //Receive Messages
	else{
	    message_element = `
        <div class="messages d-flex friend-message">
        <p>${message}
            <br>
            <span> ${send_at}</span>
        </p>
    </div>
        `

    }

    /*
      Note there are multiple div with class message-wrapper with
      attribute chat-id which is unique.(thread id).
      We wanna grab a particular div
    */
   
    let message_body = $('.messages-wrapper[chat-id="' + chat_id + '"] .chat')
	message_body.append($(message_element))
    message_body.animate({
        scrollTop: $(document).height()
    }, 100);
	input_message.val(null);
}


//on receiving message from backend(i.e self.send())
socket.onmessage = function(e){
    console.log('message', e)
    let data = JSON.parse(e.data)
    let message = data['message']
    let sent_by_id = data['sent_by']
    let thread_id = data['thread_id']
    let user_image = data['user_image']
    let msg_timestamp=data['msg_timestamp']
    newMessage(message, sent_by_id, thread_id, user_image, msg_timestamp)
}

socket.onerror = function(e){
    console.log('error', e)
}

socket.onclose = function(e){
    console.log('close', e)
}



//Set active left user
const btns = document.querySelectorAll("[data-target-tab]");
console.log(btns)
btns.forEach((btn) => {
  btn.addEventListener("click", () => {
    btns.forEach((btn) => btn.classList.remove("active"));

    const items = document.querySelectorAll(".messages-wrapper");

    items.forEach((item) => item.classList.remove("active"));
    
    btn.classList.add("active");
    console.log('tg:',document.querySelector(btn.dataset.targetTab))
    document.querySelector(btn.dataset.targetTab).classList.add("is_active");
  });
});


$('.contact-li').on('click', function (){

    // message wrappers
    let chat_id = $(this).attr('chat-id')
    $('.messages-wrapper.is_active').removeClass('is_active')
    $('.messages-wrapper[chat-id="' + chat_id +'"]').addClass('is_active')

})

