$(document).ready(function(){
    axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $('.enable-edit-form').click(function(){
        $(this).hide()
        $($(`${$(this).attr('data-target')} > fieldset`)).prop("disabled", false)
    })

    $('.btn-ajax-delete').click(function(e){
        e.preventDefault()
        Swal.fire({
            icon: 'warning',
            text: $(this).attr('data-message'),
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Supprimer',
            cancelButtonText: 'Annuler',
        }).then(result=>{
            if(result.isConfirmed){
                const csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
                axios.post($(this).prop('href'), {}, {headers: {'X-CSRFToken': csrftoken}}).then(res=>{
                    $($(this).attr('data-target')).fadeOut(300, function() { $(this).remove(); });
                }).catch(err=>{
                    Swal.fire({
                        html:err.data,
                        showConfirmButton: false
                    })
                })
            }
        })
    })

    $('.btn-ajax-form').click(function(e){
        e.preventDefault()
        axios.get($(this).prop('href'))
        .then(function(res){
            Swal.fire({
                html:res.data,
                showConfirmButton: false
            })
        }).catch(function(err){
            console.log(err)
        }).finally(function(){
            $('.ajax-form').submit(function(e){
                e.preventDefault()
                const csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
                Swal.enableLoading()
                axios.post(e.target.action, $(this).serialize(), {headers: {'X-CSRFToken': csrftoken}}).then(res=>{
                    $('.ajax-form').html(res.data);
                }).catch(err=>{
                    if(err.response.status==302){
                        window.location.href = err.response.data.redirect
                    }else{
                        $('.ajax-form').html(err.response.data);
                    }
                }).finally(function(){
                    Swal.disableLoading()
                })
            })
        })
    })

});