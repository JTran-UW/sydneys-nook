$(function() {
    $("#share-url").attr({
        value: window.location
    });
});

function showPopup() {
    $("#share-popup").css({
        display: "flex"
    });
}

function copyUrl() {
    let shareUrl = $("#share-url").val();
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareUrl).then(() => {
            alert("Link copied to clipboard");
        });
    } else {
        $("#share-url").select();
        document.execCommand('copy');
        alert("Link copied to clipboard")
    }
}

$(document).mouseup(function(e) 
{
    var container = $("#share-popup");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(e.target) && container.has(e.target).length === 0) 
    {
        container.hide();
    }
});
