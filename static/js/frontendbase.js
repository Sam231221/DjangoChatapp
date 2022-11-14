console.log('adasda')
$(document).ready(function() {
    /*--------------------
    CSRF_TOKEN
    ----------------------*/
    const getToken = (name) => {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(
                        name.length += 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    let csrftoken = getToken('csrftoken');


	/*--------------------
    SEARCH ENGINE
    ----------------------*/
	console.log('sds')
    const sendSearchData = (keyword) => {
        $.ajax({
            type: "POST",
			//{% url 'search-view' %}
            url: "/search/",
            data: {
                'csrfmiddlewaretoken': csrftoken,
                'keyword': keyword,
            },
            beforeSend: function () {
                //user can't click the button by the time
                $("#loading").addClass('spinner-border');
                $("#spinner").addClass('visually-hidden');
            },
            success: function (response) {
                console.log(response)
                const data = response.queryset
                if (Array.isArray(data)) {

                    searchquery.innerHTML = " "
                    data.forEach(keyword => {
                        searchquery.innerHTML +=
                            `<li class="mb-2 search-obj pt-3 pb-3 px-4">
							<img src="${keyword.image}" class="rounded-circle" width="36" height="36" />
							<a class="text-black" href="${keyword.url}" style="text-decoration:none;">
							<b>${keyword.username}</b>
							</a>
							</li> `
                    })
                } else {
                    if (searchinput.value.length > 0) {
                        searchquery.innerHTML = `<p  class="text-black pt-3 pb-3 px-4">${data}</p> `
                    } else {
                        searchquery.classList.add("invisible");
                    }
                }
            },
            error: function (error) {
                console.log(error.data)
            }


        })
    }

	const searchform = document.getElementById("search-form")
    const searchinput = document.getElementById("search-input")
    const searchquery = document.getElementById("search-query")

    const csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0].value
    console.log(csrf_token)
    searchinput.addEventListener("keyup", e => {
        console.log("printing", e.target.value)
        if (searchquery.classList.contains('invisible')) {
            searchquery.classList.remove('invisible')
        }
        sendSearchData(e.target.value);
    })


    
});