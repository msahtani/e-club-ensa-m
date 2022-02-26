$(document).ready(()=> {
    $("#alert_wrapper").hide()
})
$('#login').click(
    (event) => {
        event.preventDefault()
        var _data = $("#login_form").serialize()
        $.ajax({
            url: "",
            type: "POST",
            data: _data, 
            success: (result) => {
                location.reload()

            },
            error:(err, status)=>{
                console.clear()
                console.log(status)
                $("#alert_msg").text(err.responseText)
                $("#alert_wrapper").show()
            }
        })
    }
)