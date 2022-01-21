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
                Swal.enableLoading()
                axios.post($(this).prop('href'), {}, {headers: {'X-CSRFToken': csrftoken}}).then(res=>{
                    $($(this).attr('data-target')).fadeOut(300, function() { $(this).remove(); });
                    console.log(res.status)
                }).catch(err=>{
                    console.log(err.response.status)
                    if(err.response.status==302){
                        window.location.href = err.response.data.redirect
                    }else{
                        Swal.fire({
                            html:err.data,
                            showConfirmButton: false
                        })
                    }
                }).finally(function(){
                    Swal.disableLoading()
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

    $('.btn-ajax-preview').click(function(e){
        e.preventDefault()
        Swal.enableLoading()
        axios.get($(this).prop('href')).then(function(res){
            Swal.fire({
                showConfirmButton: false,
                html:res.data,
                customClass: 'swal-pdf-preview',
            })
        }).catch(function(err){

        }).finally(function(){
            Swal.disableLoading()
        })
    })

    $('.btn-ajax-email').click(function(e){
        e.preventDefault()
        if(!$(this).hasClass('disabled')){
            $(this).addClass('disabled')
            $(this).html('<i class="fas fa-spinner fa-pulse"></i>')
            const csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
            axios.post($(this).prop('href'),{},{headers: {'X-CSRFToken': csrftoken}}).then(res=>{
                $(this).toggleClass('btn-outline-primary').toggleClass('btn-outline-success')
                $(this).html('<i class="fas fa-check"></i>')
            }).catch(err=>{
                $(this).toggleClass('btn-outline-danger').toggleClass('btn-outline-success')
                $(this).html('<i class="fas fa-exclamation-circle"></i>')
            })
        }
    })

    $('.btn-ajax-bulk-email').click(function(e){
        e.preventDefault()
       $(`[data-trigger=${$(this).attr('data-target')}]`).trigger( "click" )
    })
});