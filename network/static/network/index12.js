document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#compose-post').onsubmit = compose_submit;

    document.querySelectorAll('.edit_post').forEach(btn => {
        btn.onclick = function() {
            const postId = this.dataset.postId;
            enterEditMode(postId);
        };
    });

    document.querySelectorAll('.liker').forEach(post => {
        post.onclick = function() {
            const postId = this.dataset.postId;
            likes(postId);
        };
    });
});


function compose_submit() {
    const compose_post = document.querySelector('#post-text').value;
    console.log(compose_post);

    fetch('/compose_post', {
        method: 'POST',
        body: JSON.stringify({
            subject: compose_post
        })
    })
//    load_posts();
    document.querySelector('#post-text') = ''
    return false;
}

function enterEditMode(postId) {
    text = document.querySelector(`.text-${postId}`)
    content = text.innerHTML
    edit_btn = document.querySelector(`.edit_post-${postId}`)
    edit_btn.style.display = 'none';

    console.log(text)
    console.log(content)
    text.innerHTML = `
    <form>
        <div>
        <textarea id='edited_text' name='edit-input'>${content}</textarea>
        </div>
        <div>
        <button type='button' class='btn btn-success' id='edit-post-form-${postId}'>Save Post</button>
        </div>
    </form>
    `

    document.querySelector(`#edit-post-form-${postId}`).onclick = () => {
        save_post(postId)
    }
}


function save_post(postId) {
    let edited_post = document.querySelector('#edited_text').value

    fetch(`edited_post/${postId}`, {
        method: 'POST',
        body: JSON.stringify({
            update_post_content: edited_post
        })
    })
    .then(
        text.innerHTML = edited_post
    )
    .then(
        edit_btn.style.display = 'block'
    )
}

function likes(postId) {
    let liker = document.querySelector(`#liker-${postId}`);
    let likes_count = document.querySelector(`#num-${postId}`);

    if (liker.classList.contains('added')) {
        fetch(`likes/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
                like: false
            })
        })
        .then(() => {
            console.log("delete like")
            likes_count.textContent--;
        })
    }
    else {
        fetch(`likes/${postId}`, {
            method: 'POST',
            body: JSON.stringify({
                like: true
            })
        })
        .then(() => {
            console.log("add like")
            likes_count.textContent++;
        })
    }
    liker.classList.toggle('added');
}