console.log('javascript connected')
var submitButton = document.querySelector('#submit')
var access_key = 'f1a30b3756b89cba8406fd2c5f64b3ee'

async function validate(num){
    var number = num
    var country_code = ''
    
    url = `http://apilayer.net/api/validate?access_key=${access_key}&number=${number}&country_code=${country_code}`
    
    // Please be aware that enabling format increases the API response's file size and might cause parsing problems. It should be used for debugging purposes only.
    // var format = 1
    // url += &format=${format}

    
    results = await fetch(url)
    json = await results.json()
    
    console.log(json)
    return json
}


function display_country_codes(){
    var phone_select = document.getElementById('country_code')

    console.log(`Country Codes: ${country_codes_data}`)
    
    for(const [key, value ] of Object.entries(country_codes_data)){
        
        var child = document.createElement('option')
        child.value = `${value.dialling_code}`
        child.innerHTML = `${value.country_name}`
        phone_select.append(child)
    }
}


display_country_codes()

