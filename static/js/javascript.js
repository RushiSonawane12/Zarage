$("input").on("change", function() {
    this.setAttribute(
        "data-date",
        moment(this.value, "DD-MM-YYYY")
        .format( this.getAttribute("data-date-format") )
    )
}).trigger("change")