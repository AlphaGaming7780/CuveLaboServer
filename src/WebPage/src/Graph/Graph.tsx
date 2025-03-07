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
	ChartType
  } from 'chart.js';
import { Line, ChartJSOrUndefined } from 'react-chartjs-2';
import { MotorSpeedContext } from "../API/MotorSpeed.tsx";
import { WaterLevelContext } from "../API/WaterLevel.tsx";

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
  };

// const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
const labels = [];

const data : ChartData<"line">  = {
    labels: [],
    datasets: [
        {
            label: 'Cuve 1 water level',
            // data: labels.map(() => Math.random() * 100),
            data: [],
            borderColor: 'rgb(99, 219, 255)',
            backgroundColor: 'rgba(99, 219, 255, 0.5)',
            yAxisID: 'WaterLevel',
        },
        {
            label: 'Cuve 2 water level',
            // data: labels.map(() => Math.random() * 100),
            data: [],
            borderColor: 'rgb(99, 193, 255)',
            backgroundColor: 'rgba(99, 193, 255, 0.5)',
            yAxisID: 'WaterLevel',
        },
        {
            label: 'Cuve 3 water level',
            // data: labels.map(() => Math.random() * 100),
            data: [],
            borderColor: 'rgb(99, 148, 255)',
            backgroundColor: 'rgba(99, 148, 255, 0.5)',
            yAxisID: 'WaterLevel',
        },
        {
            label: 'Motor 1 Speed',
            // data: labels.map(() => Math.random() * 100),
            data: [],
            borderColor: 'rgb(92, 168, 73)',
            backgroundColor: 'rgba(92, 168, 73, 0.5)',
            yAxisID: 'MotorSpeed',
        },
        {
            label: 'Motor 2 Speed',
            // data: labels.map(() => Math.random() * 100),
            data: [],
            borderColor: 'rgb(51, 187, 39)',
            backgroundColor: 'rgba(51, 187, 39, 0.5)',
            yAxisID: 'MotorSpeed',
        },
    ],
};

function AddValueToDataSet(WaterLevel : number[], MotorSpeed : number[]) {
	data.labels?.push(new Date().toLocaleTimeString())
	data.datasets[0].data.push(WaterLevel[0])
	data.datasets[1].data.push(WaterLevel[1])
	data.datasets[2].data.push(WaterLevel[2])
	data.datasets[3].data.push(MotorSpeed[0])
	data.datasets[4].data.push(MotorSpeed[1])
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

	const WaterLevel = useContext(MotorSpeedContext)
	const MotorSpeed = useContext(WaterLevelContext)

	useEffect( () => {

	},  )


	AddValueToDataSet(WaterLevel, MotorSpeed)

	console.log(data)

    return (
        <Line ref={ref} options={options} data={data} />
    )
}