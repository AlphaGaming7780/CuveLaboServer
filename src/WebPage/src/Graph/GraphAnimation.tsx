import { graphData } from "./GraphData.tsx";

const totalDuration = 1000;
const delayBetweenPoints = () => totalDuration / (graphData.labels !== undefined ? graphData.labels.length : 1)
const previousY = (ctx) => { 
    // console.log(ctx.chart); 
    var data = ctx.chart.getDatasetMeta(ctx.datasetIndex).data
    // var data = graphData.datasets[ctx.datasetIndex].data
    // console.log(data)
    // console.log(ctx.index)

    return ctx.index > data.length || data.length === undefined || data.length === 0 ? 
        ctx.chart.scales.y.getPixelForValue(100) :
        ctx.index < data.length ? 
            data[ctx.index].getProps(['y'], true).y :
            data[ctx.index - 1].getProps(['y'], true).y 


    // return ctx.index === 0 || data.length === undefined || data.length === 0 || ctx.index < data.length ? 
    //     // ctx.chart.scales.y.getPixelForValue(0) :
    //     data[ctx.index].getProps(['y'], true).y :
    //     data[ctx.index - 1].getProps(['y'], true).y; 

    // return ctx.index === 0 || data === null || data.length < 2 ? 
    //     ctx.chart.scales.y.getPixelForValue(100) :
    //     data[ctx.index - 1]
    // return 0.5    
}

const previousX = (ctx) => { 
    // console.log(ctx.chart); 
    var data = ctx.chart.getDatasetMeta(ctx.datasetIndex).data
    // var data = graphData.datasets[ctx.datasetIndex].data
    // console.log(data)
    // console.log(ctx.index)

    return ctx.index > data.length || data.length === undefined || data.length === 0 ? 
        ctx.chart.scales.x.getPixelForValue(100) :
        ctx.index < data.length ? 
            data[ctx.index].getProps(['x'], true).x :   
            data[ctx.index - 1].getProps(['x'], true).x; 

    // return ctx.index === 0 || data.length === undefined || data.length === 0 || ctx.index < data.length ? 
    //     // ctx.chart.scales.y.getPixelForValue(0) :
    //     data[ctx.index].getProps(['x'], true).x :
    //     data[ctx.index - 1].getProps(['x'], true).x; 

    // return ctx.index === 0 || data === null || data.length < 2 ? 
    //     ctx.chart.scales.y.getPixelForValue(100) :
    //     data[ctx.index - 1]
    // return 0.5    
}

export const graphAnimation : any = { 
    // return {s
        x: {
            type: 'number',
            easing: "linear",
            duration: 1000,
            from: (ctx) => { var y = previousX(ctx); console.log(`from x:${y}`); return y },
            // delay(ctx) {
            //     if (ctx.type !== 'data' || ctx.xStarted) {
            //         return 0;
            //     }
            //     ctx.xStarted = true;
            //     return ctx.index * delayBetweenPoints();
            // }
        },
        y: {
            type: 'number',
            easing: 'linear',
            duration: 1000,
            from: (ctx) => { var y = previousY(ctx); console.log(`from y:${y}`); return y },
            // delay(ctx) {
            //     if (ctx.type !== 'data' || ctx.yStarted) {
            //         return 0;
            //     }
            //     ctx.yStarted = true;
            //     return ctx.index * delayBetweenPoints();
            // }
        }
    };
// }