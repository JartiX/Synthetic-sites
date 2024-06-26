function closeObjectCard() {
    document.getElementById('objectCard').style.display = 'none';
}

window.addEventListener('message', function (event) {
    if (event.data.type === 'selectLocation') {
        var id = event.data.id;
        var selectedObject = document.getElementById(id);
        if (selectedObject) {
            var objectContent = selectedObject.innerHTML;
            var objectCard = document.getElementById('objectCard');
            objectCard.querySelector('.object-content').innerHTML = objectContent;
            objectCard.style.display = 'block';
        }
    }
});