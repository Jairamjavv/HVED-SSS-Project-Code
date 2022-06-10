function decryptFile(){
    fetch('/decryptFile', {
        method: 'POST'
    }).then((_res) => {
        window.location.href="/decryptFile"
    })
}