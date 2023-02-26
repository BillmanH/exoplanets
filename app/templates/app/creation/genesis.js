
// NOTE: These just affect the UI in the creator. This does not affect the actual genesis limits.
planets_min = 3
planets_max = 10

moons_min = 15
moons_max = 30

pop_min = 2
pop_max = 15

var form = {
    "label":"form",
    "name":"worldgenform",
    "objid":Math.floor(Math.random()*10000000000000),  // 13 char GUID
    "owner":"{{ user.username }}",
    "username": "{{ user.username }}",
    "accountid":account.objid,
    "conformity":.5,
    "literacy":.5,
    "aggression":.5,
    "constitution":.5
    }


function add_menu(t,c) {
    var menu = document.createElement("p")
    menu.className += "guimenu"
    menu.id = c
    var text = document.createTextNode(t);
    menu.appendChild(text);
    document.body.insertBefore(menu, document.getElementById("startmenu"));
}

function add_please_wait(){
    var plzwt = document.createElement("p")
    plzwt.id = "loading"
    var text = document.createTextNode(" Please Wait, while the system is loading ... ");
    plzwt.appendChild(text);
    document.body.insertBefore(plzwt, document.getElementById("startmenu"));
}

function add_button(c,n,t,f) {
    // id of parent, n = iteration number, text, onlcick funtion
  var button = document.createElement("div")
    button.className += "menu button";
    button.id = c + "_" + n;
  var text = document.createTextNode(t.toString());
  
  button.appendChild(text);
  document.getElementById(c).appendChild(button);  
  button.onclick = function(){f(c,n)}
}


function add_slider(c,n){
    var p = document.createElement("p")
    var text = document.createTextNode(n);
    var slider = document.createElement("input")
    p.appendChild(text);
    document.getElementById(c).appendChild(p);  
    slider.type="range"
    slider.min="1"
    slider.max="100"
    slider.value="50"
    slider.className = "slider"
    slider.id = n
    slider.oninput = function() {
        form[n] = this.value/100;
        population_form_check()
      }
    document.getElementById(c).appendChild(slider);  
}


var mark_system_checked = function(c,n){
    var parent = document.querySelector("#"+c);
    var allChildElements = parent.querySelectorAll('.button');

    for(i=0; i < allChildElements.length ; i++){
        allChildElements[i].style.color = "whitesmoke"
        allChildElements[i].style.backgroundColor = "#2d2d2d"
    }

    form[c] = n
    selected = document.getElementById(c + "_" + n)
    console.log(selected)
    selected.style.color = "black";
    selected.style.backgroundColor = "whitesmoke"

    if ((form.hasOwnProperty("num_planets"))&(form.hasOwnProperty("num_moons"))){
        d3.selectAll('#createsystem').remove()
        add_menu("Create this solar system", "createsystem")
        add_button("createsystem",1,"create", build_solar_system)
    }
}

var mark_population_checked = function(c,n){
    var parent = document.querySelector("#"+c);
    var allChildElements = parent.querySelectorAll('.button');

    for(i=0; i < allChildElements.length ; i++){
        allChildElements[i].style.color = "whitesmoke"
        allChildElements[i].style.backgroundColor = "#2d2d2d"
    }

    form[c] = n
    selected = document.getElementById(c + "_" + n)
    console.log(selected)
    selected.style.color = "black";
    selected.style.backgroundColor = "whitesmoke"

    population_form_check()
}

function population_form_check(){
    if ((form.hasOwnProperty("starting_pop"))
        &(form.hasOwnProperty("conformity"))
        &(form.hasOwnProperty("literacy"))
        &(form.hasOwnProperty("aggression"))
        &(form.hasOwnProperty("constitution"))
        ){
            d3.selectAll('#createpeople').remove()
            add_menu("let these people flourish", "createpeople")
            add_button("createpeople",1,"create", build_population)
        }
}



function add_p(i,n) {
    var p = document.createElement("p")       
    var text = document.createTextNode(n);
    p.appendChild(text);
    document.getElementById(i).appendChild(p);  
  }
  

