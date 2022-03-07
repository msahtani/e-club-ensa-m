$(document).ready(()=> {
    $("#alert_wrapper").hide()
})
$('#post').click(
    (event) => {
        event.preventDefault()
        var _data = $("#post_form").serialize()
        $.ajax({
            url: "http",
            type: "POST",
            data: _data, 
            success: (result) => {
                //location.reload()
                console.log("success !!!")
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