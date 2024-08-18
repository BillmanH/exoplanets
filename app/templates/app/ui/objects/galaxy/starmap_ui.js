{% load static %}

icons = {
    exit:"{% static 'app/objects/icons/exit_icon.png' %}",
    system:"{% static 'app/objects/icons/system_icon_1.png' %}"
}

var exit_icon = create_icon({name:'quit_icon',tooltiptext:"Quit",image:icons.exit,top:getIconTop(0)})
var system_icon = create_icon({name:'system_icon',tooltiptext:"System",image:icons.system,top:getIconTop(1)})

exit_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/'
    console.log('quit to menu')
    window.location.href = dest;
});

system_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/homesystemui'
    console.log('quit to menu')
    window.location.href = dest;
});
