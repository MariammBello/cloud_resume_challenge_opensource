
window.addEventListener('DOMContentLoaded', (event) =>{
    getVisitCount();
})
const backendApiUrl = 'https://sheac-api.hostspacecloud.com/GetResumeCounter'
const localFunctionApi = 'http://localhost:5000/GetResumeCounter';

const getVisitCount = () => {
    let count = 30;
    fetch(backendApiUrl).then(response => {
        return response.json()
    }).then(response => {
        console.log ("Website called function Api");
        count =response.count;
        document.getElementById("counter").innerText =count;
    }).catch(function(error){
        console.log(error);
    });
    return count;
}

