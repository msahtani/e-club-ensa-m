var app = Vue.createApp({
    data(){
        return {
            // form data
            title: "",
            content: "",
            presented_by: "",
            started_at: "",
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

        }, 
        validate2(){
            console.log(
                this.started_at.toString()
            )
        }
    }
})

app.mount("#app")