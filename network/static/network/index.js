function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

// JS для работы "Edit Post"
function save_edit(id){
    const textarea_value = document.getElementById(`textarea${id}`).value;
    const content = document.getElementById(`content_${id}`);
    const modal = document.getElementById(`edit_post_${id}`);
    // Получить изменяемые данные
    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            content: textarea_value
        })
    })
        .then(response => response.json())
        .then(result => {
            content.innerHTML = result.content;
            modal.style.display = "none";
        })
        // Костыль, перезагружает всю страницу
        location.reload();
}

