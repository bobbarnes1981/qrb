jQuery(document).ready(function(){
    console.log("from the script");
    jQuery.ajax({
        url: "http://127.0.0.1:8081/api/v1/candidatetests/" + candidatetest_id
    }).done(function(data, textStatus, jqXHR){
        console.log(data);
    }).fail(function(jqXHR, textStatus, errorThrown){
        console.log("fail");
    });
});