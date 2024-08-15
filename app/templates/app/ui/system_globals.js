
function flipper(){
    x = Math.random()
    if(x<=.5){
        return -1
    } else {
        return 1
    }
}

radius_p = get_values(data["nodes"],"radius", "planet")
radius_m = get_values(data["nodes"],"radius", "moon")
radiuses = radius_p.concat(radius_m)

var scale_radius = d3.scaleLinear()
            .domain([d3.min(radiuses),d3.max(radiuses)])
            .range([1,100]);
// console.log("radiuses: ", radiuses)   

distances = get_values(data["nodes"],"orbitsDistance", "planet")
// console.log("distances: ", distances)            
var scale_distance = d3.scaleSqrt()
            .domain([d3.min(distances),d3.max(distances)])
            .range([120,2000]);

var scale_distance_ln = d3.scaleLinear()
    .domain([d3.min(distances),d3.max(distances)])
    .range([2,5]);

var scale_jitter = d3.scaleLinear() 
            .domain([0,1])
            .range([10,30]);