document.addEventListener('DOMContentLoaded', function(){ // Аналог $(document).ready(function(){
    document.querySelectorAll('.mark-viewed').forEach(btn => btn.addEventListener('click', e => {
            let postId = e.currentTarget.dataset.postId
            fetch(`posts/${postId}/view/`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'patch'
            })
            .then(() => document.location.reload())
        })
    )

    document.querySelectorAll('.unmark-viewed').forEach(btn => btn.addEventListener('click', e => {
            let postId = e.currentTarget.dataset.postId
            fetch(`posts/${postId}/unview/`, {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                method: 'patch'
            })
            .then(() => document.location.reload())
        })
    )
});