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
            url: "",

            disbled: true
        }
    },methods: {
        submit(event){
            event.preventDefault()
            $.ajax({
                url: this.url,
                type: "PUT",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data : $("#post_form").serialize(),
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
    },
    created(){
        this.url = window.location.href.replace('/update', '')
        $.ajax({
            url: this.url,
            type: "GET",
            success: (result) => {
                this.title = result.title,
                this.content = result.content
            }
        })
    }
    
})

app.mount("#app")