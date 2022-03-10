const validateEmail = (email) => {
    if(!email.includes('@'))
        return false
    
    var index = email.indexOf('@')
    return email.includes('.', index)
}

const validatePassword = (pass, rpass) => {
    if (pass.lenght == 0) return false

    return pass == rpass
}

var app = Vue.createApp({
    data(){
        return{
            firstname: "",
            lastname: "",
            email: "",
            password:  "",
            rpassword: "",

            disbled: true
        }
    },
    methods: {
       signup(e){
            e.preventDefault()
            $.ajax({
                url: window.location.href,
                type: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                data: $("#signup_form").serialize(),
                success(result){
                    console.log(result)
                }
            })
        },
        validate(){
            var vFname = this.firstname.length != 0
            var vLname = this.lastname.length != 0
            var vEmail = validateEmail(this.email)
            var vPass = validatePassword(this.password, this.rpassword)

            this.disbled = !(vFname && vLname && vEmail && vPass)
        }
    }
})

app.mount("#app")
