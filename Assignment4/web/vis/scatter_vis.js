class ScatterVis {

    constructor(data, html_root, dimensions) {
        this.data = this.transformData(data)
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.x = null
        this.y = null
        this.color = null
        this.xAxis = null
        this.yAxis = null
        this.plot_function = null
        this.lasso = null

        this.color_by = "sex"

        this.init()
    }

    transformData(data) {
        
        const pca_data = data.map(d => {
            return [
                d.sex == "F" ? 1 : 0,
                parseInt(d.age), 
                //d.address == "U" ? 1 : 0,
                //d.famsize == "GT3" ? 1 : 0,
                //parseInt(d.Medu), 
                //parseInt(d.Fedu),
                //parseInt(d.studytime),
                //parseInt(d.failures), 
                //d.romantic == "yes" ? 1 : 0,
                //parseInt(d.freetime), 
                parseInt(d.goout),
                parseInt(d.Dalc), 
                parseInt(d.Walc), 
                parseInt(d.health), 
                //parseInt(d.absences), 
                //parseInt(d.G1), 
                //parseInt(d.G2), 
                parseInt(d.G3), 
            ];
        })

        const pca = new ML.PCA(pca_data, {
            method: 'NIPALS',
            nCompNIPALS: 2,
            scale: true
        });
        const pca_predict = pca.predict(pca_data);

        return pca_predict.data.map((d, i) => {
            return {
                row: data[i],
                //x: d[d.length - 2],
                //y: d[d.length - 1],
                x: d[0],
                y: d[1],
            }
        })
    }

    init() {
        // Clear the tag
        d3.select(this.html_root + " > *").remove()

        // Add new items
        var svg = d3.select(this.html_root)
        .append('svg')
            .attr('width', this.width + this.margin.left + this.margin.right)
            .attr('height', this.height + this.margin.top + this.margin.bottom) 

        var view = svg.append("g")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")")
    
    
        //scale functions
        this.x = d3.scaleLinear()
            .domain([d3.min(this.data, d => d.x), d3.max(this.data, d => d.x)])
            .range([0, this.width])
            
        this.y = d3.scaleLinear()
            .domain([d3.min(this.data, d => d.y), d3.max(this.data, d => d.y)])
            .range([this.height, 0])

        this.color = d3.scaleOrdinal()
            .domain(this.data.map(d => {
                return d.row[this.color_by];
            }))
            .range(d3.schemeTableau10)

        //axis
        this.xAxis = d3.axisBottom(this.x)
        this.yAxis = d3.axisLeft(this.y)
            
        // create a scatter plot
        var dots = view.selectAll(".dot")
            .data(this.data)
            .enter()
            .append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .attr("fill", d => { return this.color(d.row[this.color_by]) })
            .attr("opacity", "0.5")
            .attr("cx", d => { return this.x(d.x) })
            .attr("cy", d => { return this.y(d.y) })
    
    
        // x axis
        view.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + this.height + ")")
            .call(this.xAxis)
            .append("text")
            .attr("fill", "#000")
            .attr("x", this.width / 2 )
            .attr("y", 75)
            .attr("text-anchor", "mid")
            .text("PC1")

        // y axis
        view.append("g")
            .attr("class", "y axis")
            .call(this.yAxis)
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            .attr("x", -this.height / 2)
            .attr("y", -75)
            .attr("text-anchor", "mid")
            .text("PC2")

        // legend
        view.append("text")
            .attr("transform", "translate(25, 5)")
            .text(this.color_by.toUpperCase())

        var legend = view.selectAll(".legend")
            .data(this.color.domain().sort())
            .enter()
            .append("g")
            .attr("class", "legend")
            .attr("transform", (d, i) => {
                return "translate(" + 30 + ", " + (30+(i * 25)) + ")"
            })
            

        legend.append("circle")
            .attr("r", 5)
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("fill", this.color)
            
        legend.append("text")
            .attr("x", 5 + 10)
            .attr("y", 5)
            .text(d => { return d })

        // lasso
        this.lasso = d3.lasso()
            .closePathSelect(true)
            .closePathDistance(100)
            .items(dots)
            .targetArea(svg)
            .on("start", () => { this.lassoStart() })
            .on("draw", () => { this.lassoDraw() })
            .on("end", () => { this.lassoEnd() })
    
        svg.call(this.lasso)
    }

    update(data) {
        
        if (data != null)
            this.data = this.transformData(data)

        
    }

    lassoStart() {
        this.lasso.items()
            .attr("r",3.5) // reset size
    }

    lassoDraw() {
        // Style the possible dots
        this.lasso.possibleItems()
            .classed("not_possible",false)
            .classed("possible",true)

        // Style the not possible dot
        this.lasso.notPossibleItems()
            .classed("not_possible",true)
            .classed("possible",false)
    }

    lassoEnd() {
        // Reset the color of all dots
        this.lasso.items()
            .classed("not_possible",false)
            .classed("possible",false);

        // Style the selected dots
        this.lasso.selectedItems()
            .attr("selected",true)
            .attr("r",7);

        // Reset the style of the not selected dots
        this.lasso.notSelectedItems()
            .attr("r",3.5);
    }
}