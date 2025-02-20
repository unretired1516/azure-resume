windows.addEventListener('DOMContentLoaded', (event) => {
    getVisitCount();
})
const functionApiURL = ''
const functionApi = 'http://localhost:7071/api/VisitorCounter';
//Set variable to 0, call the API get the current count, then set the count variable to equal the response. Then display the count in the InnerText.
const getVisitCount = () => {
    let count = 0;
    fetch(functionApi).then(response => {
        return response.json()
    }).then(response => {
        console.log("Website called function API.");
        count = response.count;
        document.getElementById("counter").innerText = count;
    }).catch(function(error) {
        console.log(error)
    });
    return count;
}