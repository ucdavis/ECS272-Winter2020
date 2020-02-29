class NewMapVis {
    constructor(data, html_root, dimensions) {
        this.data = data
        this.html_root = html_root

        this.width = dimensions.width
        this.height = dimensions.height
        this.margin = dimensions.margin

        this.min_color = '#ffe5e5'
        this.max_color = '#cc0000'
        this.outline_color = '#b9bbb6'
        this.fill_color = '#ffffff'

        this.process_data()
        this.init()
    }

    process_data() {

        // group incidents in countries at a specific date
        this.grouped_data = d3.nest()
            .key(d => { return d['Country/Region'] })
            .rollup(row => {
                return d3.sum(row, d => {
                    return d['2/1/20']
                })
            })
            .entries(this.data)
        
        // sum all infections
        var sum = d3.sum(this.grouped_data, d => { return d.value })

        // add data country names' ISO codes, calculate ratio to total cases
        this.grouped_data.forEach(element => {
            element.id = name_iso_lookup[element.key]
            element.value = element.value / sum
        });

        // IF NOT FAST ENOUGH USE THIS? ADD ALL ENTRIES, FILTER ON CHANGE
        // total2017 = d3.sum(
        //     plastics.filter(d => d.date.getFullYear() === 2017),
        //     d => d.weight
        //   )
    

        console.log(this.grouped_data)
    }

    init() {

        // Use theme
        am4core.useTheme(am4themes_animated);

        // Create Map instance
        var map = am4core.create(this.html_root, am4maps.MapChart);
        this.map = map

        // Set map definition and projection
        this.map.geodata = am4geodata_worldLow;
        this.map.projection = new am4maps.projections.Miller();

        // Create polygon series
        var polygonSeries = this.map.series.push(new am4maps.MapPolygonSeries());

        this.map.colors.list = [
            am4core.color(this.min_color),
            am4core.color(this.max_color)
            // am4core.color("#845EC2"),
            // am4core.color("#D65DB1"),
            // am4core.color("#FF6F91"),
            // am4core.color("#FF9671"),
            // am4core.color("#FFC75F"),
            // am4core.color("#F9F871")
          ];

        // Set min / max fill color
        polygonSeries.heatRules.push({
            property: 'fill',
            target: polygonSeries.mapPolygons.template,
            min: this.map.colors.getIndex(0),
            max: this.map.colors.getIndex(1),
        })

        polygonSeries.data = this.grouped_data
    
          
        // Make map load polygon data (state shapes and names) from GeoJSON
        polygonSeries.useGeodata = true;

        /* Configure series */
        var polygonTemplate = polygonSeries.mapPolygons.template;
        polygonTemplate.applyOnClones = true;
        polygonTemplate.togglable = true;
        polygonTemplate.tooltipText = "{name} : {value}";
        polygonTemplate.nonScalingStroke = true;
        polygonTemplate.strokeOpacity = 0.5;
        polygonTemplate.stroke = am4core.color(this.outline_color)
        polygonTemplate.fill = am4core.color(this.fill_color)
        //polygonTemplate.fill = chart.colors.getIndex(2);
        var lastSelected;
        polygonTemplate.events.on("hit", function (ev) {
            if (lastSelected) {
                // This line serves multiple purposes:
                // 1. Clicking a country twice actually de-activates, the line below
                //    de-activates it in advance, so the toggle then re-activates, making it
                //    appear as if it was never de-activated to begin with.
                // 2. Previously activated countries should be de-activated.
                lastSelected.isActive = false;
            }
            ev.target.series.chart.zoomToMapObject(ev.target);
            if (lastSelected !== ev.target) {
                lastSelected = ev.target;
            }
        })


        /* Create selected and hover states and set alternative fill color */
        var ss = polygonTemplate.states.create("active");
        ss.properties.fill = this.map.colors.getIndex(2);

        var hs = polygonTemplate.states.create("hover");
        hs.properties.fill = this.map.colors.getIndex(4);

        // Hide Antarctica
        polygonSeries.exclude = ["AQ"];

        // Small map
        this.map.smallMap = new am4maps.SmallMap();
        // Re-position to top right (it defaults to bottom left)
        this.map.smallMap.align = "right";
        this.map.smallMap.valign = "top";
        this.map.smallMap.series.push(polygonSeries);

        // Zoom control
        this.map.zoomControl = new am4maps.ZoomControl();

        var homeButton = new am4core.Button();
        homeButton.events.on("hit", function () {
            map.goHome();
        });

        homeButton.icon = new am4core.Sprite();
        homeButton.padding(7, 5, 7, 5);
        homeButton.width = 30;
        homeButton.icon.path = "M16,8 L14,8 L14,16 L10,16 L10,10 L6,10 L6,16 L2,16 L2,8 L0,8 L8,0 L16,8 Z M16,8";
        homeButton.marginBottom = 10;
        homeButton.parent = this.map.zoomControl;
        homeButton.insertBefore(this.map.zoomControl.plusButton);
    }

    update() {
        //this.map.dataProvider.areas = 
    }
}