window.onload = function() {
    var delete_button = document.getElementById("delete_button");
    var confirm_dialog = document.getElementById("confirm_delete");

    // "Delete student" button opens up the <dialog> modal
    delete_button.addEventListener('click', function onOpen() {
        if (typeof confirm_dialog.showModal == "function") {
            confirm_dialog.showModal();
        }
        else {
            alert("The dialog API is not supported by this browser");
        }
    })
}