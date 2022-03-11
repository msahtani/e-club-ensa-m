var app = Vue.createApp({
    data(){
        return {
            // form data
            title: "mohcine title ....",
            content: "hello world, kldfdlkndkfgnlknfdggln",
            presented_by: "mohcine sahtani",
            started_at: "2022-03-12T22:18",
            limited_places: 0,
            // bnt property
            disbled: true
        }
    }, methods: {
        validate(){

            var vTitle = this.title.length != 0
            var vContent = this.content.length != 0
            var vStartedAt = this.started_at.length != 0
            var vPresentedBy = this.presented_by.length != 0 // TODO: ......
            var vLimitedPlace = this.limited_places >= 0
            console.log(
                this.started_at
            )
            this.disbled = !(vTitle && vContent && vStartedAt && vPresentedBy && vLimitedPlace)
        }, submit(e){
            e.preventDefault()
            var form = new FormData($('form')[0])
            form.append('file', $('#file')[0].files[0])
            form.append('club', 'club informatique')
            $.ajax({
                url: "http://127.0.0.1:8000/trs/0",
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
        }, 
        validate2(){
            console.log(
                this.started_at.toString()
            )
        }
    }
})

app.mount("#app")