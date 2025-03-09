// Plugin simpa pour le chartJS
// https://chartjs-plugin-datalabels.netlify.app/samples/scriptable/interactions.html
// https://github.com/AbelHeinsbroek/chartjs-plugin-crosshair
// https://github.com/Makanz/chartjs-plugin-trendline

import React, { useContext, useEffect, useRef } from "react";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ChartData, 
    ChartOptions,
    ChartDataset,
  } from 'chart.js';
import { Line, ChartJSOrUndefined } from 'react-chartjs-2';
import { UpdatedValueContext } from "../API/UpdatedValue.tsx";

const options : ChartOptions<"line"> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Chart.js Line Chart',
      },
    },
    scales: {
        WaterLevel: {
          type: 'linear' as const,
          display: true,
          position: 'left' as const,
          min: 0,
          max: 100,
        },
        MotorSpeed: {
            type: 'linear' as const,
            display: true,
            position: 'right' as const,
            grid: {
                drawOnChartArea: false,
            },
			min: 0,
			max: 100,
        },
    },
    // animation: {
    //     duration: 1000,
    //     easing: "linear",
    // },
    animations: {
        x: {
            properties: ["x"],
            duration: 1100, // Animation de 2s
            easing: 'linear',
            loop: false
        },
        y: {
            properties: ["y"],
            duration: 1,
            easing: 'linear',
            loop: false,
        }
    }
};

const commonDatasetoption : Partial<ChartDataset<"line">> = {
    pointRadius: 0, // Supprime les points
    fill: false,    // Remplis la zone sous la courbe
    // tension: 0.1,   // Rend la ligne fluid
}

const data : ChartData<"line">  = {
    labels: [],
    datasets: [
        {
            label: 'Cuve 1 water level',
            borderColor: 'rgb(99, 219, 255)',
            backgroundColor: 'rgba(99, 219, 255, 0.5)',
            yAxisID: 'WaterLevel',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Cuve 2 water level',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(99, 193, 255)',
            backgroundColor: 'rgba(99, 193, 255, 0.5)',
            yAxisID: 'WaterLevel',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Cuve 3 water level',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(99, 148, 255)',
            backgroundColor: 'rgba(99, 148, 255, 0.5)',
            yAxisID: 'WaterLevel',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Motor 1 Speed',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(92, 168, 73)',
            backgroundColor: 'rgba(92, 168, 73, 0.5)',
            yAxisID: 'MotorSpeed',
            data: [],
            ...commonDatasetoption,
        },
        {
            label: 'Motor 2 Speed',
            // data: labels.map(() => Math.random() * 100),
            borderColor: 'rgb(51, 187, 39)',
            backgroundColor: 'rgba(51, 187, 39, 0.5)',
            yAxisID: 'MotorSpeed',
            data: [],
            ...commonDatasetoption,
        },
    ],
};

function AddValueToDataSet(time: string, WaterLevel : number[], MotorSpeed : number[]) {
	data.labels?.push(time)
	data.datasets[0].data.push(WaterLevel[0] * 100)
	data.datasets[1].data.push(WaterLevel[1] * 100)
	data.datasets[2].data.push(WaterLevel[2] * 100)
	data.datasets[3].data.push(MotorSpeed[0] * 100)
	data.datasets[4].data.push(MotorSpeed[1] * 100)
}

export function Graph() : React.JSX.Element {

    ChartJS.register(
        CategoryScale,
        LinearScale,
        PointElement,
        LineElement,
        Title,
        Tooltip,
        Legend
    );

	const ref = useRef<ChartJSOrUndefined<"line">>(null)

	const updatedValue = useContext(UpdatedValueContext)

	useEffect( () => {

		AddValueToDataSet(updatedValue.time, updatedValue.WaterLevel, updatedValue.MotorSpeed)
		if(ref.current == null) return
		ref.current.data = data
		ref.current.update()
		console.log(ref.current.data)

	}, [updatedValue, ref]  )

    return (
        <Line title="Title" ref={ref} options={options} data={data} /> //plugins={[ChartDataLabels]}
    )
}