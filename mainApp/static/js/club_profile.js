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
    methods: {
        showModal(){
            $("#myModal").fadeIn()
        }
    }, 
    mounted(){
        console.log("mounted")
    },
    created(){
        console.log("created")
    }
})

app.component('create-post-modal', {
    template: `
    <div id="myModal" class="modal">
        <div class="modal-content">
            <span class="close" @click="hideModal">&times;</span>
            <h1> Create a Post </h1>
             <form id="post_form">
                <input class="form-control" type="text" name="title" v-model="title"/>
                <textarea class="form-control" name="content" v-model="content">  </textarea>
                <input type="datetime-local" class="form-control" v-model="started_at" />
                <input class="btn btn-primary" type="submit" value="post" id="post" @click="add_post">
            </form>
        </div>
    </div>
    `,
    data(){
        return {
            title: "",
            content: "",
            started_at: ""
        }
    },
    methods: {
        add_post(event){
            event.preventDefault()
            $.ajax({
                url: "http://127.0.0.1:8000/post/0",
                type: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data : `title=${this.title}&content=${this.content}`,
                 success(result){
                    console.log("success !!!")
                }
            })
        },
        hideModal(){
            $("#myModal").fadeOut()
        }
    }
})

app.mount("#app")