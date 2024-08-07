{% load static %}

icons = {
    exit:"{% static 'app/objects/icons/exit_icon.png' %}"
}

var exit_icon = create_icon({name:'quit_icon',tooltiptext:"Quit",image:icons.exit,top:getIconTop(0)})
