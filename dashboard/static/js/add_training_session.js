var app = Vue.createApp({
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },

    data(){
        return {
            // form data
            title: "mohcine title ....",
            content: "hello world, kldfdlkndkfgnlknfdggln",
            presented_by: "",
            started_at: "2022-03-12T22:18",
            limited_places: 0,
            // btn property
            disbled: true,
            vPresentedBy: false,
            // username auto-complete
            isOpen: false,
            results: []
        }
    }, methods: {
        validate(){

            var vTitle = this.title.length != 0
            var vContent = this.content.length != 0
            var vStartedAt = this.started_at.length != 0
            var vLimitedPlace = this.limited_places >= 0
            this.disbled = !(vTitle && vContent && vStartedAt && this.vPresentedBy && vLimitedPlace)
        }, submit(e){
            e.preventDefault()
            var form = new FormData($('form')[0])
            form.append('file', $('#file')[0].files[0])
            form.append('club', 'club informatique')
            $.ajax({
                url: "",
                contentType: 'multipart/form-data',
                type: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data : form,
                success(result){
                    console.log("success !!!")
                },
                cache: false,
                contentType: false,
                processData: false
            })
        }, select(e){
            this.presented_by = $(e.target).html()
            this.isOpen = false 
            this.vPresentedBy = true
            this.validate()
        }, async filterUsers(e){
            
           await $.ajax({
                url: "http://127.0.0.1:8000/users/",
                type: "GET",
                data: `username=${this.presented_by}`,
                success(data){
                    window.localStorage.setItem('users', data.users)
                }, 
                cache: false,
                contentType: false,
                processData: false
            })
        }, getUsers(e){
            this.filterUsers(e)
            this.filterUsers(e)
            console.log(
                window.localStorage.getItem('users').split(',')
            )
            this.results = window.localStorage.getItem('users').split(',')
            window.localStorage.removeItem('users')
            this.isOpen = this.results.length != 0
        }
    }, created(){
        console.log('created')
        window.localStorage.setItem('users', '')
    }
})

app.mount("#app")