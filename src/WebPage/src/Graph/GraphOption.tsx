import { ChartOptions } from "chart.js";
import { graphAnimation } from "./GraphAnimation.tsx";

export const graphOptions : ChartOptions<"line"> = {
    responsive: true,
    parsing: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Data Graph',
      },
      decimation: {
        enabled: true,
        algorithm: 'min-max',
      }
      
    },
    scales: {
        y: {
            type: 'linear' as const,
            display: true,
            position: 'left' as const,
            min: 0,
            max: 100,  
        },
        // WaterLevel: {
        //   type: 'linear' as const,
        //   display: true,
        //   position: 'left' as const,
        //   min: 0,
        //   max: 100,
        // },
        // MotorSpeed: {
        //     type: 'linear' as const,
        //     display: true,
        //     position: 'right' as const,
        //     grid: {
        //         drawOnChartArea: false,
        //     },
		// 	min: 0,
		// 	max: 100,
        // },
    },

    // animation: {
    //     duration: 1000,
    //     easing: "linear",
    // },
    // animations: {
        // ...graphAnimation
        // x: {
        //     properties: ["x"],
        //     duration: 1000,
        //     easing: 'linear',
        //     loop: false,
        //     from: undefined,
        //     to: undefined
        // },
        // y: {
        //     properties: ["y"],
        //     duration: 1000,
        //     easing: 'linear',
        //     loop: false,
        //     from: undefined,
        //     to: undefined
        // }
    // }
};