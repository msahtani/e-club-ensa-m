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
             <form id="post_form" enctype="multipart/form-data" @submit="add_post">
                <input type="hidden" name="club" v-model="club" />
                <input class="form-control" type="text" name="title" v-model="title" placeholder="title" />
                <textarea class="form-control" name="content" v-model="content" placeholder="content" ></textarea>
                <input type="file" id="file" name="pic" class="form-control" placeholder="" />
                <input class="btn btn-primary" type="submit" value="post" id="post">
            </form>
        </div>
    </div>
    `,
    data(){
        return {
            title: "kndlkfnlsdnfknsd",
            content: "wsllsvlslsldbjsbdfsldbflb",
            club: 'club informatique'
        }
    },
    methods: {
        add_post(e){

            e.preventDefault()

            var form = new FormData($('form')[0]);
            form.append('file', $('#file')[0].files[0]);
            

            $.ajax({
                url: "http://127.0.0.1:8000/post/0",
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
        hideModal(){
            $("#myModal").fadeOut()
        }
    }
})

app.mount("#app")