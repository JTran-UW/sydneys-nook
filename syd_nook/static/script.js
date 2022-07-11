const delay = 250;
const duration = 1000;
const leftFr = 6;
const rightFr = 5;
const screenRatio = leftFr * 100 / (leftFr + rightFr);

let queryRequestString = "";

let maxArticlesReached = false;
let startArticleIndex = 0;
const articleLoadNum = 5;

$(function() {
    // Set screen ratio
    $("body").css({
        "grid-template-columns": leftFr + "fr " + rightFr + "fr" 
    });

    // Fetch articles and put them in the DOM, then show everything
    loadLinks(startArticleIndex, startArticleIndex + articleLoadNum).then(() => {
        revealElems($("body"));
        revealElems($("#post").children());
    });
});

function checkScroll(e) {
    let links = $(e)
    let reachedTop = links[0].scrollHeight - links.scrollTop() === links.outerHeight();

    if (reachedTop && !maxArticlesReached) {
        startArticleIndex += articleLoadNum;

        loadLinks(startArticleIndex, startArticleIndex + articleLoadNum);
    }
}

function loadLinks(start_index, end_index) {
    return new Promise((resolve, reject) => {

        // Get all articles
        fetch(window.location + "blog/blurb/" + start_index + "-" + end_index + "?query=" + queryRequestString)
        .then(response => response.json())
        .then(data => {
            // Update max articles reached
            maxArticlesReached = data["maxReached"];

            articles = data["blurbs"];
            let cards = [];
            for (let i = 0; i < articles.length; i++)
            {
                let a = articles[i];
                
                // Create card wrapper
                let card = createCard(a.id, a.date_edited, a.title, a.thumbnail, a.peek);

                // Append it to the links
                $("#post-links").append(card);
                cards.push(card);
            }
            revealElems(cards);
            resolve(data); // Resolve promise
        });
    });
}

function createCard(id, dateEdited, title, thumbnail, peek) {
    // Create card wrapper
    let card = $("<div>").attr({
        onclick: "javascript: loadPostPage(this);",
        id: id
    }).addClass("bordered post-link");
    
    // Create header
    let date = new Date(dateEdited);
    let dateString = date.toLocaleDateString("en-us", {
        month: "long",
        day: "numeric",
        year: "numeric"
    })
    let header = $("<section>").addClass("post-link-header");
    header.append($("<h2>").addClass("post-link-title").html(title));
    header.append($("<p>").addClass("young-serif").html(dateString));
    card.append(header);

    // Add thumbnail
    card.append(
        $("<div>").addClass("post-link-tn").css({
            "background-image": "url(" + thumbnail + ")"
        }).append(
            $("<p>").html(peek)
        )
    );

    return card;
}

function loadPostPage(elem) {
    window.location = "blog/" + elem.id;
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

$(document).on("keypress", "#search-bar", function(e) {
    if (e.which == 13)
    {
        loadQuery();
    }
});

function loadQuery() {
    $(".post-link").remove();
    queryRequestString = $("#search-bar").val();
    loadLinks(0, 5);
}
