var app = Vue.createApp({
    compilerOptions: {
        delimiters: ["[[", "]]"]
    },
    data(){
        return {
            posts : []
        }
    },
    created(){
        console.log("hello s")
        $.ajax({
            url: "http://127.0.0.1:8000/post/0",
            type: "GET",
            success: (result) => {
                this.posts = result.posts
                console.log(result.data)
            },
            error:(err, status)=>{
                console.log(status)
            }
        })
    }
})


app.component('post', {
    template: `
        <div class="post">
            <h1> {{ title }}</h1>
            <hr/>
            <p> {{ content }} </p>
        </div>
    `,
    props: ['title', 'content'],

})

app.mount("#app")