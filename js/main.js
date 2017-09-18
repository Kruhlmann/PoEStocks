{currencies}

function search_results_to_html(results){
    html = "";
    if(results.length == 0) return '<a href="#"><li class="result result-final"><span>No results found</span></li></a>';
    for(var i = 0; i < results.length; i++){
        html += '<a href="#"><li class="result result-final"><img src="../img/currency/' + currencies[results[i]]["name"] + '.png"></img><span>' + currencies[results[i]]["display_name"] + '</span></li></a>'
    }
    return html;
}

function populate_search_results(query){
    currencies.sort(compare_currency);
    results = [];
    for(var i = 0; i < currencies.length; i++){
        if(currencies[i]["name"].indexOf(query) !== -1 || query == ""){
            results.push(i);
            if(results.length >= 3){
                document.getElementById("results").innerHTML = search_results_to_html(results)
                return
            }
        }
    }
    document.getElementById("results").innerHTML = search_results_to_html(results)
}

function compare_currency(a, b) {
  if (a.name < b.name)
    return -1;
  if (a.name > b.name)
    return 1;
  return 0;
}


// INIT
populate_search_results("")