add_menu("Your account:", "accountinfo")
add_p("accountinfo", "Your account type is: " + account.type)
add_p("accountinfo","created: " + account.created)
add_p("accountinfo","last used: "+account.last_used)

function back_to_home(c,n){
    window.location.href = '/';
}

function delete_existing_game(c,n) {
    $.ajax({
        url: '/ajax/refreshaccount',
        type: 'get',
        data: form,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#accountinfo').remove()
            add_please_wait()
        },
        success: function(data){
            cnsl(data)
            d3.selectAll('#loading').remove()
            form_solar_system()
        }
    });
}

function build_solar_system(c,n) {
    $.ajax({
        url: '/ajax/genesissystem',
        type: 'get',
        data: form,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#num_planets').remove()
            d3.selectAll('#num_moons').remove()
            d3.selectAll('#createsystem').remove()
            add_please_wait()
        },
        success: function(data){
            var solar_system = data.solar_system
            {% include "app/charts/solar_system.js" %}
            form_population()
            form_people_culture()
            d3.selectAll('#loading').remove()
        }
    });
}

if(account.type=="pre_beta_account"){
    add_p("accountinfo","your account requires that you can only have one account open at a time. Do you want to delete your old game and start over?")
    add_button("accountinfo",1,"delete everything, start over", delete_existing_game)
    add_button("accountinfo",2,"return to the main menu", back_to_home)
}

function form_solar_system(){
    // TODO: Create text field to allow user to name planet (`planet_name`)
    add_menu("Choose the number of planets in your system, 6 is average.", "num_planets")
    add_menu("... and choose the number of moons, 24 is average. They will be spread across the whole system", "num_moons")

    for (i=planets_min;i<=planets_max;i++){
        add_button("num_planets",i,i, mark_system_checked)
    }

    for (i=moons_min;i<=moons_max;i++){
        add_button("num_moons",i,i, mark_system_checked)
    }
}

function form_population(){
    add_menu("Against all odds, a species on this planet has risen out of the muck and begun to form a culture.", "starting_pop")
    add_p("starting_pop","Choose your starting population")
    for (i=pop_min;i<=pop_max;i++){
        add_button("starting_pop",i,i, mark_population_checked)
    }    
}

function form_people_culture(){
    add_menu("That species has established a culture that enables them to thrive.", "home_world")
    add_p("home_world","Choose the starting attributes of your people. Each attribute has both advantages and disadvantages.")
    add_slider("home_world","conformity")
    add_slider("home_world","literacy")
    add_slider("home_world","aggression")
    add_slider("home_world","constitution")
}

function build_population(c,n) {
    $.ajax({
        url: '/ajax/genesispopulation',
        type: 'get',
        data: form,
        dataType: 'json',
        beforeSend: function () {
            d3.selectAll('#home_world').remove()
            d3.selectAll('#starting_pop').remove()
            d3.selectAll('#createpeople').remove()
            add_please_wait()
        },
        success: function (data) {
            console.log("pops, were created")
            if ("pops" in data) {
                draw_table(
                    "peopleTable",
                    data['pops'],
                    pop_table_lables
                )
                console.log(data['factions'])
                draw_table(
                    "FactionTable",
                    data['factions'],
                    faction_table_lables
                )
            }
            finalize_world()
            d3.selectAll('#loading').remove()
        }
    });
}

function goto_system(c,n){
            window.location.href = '/homesystemui';
}


function finalize_world(){
    add_menu("Feel free to click around, but the game hasn't started yet.", "finalize")
    add_button("finalize",1,"continue to the game", goto_system)
}

// An example `data` set:
// data = {
//     "planet_name": "Earth",
//     "num_planets": "6",
//     "num_moons": "24",
//     "home_has_moons": "on",
//     "starting_pop": "7",
//     "conformity": "0.3",
//     "literacy": "0.7",
//     "aggression": "0.5",
//     "constitution": "0.5",
//     "name": "form",
//     "objid": "4864559553238",
//     "username": "Billmanh",
//     "objtype": "form",
//     "id": "4864559553238",
// }
