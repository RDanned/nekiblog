document.addEventListener('DOMContentLoaded', function(){ // Аналог $(document).ready(function(){
    document.querySelector('.mark-viewed').addEventListener('click', e => {
        let postId = e.target.dataset.postId
        fetch(`posts/${postId}/view/`, {
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            method: 'patch'
        })
            .then(() => console.log('viewd'))
    })
});