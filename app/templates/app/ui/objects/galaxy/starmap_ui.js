{% load static %}

icons = {
    exit:"{% static 'app/objects/icons/exit_icon.png' %}"
}

var exit_icon = create_icon({name:'quit_icon',tooltiptext:"Quit",image:icons.exit,top:getIconTop(0)})


exit_icon.onPointerClickObservable.add(function () {
    dropAllControls()
    plz = pleaseWaiter(dashboard)
    dest = '/'
    console.log('quit to menu')
    window.location.href = dest;
});
