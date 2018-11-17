$(function () {
    var modifyDiv = $(".modifyDiv");
    modifyDiv.css("display", "none");
    $("#formAddress").css("display", "none");
    $(".addressSubmit").css("display", "none");
    $(".selectAddress").css("display", "none");

    $(".buttonModifyDiv").on("click", function () {
        var modifyDivThis = $(this).siblings(".modifyDiv");
        if (modifyDivThis.css("display") === "none") {
            modifyDivThis.css("display", "block");
            $(this).val("Zwiń")
        } else {
            modifyDivThis.css("display", "none");
            $(this).val("Rozwiń")
        }
    });
    $(".buttonSelectAddress").on("click", function () {
        $(".addressSubmit").css("display", "block");
        $(".selectAddress").css("display", "block");
        $("#formAddress").css("display", "none");
    });
    $(".buttonFormAddress").on("click", function () {
        $(".addressSubmit").css("display", "block");
        $(".selectAddress").css("display", "none");
        $("#formAddress").css("display", "block");
    });

    var popUpQuestion = function (event) {
        return window.confirm("Czy jesteś pewien że chcesz usunąć element?");
    };

    $(".deleteElement").on("click", popUpQuestion)
});