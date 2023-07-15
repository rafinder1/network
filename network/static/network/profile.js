document.addEventListener('DOMContentLoaded', function () {

    follow_btn();

})

function follow_btn() {
    const follow_btn = document.querySelector('#follow_btn');
    const unfollow_btn = document.querySelector('#unfollow_btn');
    let name = document.querySelector('._name').innerHTML

    fetch(`is_follow/${name}`)
        .then(response => response.json())
        .then(status => {
            if (status.status) {
                follow_btn.style.display = 'none'
                unfollow_btn.style.display = 'block'
            }
            else {
                follow_btn.style.display = 'block'
                unfollow_btn.style.display = 'none'
                console.log("false")
            }
        })



    unfollow_btn.addEventListener('click', () => {
        console.log('unfollow_btn')
        fetch(`/profile/${name}/follow`, {
                method: 'PUT',
                body: JSON.stringify({
                    follow: false
                })
            }
        )
        .then(() => {
            unfollow_btn.style.display = 'none'
            follow_btn.style.display = 'block'
            count()
        })
    })

    follow_btn.addEventListener('click', () => {
        console.log('follow_btn')
        fetch(`/profile/${name}/follow`, {
                method: 'PUT',
                body: JSON.stringify({
                    follow: true
                })
            }
        )
        .then(() => {
            unfollow_btn.style.display = 'block'
            follow_btn.style.display = 'none'
            count()
        })
    })

}

function count() {
    let name = document.querySelector('._name').innerHTML

    fetch(`count/${name}`)
    .then(response => response.json())
    .then(data => {
        let followers = data.followers
        let following = data.following
        document.querySelector('#followers_count').innerHTML = `${followers} Followers`
        document.querySelector('#following_count').innerHTML = `${following} Following`
    })
}

