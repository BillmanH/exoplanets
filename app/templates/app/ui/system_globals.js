
function flipper(){
    x = Math.random()
    if(x<=.5){
        return -1
    } else {
        return 1
    }
}

radiuses = get_values(solar_system["nodes"],"radius", "planet")
var scale_radius = d3.scaleLinear()
            .domain([d3.min(radiuses),d3.max(radiuses)])
            .range([10,100]);
// console.log("radiuses: ", radiuses)   

distances = get_values(solar_system["nodes"],"orbitsDistance", "planet")
// console.log("distances: ", distances)            
var scale_distance = d3.scaleSqrt()
            .domain([d3.min(distances),d3.max(distances)])
            .range([20,2000]);

var scale_distance_ln = d3.scaleLinear()
    .domain([d3.min(distances),d3.max(distances)])
    .range([2,5]);

var scale_jitter = d3.scaleLinear() 
            .domain([0,1])
            .range([10,30]);