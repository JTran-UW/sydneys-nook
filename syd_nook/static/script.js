const delay = 250;
const duration = 1000;
const leftFr = 7;
const rightFr = 6;
const screenRatio = leftFr * 100 / (leftFr + rightFr);

$(function() {
    // Set screen ratio
    $("body").css({
        "grid-template-columns": leftFr + "fr " + rightFr + "fr" 
    });

    // Fetch articles and put them in the DOM, then show everything
    loadLinks(0, 10).then(() => {
        const postChildren = $("#post").children();
        revealElems($("body"));
        revealElems(postChildren);
    });
});

function loadLinks(start_index, end_index) {
    return new Promise((resolve, reject) => {

        // Get all articles
        fetch(window.location + "blog/blurb/" + start_index + "-" + end_index)
        .then(response => response.json())
        .then(articles => {
            for (let i = 0; i < articles.length; i++)
            {
                let a = articles[i];
                
                // Create card wrapper
                let card = $("<div>").attr({
                    onclick: "javascript: loadPost(this)",
                    id: a.id
                }).addClass("bordered post-link");
                
                // Create header
                let date = new Date(a.date_edited);
                let header = $("<section>").addClass("post-link-header");
                header.append($("<h2>").addClass("post-link-title").html(a.title));
                header.append($("<p>").addClass("young-serif").html(date.toDateString()));
                card.append(header);

                // Add thumbnail
                card.append(
                    $("<div>").addClass("post-link-tn").css({
                        "background-image": "url(" + a.thumbnail + ")"
                    }).append(
                        $("<p>").html(a.peek)
                    )
                );
                
                // Append it to the links
                $("#post-links").append(card);
            }
            resolve(); // Resolve promise
        });
    })
}

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
        let elem = elems[i];
        $(elem).stop().css({
            "opacity": 0,
        });

        $(elems[i]).delay(delay * i).animate({
            "opacity": 1,
        }, duration);
    }
}

function expandPost(button) {
    // Make other links unclickable
    $("#post-links").css({
        "pointer-events": "none",
    });

    // Change button properties
    $(button).removeAttr("onclick");
    let icon = $(button).children()[0];
    $(icon).removeClass("gg-arrows-expand-left").addClass("gg-minimize-alt");

    // Animate the post wrapper to fill the screen
    let post = $("#post");
    let postClone = post.clone();
    postClone.attr("id", "post-clone");
    postClone.prependTo("body");
    post.css({
        "position": "absolute",
        "z-index": 99,
        "width": screenRatio + "vw",
        "height": "100%"
    });
    post.animate({
        "width": "100%",
    }, 800);

    // Remove content of clone for wrapping issues
    $("#post-content").html("");

    $(button).attr("onclick", "javascript: closePost(this);");
}

function closePost(button) {
    // Change button properties
    $(button).removeAttr("onclick");
    let icon = $(button).children()[0];
    $(icon).removeClass("gg-minimize-alt").addClass("gg-arrows-expand-left");

    let delay = 800;
    let post = $("#post");
    post.animate({
        "width": screenRatio + "vw",
    }, delay);
    setTimeout(() => {
        post.css({
            "position": "relative",
            "height": "auto",
        });
        $("#post-clone").remove();
        
        // Reset button click listener
        $(button).attr("onclick", "javascript: expandPost(this);");
    
        // Reset post links
        $("#post-links").css({
            "pointer-events": "auto",
        });
    }, delay);
}
