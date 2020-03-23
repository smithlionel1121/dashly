function revealMessage() {
    document.getElementById("hidden").style.display = 'block';
}

function countdown() {
    var currentVal = document.getElementById("countdownButton").innerHTML;
    if (currentVal > 0) {
        var newVal = currentVal - 1;
        document.getElementById("countdownButton").innerHTML = newVal;
    } else  {
        //var cret = document.createElement('p');
        var ccc = document.getElementById("made").innerText; //("");
        var ccd =  `${ccc} RELAX!`;
        document.getElementById("made").innerText = ccd;
        //cret.tagName = "created";
        //cret.textContent = 
        //document.getElementById("maker").append(cret);
    }
    //(method) Document.createElement<"p">(tagName: "p", options?: ElementCreationOptions): HTMLParagraphElement (+2 overloads)
};

$(document).ready(function() {
    $(".camo").hover(function() {
        $(this).css("color", "black");
    },
    function() {

    });
});

