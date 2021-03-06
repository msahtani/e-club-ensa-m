var app = Vue.createApp({
    data(){
        return{
            username: "",
            password: ""
        }
    },
    methods: {
        login(e){
            e.preventDefault()
            $.ajax({
                url: window.location.href,
                type: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: $("#login_form").serialize(),
                success(result){
                    if (!result.message)
                        window.location.reload()
                    console.log(result.message)
                }
            })
        }
    }
})

app.mount("#app")