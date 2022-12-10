function get_values(l,v,t){
    /// l = list; v = value to return; t = type to filter on; 
    var mylist = []
    for (let i = 0; i < l.length; i++){
        if(l[i][v]!=undefined & l[i]["objtype"]==t){
            mylist.push(l[i][v])
        }
    } 
    return mylist
}

radiuses = get_values(solar_system["nodes"],"radius", "planet")
var scale_radius = d3.scaleLinear()
            .domain([d3.min(radiuses),d3.max(radiuses)])
            .range([10,100]);
console.log("radiuses: ", radiuses)   

distances = get_values(solar_system["nodes"],"orbitsDistance", "planet")
console.log("distances: ", distances)            
var scale_distance = d3.scaleSymlog()
            .constant(0.1)    
            .domain([d3.min(distances),d3.max(distances)])
            .range([20,2000]);

var scale_jitter = d3.scaleLinear() 
            .domain([0,1])
            .range([100,200]);