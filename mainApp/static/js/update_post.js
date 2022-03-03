const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var app = Vue.createApp({
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data(){
        return {
            title: "",
            content: "",
            disbled: true
        }
    },methods: {
        submit(event){
            event.preventDefault()
            $.ajax({
                url: "http://127.0.0.1:8000/post/1",
                type: "PUT",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'title': this.title,
                    'content': this.content
                },
                success: (result) => {
                    console.log(result)
                },
                error:(err, status)=>{
                    console.log(status)
                }
            })
        },

        validate(){
            this.disbled = this.title.length == 0 || this.content.length == 0
        }
    }
})

app.mount("#app")