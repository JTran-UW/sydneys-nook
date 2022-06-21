const openArticle = (elem) => { 
    // Get article text
    newUrl = window.location + "blog/" + elem.id
    fetch(newUrl)
    .then(response => response.json())
    .then(data => {
        document.getElementById("article-title").innerHTML = data["title"];
        document.getElementById("article-content").innerHTML = data["post"];

        // Show article
        expand(elem);

        // Change url and push to history
        history.pushState({}, "", newUrl);
    });
}
const closeArticle = () => {
    const box = document.getElementById("article");
    const post_id = window.location.pathname.split("/")[2]
    const post = document.getElementById(post_id)
    const holder = $(post).children(".post-tn")[0];

    // Get its position
    const pos = $(holder).position();

    // Hide contents
    $(box).children().animate({
        "opacity": 0
    }, 200);

    // Animate the box to contract
    setTimeout(() => {
        $(box).animate({
            "width": holder.offsetWidth + "px",
            "height": holder.offsetHeight + "px",
            "left": pos.left + "px",
            "top": pos.top + "px",
        }, 600)
    }, 200);

    // Lower box opacity
    setTimeout(() => {
        $(box).animate({
            "opacity": 0.2,
        }, 200)

        $(box).css({
            "width": "0px",
            "height": "0px",
        })
    }, 1400);

    // Change url
    window.history.back();
}

function expand(elem) {
    let box = document.getElementById("article");
    let holder = $(elem).children(".post-tn")[0]

    // Get and set its position
    let pos = $(holder).position();
    $(box).css({
        "left": pos.left + "px",
        "top": pos.top + "px",
        "width": holder.offsetWidth + "px",
        "height": holder.offsetHeight + "px",
    });

    // Show the box
    $(box).animate({
        "opacity": 0.92,
    }, 200);
    
    // Animate the box to expand
    setTimeout(() => {
        $(box).animate({
            "width": '100%',
            "height": '100%',
            "top": 0,
            "left": 0,
        }, 600);
    }, 200);
    
    // Reveal the article contents
    setTimeout(() => {
        $(box).children().animate({
            "opacity": "1"
        }, 200)
    }, 1400);
}
