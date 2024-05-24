
// NOTE: These just affect the UI in the creator. This does not affect the actual genesis limits.
pop_min = 2
pop_max = 15

var form = {
    "label":"form",
    "name":"worldgenform",
    "objid":Math.floor(Math.random()*10000000000000),  // 13 char GUID
    "owner":"{{ account.username }}",
    "userguid":"{{ account.userguid }}",
    "username": "{{ account.username }}",
    "accountid":account.objid,
    "conformity":.5,
    "constitution":.5,
    "literacy":.5,
    "aggression":.5,
    "num_planets": 4,
    "num_moons": 10,
    "starting_pop":7,
    "organics":.5,
    "minerals":.5,
    "consumes":"organics",
    "effuses":"organic waste,plastics"
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



function add_duality_slider(c,n1,n2){
    // n1 = duality 1; n2 = duality 2
    // c = document id to place it
    var div = document.createElement("div")
    var p1 = document.createElement("p")
    var p2 = document.createElement("p")
    var p3 = document.createElement("p")
    var textn1 = document.createTextNode(n1);
    var textn2 = document.createTextNode(n2);
    p1.id = n1+"_text"
    p2.id = n2+"_text"
    var slider = document.createElement("input")
    p1.appendChild(textn1);
    p2.appendChild(textn2);
    p3.appendChild(slider);
    div.appendChild(p1);
    div.appendChild(p2);
    div.appendChild(p3);
    document.getElementById(c).appendChild(div); 
    slider.type="range"
    slider.min="1"
    slider.max="100"
    slider.value="50"
    slider.className = "slider"
    slider.id = n1+"-"+n2
    slider.oninput = function() {
        form[n1] = (this.value/100).toFixed(3);
        form[n2] = (1-(this.value/100)).toFixed(3);
        document.getElementById(n1+"_text").innerText = n1 + ": "+ form[n1] 
        document.getElementById(n2+"_text").innerText = n2 + ": "+ form[n2]
      }
    document.getElementById(c).appendChild(div);  
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
add_p("accountinfo","Owner: "+account.username)

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
        },
        error: function(xhr, status, error) {
            console.log(xhr.status + ': ' + xhr.statusText);
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
            d3.selectAll('#starting_homeworld').remove()
            add_please_wait()
        },
        success: function(data){
            var data = data.solar_system
            cnsl(data.status,data.note)
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
    add_menu("Choose the nature of your homeworld." , "starting_homeworld")
    add_p("starting_homeworld","Organic materials will sustain your population in the beginning, minerals will help your population later.")
    add_duality_slider("starting_homeworld","organics","minerals")
    add_button("starting_homeworld",1,"Build solar system, and homeworld", build_solar_system)
}

function form_population(){
    add_menu("Against all odds, a species on this planet has risen out of the muck and begun to form a culture.", "starting_pop")
}

function form_people_culture(){
    add_menu("That species has established a culture that enables them to thrive.", "home_population")
    add_p("home_population","Choose the starting attributes of your people. Each attribute has both advantages and disadvantages.")
    add_duality_slider("home_population","conformity","constitution")
    add_duality_slider("home_population","literacy","aggression")
    add_button("home_population",1,"Let the people evolve.", build_population)
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
                console.log('homeworld id:', data.homeworldid)
                draw_table(
                    "FactionTable",
                    data['factions'],
                    faction_table_lables
                )
            }
            finalize_world(data)
            d3.selectAll('#loading').remove()
        }
    });
}

function goto_system(data){
            window.location.href = '/popuilocal?objid='+ data.homeworldid;
}


function finalize_world(data){
    add_menu("Feel free to click around, but the game hasn't started yet.", "finalize")
    add_button("finalize",1,"continue to the game", goto_system(data))
}

