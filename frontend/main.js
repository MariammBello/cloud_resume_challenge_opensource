
window.addEventListener('DOMContentLoaded', (event) =>{
    getVisitCount();
})
const backendApiUrl = 'http://127.0.0.1:5000/GetResumeCounter';

const getVisitCount = () => {
    let count = 30;
    fetch(backendApiUrl).then(response => {
        return response.json()
    }).then(response => {
        console.log ("Website called flaskapi");
        count =response.count;
        document.getElementById("counter").innerText =count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}

console.log("I got here")