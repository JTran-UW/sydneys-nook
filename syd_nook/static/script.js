const delay = 250;
const duration = 1000;

$(function() {
    const postChildren = $("#post").children();
    revealElems(postChildren);
});

function loadPost(postLinkElem) {
    // Get content
    fetch(window.location + "blog/content/" + postLinkElem.id)
        .then(response => response.json())
        .then(data => {
            const bodyChildren = $("#post-body").children();
            bodyChildren.css({
                "opacity": 0,
            });

            let date = new Date(data["date_edited"]);
            let dateString = date.toDateString();

            // Put this data in the blog
            $("#post-title").html(data["title"]);
            $("#post-date").html(dateString);
            $("#post-content").html(data["post"])

            revealElems(bodyChildren);
        });
}

function revealElems(elems) {
    for (let i = 0; i < elems.length; i++)
    {
        $(elems[i]).delay(delay * i).animate({
            "opacity": 1,
        }, duration);
    }
}

expandPost = (button) => {
    // Change button properties
    $(button).removeAttr("onclick");
    $(button).removeClass("gg-arrows-expand-left").addClass("gg-minimize-alt");

    let post = $("#post-wrapper");
    let postClone = post.clone();
    postClone.attr("id", "post-clone");
    postClone.prependTo("body");
    post.css({
        "position": "absolute",
        "z-index": 99,
        "width": "50vw",
        "height": "100%"
    });
    post.animate({
        "width": "100vw",
    }, 1000);

    // Remove content of clone for wrapping issues
    $("#post-content").html("");

    $(button).attr("onclick", "javascript: closePost(this);");
}

closePost = (button) => {
    // Change button properties
    $(button).removeAttr("onclick");
    $(button).removeClass("gg-minimize-alt").addClass("gg-arrows-expand-left");

    let post = $("#post-wrapper");
    $("#post-clone").remove();
    post.animate({
        "width": "50vw",
    }, 1000);
    post.css({
        "position": "relative"
    });

    $(button).attr("onclick", "javascript: expandPost(this);");
}
